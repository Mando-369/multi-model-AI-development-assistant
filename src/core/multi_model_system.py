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
from .prompts import SYSTEM_PROMPTS, AGENT_MODES, get_system_prompt_for_model
from .context_enhancer import ContextEnhancer, enhance_vectorstore_retrieval
from .project_meta_manager import ProjectMetaManager
from .model_config import get_model_config, ModelConfigManager
from .model_backends import get_backend_manager, BackendManager

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
        # Dynamic model configuration from config manager
        self.model_config = get_model_config()
        self.backend_manager = get_backend_manager()

        # Cache for model instances
        self._model_instances = {}

        # Initialize system components
        self._initialize_system()

    @property
    def models(self) -> Dict[str, str]:
        """Get current model configuration as display_name -> model_id dict."""
        return self.model_config.get_models_dict()

    def get_reasoning_model_name(self) -> str:
        """Get the display name of the reasoning model."""
        return self.model_config.get_reasoning_display_name()

    def get_fast_model_name(self) -> str:
        """Get the display name of the fast model."""
        return self.model_config.get_fast_display_name()

    def reload_config(self):
        """Reload model configuration and clear cache."""
        self.model_config.reload()
        self._model_instances.clear()

    def _initialize_system(self):
        """Initialize embeddings, vectorstore, and managers."""
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
                    # Determine model role for system prompt
                    model_role = None
                    if model_name == self.get_reasoning_model_name():
                        model_role = "reasoning"
                    elif model_name == self.get_fast_model_name():
                        model_role = "fast"

                    system_prompt = get_system_prompt_for_model(model_name, model_role or "reasoning")

                    self._model_instances[model_name] = Ollama(
                        model=model_id,
                        temperature=0.7,
                        system=system_prompt,
                    )
                except Exception as e:
                    print(f"Error loading model {model_name}: {e}")
                    return None

        return self._model_instances.get(model_name)

    def generate_response(
        self,
        prompt: str,
        selected_model: Optional[str] = None,
        use_context: bool = True,
        project_name: str = "Default",
        chat_history: Optional[List[Tuple[str, str]]] = None,
        agent_mode: str = "General",
        **kwargs  # Accept extra args for compatibility
    ) -> Dict[str, Union[str, Dict]]:
        """Generate response with specialist agent mode.

        Args:
            prompt: User's request
            selected_model: Model to use (defaults to reasoning model from config)
            use_context: Whether to use knowledge base context
            project_name: Project name for context
            chat_history: Previous conversation
            agent_mode: Specialist mode (General, FAUST, JUCE, Math, Physics)

        Returns:
            Dict with response and model info
        """
        # Default to reasoning model from config
        if selected_model is None:
            selected_model = self.get_reasoning_model_name()

        try:
            # Use selected model directly
            final_model = selected_model if selected_model in self.models else self.get_reasoning_model_name()

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
            # Fallback to reasoning model
            reasoning_model = self.get_reasoning_model_name()
            response_text = self.chat_with_model(
                prompt, reasoning_model, use_context, project_name, chat_history, agent_mode
            )

            return {
                "response": response_text,
                "routing": {
                    "mode": "fallback",
                    "selected_model": reasoning_model,
                    "agent_mode": agent_mode,
                    "error": str(e),
                }
            }

    def quick_summarize(self, text: str, max_words: int = 50) -> str:
        """Use fast model for summarization.

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
            fast_model = self.get_fast_model_name()
            llm = self.get_model_instance(fast_model)
            if llm:
                response = llm.invoke(prompt)
                return response.strip()
            else:
                return f"Error: Fast model ({fast_model}) not available"
        except Exception as e:
            return f"Error summarizing: {e}"

    def generate_title(self, chat_history: str, max_words: int = 6) -> str:
        """Generate a short title for a chat session using fast model.

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
            fast_model = self.get_fast_model_name()
            llm = self.get_model_instance(fast_model)
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
        """Summarize multiple chat sessions into a combined context using fast model.

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
            fast_model = self.get_fast_model_name()
            llm = self.get_model_instance(fast_model)
            if llm:
                response = llm.invoke(prompt)
                return response.strip()
            else:
                return f"Error: Fast model ({fast_model}) not available"
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
        """Update agent's meta context file using fast model.

        Fast model analyzes the current exchange and updates the meta file
        with relevant context for future questions.
        """
        try:
            meta_path = get_agent_meta_path(project_name, agent_mode)
            current_meta = self.read_agent_meta(project_name, agent_mode)

            # Get agent config for context
            agent_config = AGENT_MODES.get(agent_mode, AGENT_MODES["General"])

            # Build the update prompt
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

            fast_model = self.get_fast_model_name()
            llm = self.get_model_instance(fast_model)
            if llm:
                updated_meta = llm.invoke(prompt)
                meta_path.write_text(updated_meta.strip(), encoding="utf-8")
                print(f"✅ Updated {agent_mode} agent meta for {project_name}")
                return True
            else:
                print(f"⚠️ Fast model ({fast_model}) not available for meta update")
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
                    # Handle both 2-tuple (legacy) and 3-tuple (with agent_mode) formats
                    last_entry = chat_history[-1]
                    last_q, last_a = last_entry[0], last_entry[1]
                    # Truncate to keep it focused
                    last_exchange = f"Previous exchange:\nUser: {last_q[:300]}{'...' if len(last_q) > 300 else ''}\nAssistant: {last_a[:500]}{'...' if len(last_a) > 500 else ''}"
                    context_parts.append(f"=== LAST EXCHANGE ===\n{last_exchange}")
                    print("✅ Included last exchange for continuity")

                # 5. Query vectorstore using AI-extracted keywords
                try:
                    relevant_docs = self._smart_doc_retrieval(question, agent_mode)
                    if relevant_docs:
                        doc_context = "\n\n".join([
                            f"[{doc.metadata.get('source', 'docs')}]\n{doc.page_content[:1000]}"
                            for doc in relevant_docs
                        ])
                        context_parts.append(f"=== RELEVANT DOCUMENTATION ===\n{doc_context}")
                        print(f"📚 Retrieved {len(relevant_docs)} docs via smart retrieval")
                except Exception as e:
                    print(f"⚠️ Smart retrieval failed: {e}")

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

    def stream_chat_response(
        self,
        question: str,
        model_name: str,
        use_context: bool = True,
        project_name: str = "Default",
        agent_mode: str = "General",
    ):
        """Stream response tokens from model. Yields string chunks.

        This is the streaming version of chat_with_model. Use for real-time
        display of AI responses.

        Yields special [STATUS] prefixed messages for UI updates before the actual response.
        """
        try:
            llm = self.get_model_instance(model_name)
            if not llm:
                yield f"❌ Model {model_name} is not available"
                return

            # Get agent mode configuration
            agent_config = AGENT_MODES.get(agent_mode, AGENT_MODES["General"])
            agent_prompt_addon = agent_config.get("system_prompt_addon", "")

            # Check for meta questions
            is_meta = is_meta_question(question)

            # Build context (same logic as chat_with_model)
            enhanced_prompt = question
            if use_context and not is_meta:
                context_parts = []

                if agent_prompt_addon:
                    context_parts.append(f"=== {agent_mode.upper()} SPECIALIST MODE ===\n{agent_prompt_addon}")
                    yield f"[STATUS]🎯 Using {agent_mode} specialist mode"

                project_meta = self.project_meta_manager.read_project_meta(project_name)
                if project_meta:
                    truncated_meta = self.project_meta_manager.truncate_for_context(project_meta, max_chars=2000)
                    context_parts.append(f"=== PROJECT OVERVIEW ===\n{truncated_meta}")
                    yield f"[STATUS]📋 Loaded project meta ({len(truncated_meta)} chars)"

                if agent_mode == "Orchestrator":
                    all_agent_metas = self.project_meta_manager.get_all_agent_metas(project_name)
                    if all_agent_metas:
                        combined_metas = "\n\n".join([
                            f"--- {mode.upper()} AGENT ---\n{content[:800]}{'...' if len(content) > 800 else ''}"
                            for mode, content in all_agent_metas.items()
                        ])
                        context_parts.append(f"=== ALL AGENT CONTEXTS ===\n{combined_metas}")
                        yield f"[STATUS]🔗 Loaded {len(all_agent_metas)} agent contexts"
                else:
                    agent_meta = self.read_agent_meta(project_name, agent_mode)
                    if agent_meta:
                        context_parts.append(f"=== {agent_mode.upper()} AGENT CONTEXT ===\n{agent_meta}")
                        yield f"[STATUS]📝 Loaded {agent_mode} context ({len(agent_meta)} chars)"

                # Query vectorstore using AI-extracted keywords (with status updates)
                try:
                    yield "[STATUS]🔍 Extracting search keywords..."
                    relevant_docs, keywords = self._smart_doc_retrieval_with_status(question, agent_mode)
                    if keywords:
                        yield f"[STATUS]🔑 Keywords: {', '.join(keywords)}"
                    if relevant_docs:
                        doc_sources = [doc.metadata.get('source', 'docs').split('/')[-1] for doc in relevant_docs]
                        yield f"[STATUS]📚 Found {len(relevant_docs)} docs: {', '.join(doc_sources[:3])}{'...' if len(doc_sources) > 3 else ''}"
                        doc_context = "\n\n".join([
                            f"[{doc.metadata.get('source', 'docs')}]\n{doc.page_content[:1000]}"
                            for doc in relevant_docs
                        ])
                        context_parts.append(f"=== RELEVANT DOCUMENTATION ===\n{doc_context}")
                    else:
                        yield "[STATUS]📭 No matching docs found"
                except Exception as e:
                    yield f"[STATUS]⚠️ Doc retrieval failed: {str(e)[:50]}"
                    print(f"⚠️ Smart retrieval failed: {e}")

                if context_parts:
                    full_context = "\n\n".join(context_parts)
                    enhanced_prompt = f"""{full_context}

