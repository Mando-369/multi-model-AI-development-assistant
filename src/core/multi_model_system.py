import os
import re
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Union
from langchain_community.llms import Ollama
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .project_manager import ProjectManager
from .file_processor import FileProcessor
from .prompts import SYSTEM_PROMPTS, AGENT_MODES
from .context_enhancer import ContextEnhancer, enhance_vectorstore_retrieval
from .project_meta_manager import ProjectMetaManager

# Project root directory (2 levels up from this file: src/core/multi_model_system.py)
PROJECT_ROOT = Path(__file__).parent.parent.parent


def get_agent_meta_path(project_name: str, agent_mode: str) -> Path:
    """Get path to agent's meta file for a project."""
    agents_dir = PROJECT_ROOT / "projects" / project_name / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    return agents_dir / f"{agent_mode.lower()}_context.md"


def is_meta_question(question: str) -> bool:
    """Detect meta/identity questions that shouldn't load project context.

    These are questions about the model itself, not about coding tasks.
    Loading project context for these causes pollution and wrong answers.
    """
    q = question.lower().strip()

    # Identity questions
    identity_patterns = [
        "who are you", "what are you", "who am i talking to",
        "introduce yourself", "tell me about yourself",
        "what's your name", "what is your name",
    ]

    # Capability questions
    capability_patterns = [
        "what can you do", "what are you capable of",
        "what's your context window", "what is your context window",
        "how many tokens", "what model are you",
        "what are your capabilities", "what are your limitations",
    ]

    # Help questions
    help_patterns = [
        "how do i use you", "how does this work",
        "help me get started", "what should i know",
    ]

    all_patterns = identity_patterns + capability_patterns + help_patterns

    for pattern in all_patterns:
        if pattern in q:
            return True

    return False



