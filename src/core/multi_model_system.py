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

# Project root directory (2 levels up from this file: src/core/multi_model_system.py)
PROJECT_ROOT = Path(__file__).parent.parent.parent



class MultiModelGLMSystem:
    def __init__(self):
        # Simplified 2-model configuration
        # DeepSeek: Heavy reasoning (slower but smarter)
        # Qwen: Fast summarization and quick tasks
        self.models = {
            "DeepSeek-R1:70B (Reasoning)": "deepseek-r1:70b",
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
        selected_model: str = "DeepSeek-R1:70B (Reasoning)",
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
            final_model = selected_model if selected_model in self.models else "DeepSeek-R1:70B (Reasoning)"

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
                prompt, "DeepSeek-R1:70B (Reasoning)", use_context, project_name, chat_history, agent_mode
            )

            return {
                "response": response_text,
                "routing": {
                    "mode": "fallback",
                    "selected_model": "DeepSeek-R1:70B (Reasoning)",
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

            # Build enhanced context if enabled
            if use_context:
                context_parts = []

                # 0. Add agent mode context if not General
                if agent_prompt_addon:
                    context_parts.append(f"=== SPECIALIST MODE ===\n{agent_prompt_addon}")
                    print(f"🎯 Using {agent_mode} specialist mode")

                # 1. Get enhanced knowledge base context
                try:
                    # Use agent mode to determine task type for retrieval
                    task_type = agent_mode.lower() if agent_mode in ["FAUST", "JUCE"] else "general"
                    question_lower = question.lower()
                    if task_type == "general":
                        if any(term in question_lower for term in ["faust", "dsp", "signal processing", "audio effect"]):
                            task_type = "faust"
                        elif any(term in question_lower for term in ["juce", "plugin", "vst", "au", "processor"]):
                            task_type = "juce"
                    
                    # Get enhanced context
                    enhanced_context = enhance_vectorstore_retrieval(self.vectorstore, question, task_type)
                    
                    if enhanced_context:
                        context_parts.append(enhanced_context)
                        print(f"✅ Enhanced context retrieved for {task_type} task")
                    else:
                        # Fallback to basic retrieval
                        relevant_docs = self.vectorstore.similarity_search(question, k=5)
                        if relevant_docs:
                            kb_context = "\n\n".join(
                                [doc.page_content for doc in relevant_docs]
                            )
                            context_parts.append(
                                f"=== KNOWLEDGE BASE CONTEXT ===\n{kb_context[:3000]}"
                            )
                            print(f"✅ Found {len(relevant_docs)} relevant documents from knowledge base")
                        else:
                            print("⚠️ No relevant documents found in knowledge base")
                except Exception as e:
                    print(f"❌ Error accessing enhanced knowledge base: {e}")

                # 2. Get conversation history context
                if chat_history and len(chat_history) > 0:
                    # Include last 5 exchanges for context
                    recent_history = (
                        chat_history[-5:] if len(chat_history) > 5 else chat_history
                    )
                    history_context = []

                    for i, (prev_q, prev_a) in enumerate(recent_history, 1):
                        history_context.append(f"Exchange {i}:")
                        history_context.append(f"Human: {prev_q}")
                        history_context.append(
                            f"Assistant: {prev_a[:500]}{'...' if len(prev_a) > 500 else ''}"
                        )
                        history_context.append("")

                    if history_context:
                        context_parts.append(
                            f"=== CONVERSATION HISTORY ===\n"
                            + "\n".join(history_context)
                        )
                        print(
                            f"✅ Including {len(recent_history)} previous exchanges for context"
                        )

                # 3. Get project context
                try:
                    project_context = self.project_manager.get_project_context(
                        project_name
                    )
                    if project_context:
                        context_parts.append(
                            f"=== PROJECT CONTEXT ===\n{project_context}"
                        )
                        print(f"✅ Including project context from {project_name}")
                except Exception as e:
                    print(f"❌ Error getting project context: {e}")

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