=== CURRENT QUESTION ===
{question}

=== INSTRUCTIONS ===
Please provide a detailed and helpful response based on the context above and your knowledge."""

            # Signal start of AI response
            yield "[STATUS]🤖 Generating response..."
            yield "[STREAM_START]"

            # Stream response
            print(f"🔄 Streaming response from {model_name}...")
            for chunk in llm.stream(enhanced_prompt):
                yield chunk

        except Exception as e:
            yield f"❌ Error: {str(e)}"
            print(f"❌ Stream error: {e}")

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
            
            for meta in (all_docs['metadatas'] or []):
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

    def analyze_faust_in_response(self, response_text: str) -> Optional[Dict]:
        """
        Detect FAUST code in response and analyze it via faust-mcp.

        Args:
            response_text: The response text potentially containing FAUST code

        Returns:
            Analysis result dict if FAUST code was found and analyzed, None otherwise.
        """
        try:
            from .faust_mcp_client import analyze_faust_code, check_faust_server

            # Check if server is available
            if not check_faust_server():
                print("ℹ️ faust-mcp server not running - skipping analysis")
                return None

            # Find FAUST code blocks - look for code with stdfaust.lib import and process definition
            faust_pattern = r'```(?:faust|dsp)?\s*\n(.*?import\s*\(\s*["\']stdfaust\.lib["\']\s*\).*?process\s*=.*?)```'
            matches = re.findall(faust_pattern, response_text, re.DOTALL | re.IGNORECASE)

            if not matches:
                # Try alternative pattern without code fence
                alt_pattern = r'(import\s*\(\s*["\']stdfaust\.lib["\']\s*\);.*?process\s*=.*?;)'
                matches = re.findall(alt_pattern, response_text, re.DOTALL | re.IGNORECASE)

            if not matches:
                return None

            # Analyze the first/main FAUST code block
            faust_code = matches[0].strip()
            print(f"🎛️ Detected FAUST code, analyzing via faust-mcp...")

            result = analyze_faust_code(faust_code)

            return {
                "status": result.status,
                "max_amplitude": result.max_amplitude,
                "rms": result.rms,
                "is_silent": result.is_silent,
                "waveform": result.waveform_ascii,
                "num_outputs": result.num_outputs,
                "channels": result.channels,
                "features": result.features,
                "error": result.error,
                "summary": result.get_summary(),
            }

        except ImportError:
            print("⚠️ faust_mcp_client not available")
            return None
        except Exception as e:
            print(f"❌ Error analyzing FAUST code: {e}")
            return None

    def check_faust_server_status(self) -> Dict:
        """Check if faust-mcp server is running and get backend info."""
        try:
            from .faust_mcp_client import (
                check_faust_server,
                detect_faust_backend,
                get_faust_version,
            )

            server_running = check_faust_server()
            backend = detect_faust_backend()
            faust_version = get_faust_version()

            return {
                "server_running": server_running,
                "backend": backend,
                "faust_version": faust_version,
                "status": "✅ Ready" if server_running else "⚠️ Server not running",
                "message": (
                    f"faust-mcp server running ({backend} backend)"
                    if server_running
                    else f"Start server with: python tools/faust-mcp/faust_server.py"
                ),
            }

        except ImportError:
            return {
                "server_running": False,
                "backend": "none",
                "faust_version": None,
                "status": "❌ Not installed",
                "message": "faust_mcp_client module not available",
            }

    def _smart_doc_retrieval_with_status(self, question: str, agent_mode: str, max_docs: int = 5) -> tuple:
        """Use fast AI to extract search keywords, then query ChromaDB.

        Returns:
            Tuple of (documents, keywords) for UI visibility
        """
        docs, keywords = [], []
        try:
            fast_model = self.get_fast_model_name()
            llm = self.get_model_instance(fast_model)

            if not llm:
                docs = self.vectorstore.similarity_search(question, k=max_docs)
                return docs, ["(direct search)"]

            mode_hints = {
                "FAUST": "FAUST DSP, signal processing, audio synthesis, filters, oscillators",
                "JUCE": "JUCE C++, audio plugins, VST, AU, GUI components",
                "Math": "DSP algorithms, filter design, Fourier transform, z-transform",
                "Physics": "acoustics, electronics, circuits, wave propagation",
                "General": "programming, code, development",
            }
            domain_hint = mode_hints.get(agent_mode, "programming")

            keyword_prompt = f"""Extract 3-5 precise search keywords from this question for documentation lookup.