class MultiModelGLMSystem:
    def __init__(self):
        # Simplified 2-model configuration
        # DeepSeek: Heavy reasoning (slower but smarter)
        # Qwen: Fast summarization and quick tasks
        self.models = {
            "DeepSeek-R1:32B (Reasoning)": "deepseek-r1:32b",
            "Qwen2.5:32B (Fast)": "qwen2.5:32b",
        }

        # Cache for model instances
        self._model_instances = {}

        # Initialize embeddings and vectorstore
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        self.vectorstore = Chroma(
            persist_directory=str(PROJECT_ROOT / "chroma_db"),
            embedding_function=self.embeddings
        )

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )

        # Initialize managers
        self.project_manager = ProjectManager()
        self.project_meta_manager = ProjectMetaManager()
        self.file_processor = FileProcessor(self.vectorstore, self.text_splitter)

        # Create necessary directories (using absolute paths)
        (PROJECT_ROOT / "uploads").mkdir(exist_ok=True)
        (PROJECT_ROOT / "projects").mkdir(exist_ok=True)
        (PROJECT_ROOT / "chroma_db").mkdir(exist_ok=True)
        (PROJECT_ROOT / "faust_documentation").mkdir(exist_ok=True)
        
        # Initialize context enhancer after vectorstore is ready
        self.context_enhancer = ContextEnhancer(self.vectorstore)

    def get_model_instance(self, model_name: str):
        """Get or create a cached model instance"""
        if model_name not in self._model_instances:
            model_id = self.models.get(model_name)
            if model_id:
                try:
                    self._model_instances[model_name] = Ollama(
                        model=model_id,
                        temperature=0.7,
                        system=SYSTEM_PROMPTS.get(model_name, ""),
                    )
                except Exception as e:
                    print(f"Error loading model {model_name}: {e}")
                    return None

        return self._model_instances.get(model_name)

    def generate_response(
        self,
        prompt: str,
        selected_model: str = "DeepSeek-R1:32B (Reasoning)",
        use_context: bool = True,
        project_name: str = "Default",
        chat_history: Optional[List[Tuple[str, str]]] = None,
        agent_mode: str = "General",
        **kwargs  # Accept extra args for compatibility
    ) -> Dict[str, Union[str, Dict]]:
        """Generate response with specialist agent mode.

        Args:
            prompt: User's request
            selected_model: Model to use (DeepSeek for reasoning, Qwen for fast tasks)
            use_context: Whether to use knowledge base context
            project_name: Project name for context
            chat_history: Previous conversation
            agent_mode: Specialist mode (General, FAUST, JUCE, Math, Physics)

        Returns:
            Dict with response and model info
        """
        try:
            # Use selected model directly
            final_model = selected_model if selected_model in self.models else "DeepSeek-R1:32B (Reasoning)"

            response_text = self.chat_with_model(
                prompt, final_model, use_context, project_name, chat_history, agent_mode
            )

            return {
                "response": response_text,
                "routing": {
                    "mode": "direct",
                    "selected_model": final_model,
                    "agent_mode": agent_mode,
                }
            }

        except Exception as e:
            # Fallback to DeepSeek
            response_text = self.chat_with_model(
                prompt, "DeepSeek-R1:32B (Reasoning)", use_context, project_name, chat_history, agent_mode
            )

            return {
                "response": response_text,
                "routing": {
                    "mode": "fallback",
                    "selected_model": "DeepSeek-R1:32B (Reasoning)",
                    "agent_mode": agent_mode,
                    "error": str(e),
                }
            }

    def quick_summarize(self, text: str, max_words: int = 50) -> str:
        """Use Qwen for fast summarization.

        Args:
            text: Text to summarize
            max_words: Maximum words in summary

        Returns:
            Summary string
        """
        prompt = f"""Summarize the following in {max_words} words or less. Be concise and capture the key points:

{text}

Summary:"""

        try:
            llm = self.get_model_instance("Qwen2.5:32B (Fast)")
            if llm:
                response = llm.invoke(prompt)
                return response.strip()
            else:
                return "Error: Qwen model not available"
        except Exception as e:
            return f"Error summarizing: {e}"

    def generate_title(self, chat_history: str, max_words: int = 6) -> str:
        """Generate a short title for a chat session using Qwen (fast).

        Args:
            chat_history: The chat content to title
            max_words: Maximum words in title (default 6)

        Returns:
            Title string
        """
        prompt = f"""Generate a {max_words}-word title that captures the main topic of this conversation.
Return ONLY the title, nothing else.

Conversation:
{chat_history[:2000]}

Title:"""

        try:
            llm = self.get_model_instance("Qwen2.5:32B (Fast)")
            if llm:
                response = llm.invoke(prompt)
                # Clean up response - take first line, strip quotes
                title = response.strip().split('\n')[0].strip('"\'')
                # Limit to max_words
                words = title.split()[:max_words]
                return ' '.join(words)
            else:
                return "Untitled Chat"
        except Exception as e:
            return "Untitled Chat"

    def summarize_multiple_chats(self, chat_contents: List[str], max_words: int = 200) -> str:
        """Summarize multiple chat sessions into a combined context using Qwen (fast).

        Args:
            chat_contents: List of chat content strings
            max_words: Maximum words in summary

        Returns:
            Combined summary
        """
        combined = "\n\n---\n\n".join(chat_contents)

        prompt = f"""Summarize these related conversations into a coherent context summary of {max_words} words or less.
Focus on: key decisions, technical approaches, and important details.

Conversations:
{combined[:8000]}

Context Summary:"""

        try:
            llm = self.get_model_instance("Qwen2.5:32B (Fast)")
            if llm:
                response = llm.invoke(prompt)
                return response.strip()
            else:
                return "Error: Qwen model not available"
        except Exception as e:
            return f"Error summarizing: {e}"

    def read_agent_meta(self, project_name: str, agent_mode: str) -> str:
        """Read agent's meta context file.

        Returns the content of the meta file, or empty string if not exists.
        """
        meta_path = get_agent_meta_path(project_name, agent_mode)
        if meta_path.exists():
            try:
                return meta_path.read_text(encoding="utf-8")
            except Exception as e:
                print(f"❌ Error reading agent meta: {e}")
                return ""
        return ""

    def save_agent_meta(self, project_name: str, agent_mode: str, content: str) -> bool:
        """Save manually edited agent meta file.

        Returns True if saved successfully.
        """
        try:
            meta_path = get_agent_meta_path(project_name, agent_mode)
            meta_path.write_text(content, encoding="utf-8")
            print(f"✅ Saved {agent_mode} agent meta for {project_name}")
            return True
        except Exception as e:
            print(f"❌ Error saving agent meta: {e}")
            return False

    def clear_agent_meta(self, project_name: str, agent_mode: str) -> bool:
        """Clear/reset agent meta file.

        Returns True if cleared successfully.
        """
        try:
            meta_path = get_agent_meta_path(project_name, agent_mode)
            if meta_path.exists():
                meta_path.unlink()
                print(f"🗑️ Cleared {agent_mode} agent meta for {project_name}")
            return True
        except Exception as e:
            print(f"❌ Error clearing agent meta: {e}")
            return False

    def update_agent_meta(
        self,
        project_name: str,
        agent_mode: str,
        question: str,
        answer: str,
    ) -> bool:
        """Update agent's meta context file using Qwen (fast).

        Qwen analyzes the current exchange and updates the meta file
        with relevant context for future questions.
        """
        try:
            meta_path = get_agent_meta_path(project_name, agent_mode)
            current_meta = self.read_agent_meta(project_name, agent_mode)

            # Get agent config for context
            agent_config = AGENT_MODES.get(agent_mode, AGENT_MODES["General"])

            # Build the update prompt for Qwen
            # 2000 words allows detailed context while staying within model limits
            # (~3000 tokens, small fraction of 32K+ context windows)
            prompt = f"""You are updating a context summary file for a {agent_mode} coding assistant.

CURRENT CONTEXT FILE:
{current_meta if current_meta else "(Empty - this is a new session)"}

NEW EXCHANGE:
User: {question[:1500]}
Assistant: {answer[:3000]}

TASK:
Update the context file to include relevant information from this exchange.
Keep comprehensive but focused (max 2000 words).
Preserve important code snippets and technical details.
Structure it as:

# {agent_mode} Agent Context

## Current Focus
(What the user is currently working on - be specific)

## Key Decisions
(Important technical choices made with reasoning)

## Active Problems
(Open questions or issues being solved)

## Important Code/Patterns
(Key code snippets, algorithms, or patterns discussed - preserve these fully)

## Technical Notes
(Architecture decisions, performance considerations, dependencies)

## Session History
(Brief summary of conversation flow and topics covered)

Return ONLY the updated context file content, nothing else."""

            llm = self.get_model_instance("Qwen2.5:32B (Fast)")
            if llm:
                updated_meta = llm.invoke(prompt)
                meta_path.write_text(updated_meta.strip(), encoding="utf-8")
                print(f"✅ Updated {agent_mode} agent meta for {project_name}")
                return True
            else:
                print("⚠️ Qwen not available for meta update")
                return False

        except Exception as e:
            print(f"❌ Error updating agent meta: {e}")
            return False

    def chat_with_model(
        self,
        question: str,
        model_name: str,
        use_context: bool = True,
        project_name: str = "Default",
        chat_history: Optional[List[Tuple[str, str]]] = None,
        agent_mode: str = "General",
    ) -> str:
        """Chat with a specific model with specialist agent mode"""
        try:
            # Get model instance
            llm = self.get_model_instance(model_name)
            if not llm:
                return f"❌ Model {model_name} is not available. Please check if it's installed with 'ollama pull {self.models[model_name]}'"

            # Ensure chat_history is a list
            if chat_history is None:
                chat_history = []

            # Get agent mode configuration
            agent_config = AGENT_MODES.get(agent_mode, AGENT_MODES["General"])
            agent_prompt_addon = agent_config.get("system_prompt_addon", "")

            # Check for meta/identity questions - skip context to avoid pollution
            is_meta = is_meta_question(question)
            if is_meta:
                print("ℹ️ Meta question detected - skipping project/KB context to avoid pollution")

            # Build context using agent meta file (fast, focused, no pollution)
            if use_context and not is_meta:
                context_parts = []

                # 1. Add agent system prompt (domain expertise)
                if agent_prompt_addon:
                    context_parts.append(f"=== {agent_mode.upper()} SPECIALIST MODE ===\n{agent_prompt_addon}")
                    print(f"🎯 Using {agent_mode} specialist mode")

                # 2. Add PROJECT_META.md (project-level strategic context)
                # This gives all agents visibility into the master plan
                project_meta = self.project_meta_manager.read_project_meta(project_name)
                if project_meta:
                    truncated_meta = self.project_meta_manager.truncate_for_context(project_meta, max_chars=2000)
                    context_parts.append(f"=== PROJECT OVERVIEW ===\n{truncated_meta}")
                    print(f"✅ Loaded PROJECT_META.md ({len(truncated_meta)} chars)")

                # 3. Read agent meta file (pre-summarized context by Qwen)
                # Special case for Orchestrator: load ALL agent metas for cross-agent synthesis
                if agent_mode == "Orchestrator":
                    all_agent_metas = self.project_meta_manager.get_all_agent_metas(project_name)
                    if all_agent_metas:
                        combined_metas = "\n\n".join([
                            f"--- {mode.upper()} AGENT ---\n{content[:800]}{'...' if len(content) > 800 else ''}"
                            for mode, content in all_agent_metas.items()
                        ])
                        context_parts.append(f"=== ALL AGENT CONTEXTS ===\n{combined_metas}")
                        print(f"✅ Loaded {len(all_agent_metas)} agent metas for Orchestrator")
                else:
                    # Standard agent: load only its own meta
                    agent_meta = self.read_agent_meta(project_name, agent_mode)
                    if agent_meta:
                        context_parts.append(f"=== {agent_mode.upper()} AGENT CONTEXT ===\n{agent_meta}")
                        print(f"✅ Loaded {agent_mode} agent meta ({len(agent_meta)} chars)")
                    else:
                        print(f"ℹ️ No {agent_mode} agent meta yet - will be created after this exchange")

                # 4. Only include last exchange for immediate continuity
                # (More history is already summarized in the agent meta file)
                if chat_history and len(chat_history) > 0:
                    last_q, last_a = chat_history[-1]
                    # Truncate to keep it focused
                    last_exchange = f"Previous exchange:\nUser: {last_q[:300]}{'...' if len(last_q) > 300 else ''}\nAssistant: {last_a[:500]}{'...' if len(last_a) > 500 else ''}"
                    context_parts.append(f"=== LAST EXCHANGE ===\n{last_exchange}")
                    print("✅ Included last exchange for continuity")

                # Build the enhanced prompt
                if context_parts:
                    full_context = "\n\n".join(context_parts)
                    enhanced_prompt = f"""{full_context}

=== CURRENT QUESTION ===
{question}

=== INSTRUCTIONS ===
Please provide a detailed and helpful response based on the context above and your knowledge. 
If the conversation history shows we were discussing something specific, please continue that conversation naturally.
Reference the knowledge base information when relevant."""

                    print(
                        f"🚀 Sending enhanced prompt with {len(context_parts)} context sections"
                    )
                    response = llm.invoke(enhanced_prompt)
                else:
                    print("⚠️ No context available, using basic prompt")
                    response = llm.invoke(question)
            else:
                print("📝 Context disabled, using direct question")
                response = llm.invoke(question)

            # Track model usage in project
            metadata = self.project_manager.get_project_metadata(project_name)
            if model_name not in metadata.get("models_used", []):
                metadata.setdefault("models_used", []).append(model_name)
                self.project_manager.update_project_metadata(project_name, metadata)

            # Update agent meta file with this exchange (async, using Qwen)
            # Skip for meta questions (they don't add project context)
            if not is_meta and project_name != "Default":
                try:
                    # Run meta update in background - don't block the response
                    import threading
                    update_thread = threading.Thread(
                        target=self.update_agent_meta,
                        args=(project_name, agent_mode, question, response),
                        daemon=True
                    )
                    update_thread.start()
                    print(f"📝 Started background meta update for {agent_mode}")
                except Exception as e:
                    print(f"⚠️ Could not start meta update: {e}")

            return response

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}\n\nMake sure the model is installed with:\nollama pull {self.models[model_name]}"
            print(f"❌ Chat error: {e}")
            return error_msg

    def check_vectorstore_status(self):
        """Check if vectorstore has documents and get count (excluding test documents)"""
        try:
            # Get actual document count from ChromaDB collection, excluding test documents
            collection = self.vectorstore._collection
            
            # Get all documents with metadata to filter out test documents
            all_docs = collection.get(include=['metadatas'])
            
            # Count only non-test documents
            real_doc_count = 0
            test_doc_count = 0
            
            for meta in all_docs['metadatas']:
                if meta.get('is_test_data', False):
                    test_doc_count += 1
                else:
                    real_doc_count += 1
            
            total_count = real_doc_count + test_doc_count
            
            # Status message includes both counts for transparency
            if real_doc_count > 0:
                message = f"Knowledge base contains {real_doc_count} documents"
                if test_doc_count > 0:
                    message += f" ({test_doc_count} test documents excluded)"
            else:
                if test_doc_count > 0:
                    message = f"No real documents loaded ({test_doc_count} test documents excluded). Upload files or load documentation."
                else:
                    message = "No documents in knowledge base. Upload files to improve context."
            
            return {
                "status": "✅ Ready" if real_doc_count > 0 else "⚠️ Empty",
                "document_count": real_doc_count,
                "total_count": total_count,
                "test_count": test_doc_count,
                "message": message,
            }
            
        except Exception as e:
            # Fallback to similarity search method if direct count fails
            try:
                test_results = self.vectorstore.similarity_search("test", k=100)  # Higher limit
                doc_count = len(test_results)
                return {
                    "status": "✅ Ready" if doc_count > 0 else "⚠️ Empty",
                    "document_count": doc_count,
                    "total_count": doc_count,
                    "test_count": 0,
                    "message": (
                        f"Knowledge base contains {doc_count}+ documents (test filtering unavailable)"
                        if doc_count > 0
                        else "No documents in knowledge base. Upload files to improve context."
                    ),
                }
            except Exception as fallback_error:
                return {
                    "status": "❌ Error",
                    "document_count": 0,
                    "total_count": 0,
                    "test_count": 0,
                    "message": f"Error accessing knowledge base: {fallback_error}",
                }

    def check_model_availability(self):
        """Check which models are available"""
        status = {}

        for model_name, model_id in self.models.items():
            try:
                # Try to create an instance
                llm = Ollama(model=model_id)
                # Try a simple test
                llm.invoke("test")
                status[model_name] = "✅ Available"
            except Exception as e:
                if "not found" in str(e).lower():
                    status[model_name] = f"❌ Not installed"
                else:
                    status[model_name] = f"⚠️ Error: {str(e)[:50]}"

        return status

    def get_available_models(self):
        """Get list of available models"""
        available = []
        for model_name in self.models.keys():
            if model_name in self._model_instances:
                available.append(model_name)
            else:
                # Try to load it
                if self.get_model_instance(model_name):
                    available.append(model_name)

        return available