Domain context: {domain_hint}

Question: {question}

Rules:
- Return ONLY the keywords, one per line
- Focus on technical terms, function names, concepts
- No full sentences, just key terms
- If it's an error message, extract the key identifiers

Keywords:"""

            keyword_response = llm.invoke(keyword_prompt)

            for line in keyword_response.strip().split('\n'):
                keyword = line.strip().strip('-•*1234567890.').strip()
                if keyword and len(keyword) > 1 and len(keyword) < 50:
                    keywords.append(keyword)

            keywords = keywords[:5]

            if not keywords:
                docs = self.vectorstore.similarity_search(question, k=max_docs)
                return docs, ["(no keywords, direct search)"]

            all_docs = []
            seen_content = set()

            for keyword in keywords:
                try:
                    found = self.vectorstore.similarity_search(keyword, k=3)
                    for doc in found:
                        content_hash = hash(doc.page_content[:200])
                        if content_hash not in seen_content:
                            seen_content.add(content_hash)
                            all_docs.append(doc)
                except Exception:
                    continue

            return all_docs[:max_docs], keywords

        except Exception as e:
            print(f"❌ Smart retrieval error: {e}")
            try:
                return self.vectorstore.similarity_search(question, k=max_docs), ["(fallback)"]
            except:
                return [], []

    def _smart_doc_retrieval(self, question: str, agent_mode: str, max_docs: int = 5) -> List:
        """Use fast AI to extract search keywords, then query ChromaDB.

        Args:
            question: User's question/prompt
            agent_mode: Current specialist mode for context hints
            max_docs: Maximum documents to return

        Returns:
            List of relevant documents (deduplicated)
        """
        try:
            # Get the fast model for keyword extraction
            fast_model = self.get_fast_model_name()
            llm = self.get_model_instance(fast_model)

            if not llm:
                print("⚠️ Fast model not available for keyword extraction, using direct search")
                return self.vectorstore.similarity_search(question, k=max_docs)

            # Build keyword extraction prompt based on agent mode
            mode_hints = {
                "FAUST": "FAUST DSP, signal processing, audio synthesis, filters, oscillators",
                "JUCE": "JUCE C++, audio plugins, VST, AU, GUI components",
                "Math": "DSP algorithms, filter design, Fourier transform, z-transform",
                "Physics": "acoustics, electronics, circuits, wave propagation",
                "General": "programming, code, development",
            }
            domain_hint = mode_hints.get(agent_mode, "programming")

            keyword_prompt = f"""Extract 3-5 precise search keywords from this question for documentation lookup.
Domain context: {domain_hint}

Question: {question}

Rules:
- Return ONLY the keywords, one per line
- Focus on technical terms, function names, concepts
- No full sentences, just key terms
- If it's an error message, extract the key identifiers

Keywords:"""

            # Get keywords from fast model
            keyword_response = llm.invoke(keyword_prompt)

            # Parse keywords (one per line, clean up)
            keywords = []
            for line in keyword_response.strip().split('\n'):
                keyword = line.strip().strip('-•*1234567890.').strip()
                if keyword and len(keyword) > 1 and len(keyword) < 50:
                    keywords.append(keyword)

            # Limit to 5 keywords max
            keywords = keywords[:5]

            if not keywords:
                print("⚠️ No keywords extracted, using question directly")
                return self.vectorstore.similarity_search(question, k=max_docs)

            print(f"🔍 Extracted keywords: {keywords}")

            # Query vectorstore with each keyword and collect results
            all_docs = []
            seen_content = set()

            for keyword in keywords:
                try:
                    docs = self.vectorstore.similarity_search(keyword, k=3)
                    for doc in docs:
                        # Deduplicate by content hash
                        content_hash = hash(doc.page_content[:200])
                        if content_hash not in seen_content:
                            seen_content.add(content_hash)
                            all_docs.append(doc)
                except Exception as e:
                    print(f"⚠️ Search failed for '{keyword}': {e}")
                    continue

            # Return top docs up to max_docs
            return all_docs[:max_docs]

        except Exception as e:
            print(f"❌ Smart retrieval error: {e}")
            # Fallback to direct search
            try:
                return self.vectorstore.similarity_search(question, k=max_docs)
            except:
                return []
