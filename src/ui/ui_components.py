import streamlit as st
from pathlib import Path
from ..core.prompts import MODEL_INFO, AGENT_MODES
from typing import Optional
import re


def generate_agent_context_suggestion(glm_system, project_name: str, agent_mode: str) -> Optional[str]:
    """Generate suggested agent context based on PROJECT_META.md and recent chat.

    Uses the selected model to create an improved agent context that aligns
    with the project overview and incorporates recent work.
    """
    try:
        # Get PROJECT_META.md content
        project_meta = glm_system.project_meta_manager.read_project_meta(project_name)
        if not project_meta:
            project_meta = "(No PROJECT_META.md found)"

        # Get current agent context
        current_context = glm_system.read_agent_meta(project_name, agent_mode)

        # Get agent configuration
        agent_config = AGENT_MODES.get(agent_mode, AGENT_MODES["General"])
        agent_description = agent_config.get("description", "General assistant")

        # Get recent chat history for this agent
        chat_key = f"chat_history_{project_name}"
        chat_history = st.session_state.get(chat_key, [])
        recent_exchanges = chat_history[-5:] if chat_history else []
        chat_summary = ""
        if recent_exchanges:
            chat_summary = "\n\n".join([
                f"Q: {q[:200]}...\nA: {a[:300]}..."
                for q, a in recent_exchanges
            ])

        prompt = f"""You are generating/updating context for a specialist AI agent.

AGENT: {agent_mode}
ROLE: {agent_description}

PROJECT OVERVIEW (PROJECT_META.md):
{project_meta}

CURRENT AGENT CONTEXT:
{current_context if current_context else "(No existing context)"}

RECENT CHAT EXCHANGES:
{chat_summary if chat_summary else "(No recent exchanges)"}

TASK:
Generate an improved agent context file that:
1. Summarizes what this agent needs to know about the project
2. Lists key decisions, constraints, and requirements relevant to this agent's specialty
3. Tracks the current state of work in this agent's domain
4. Notes any blockers or dependencies on other agents
5. Keeps important technical details from recent conversations

FORMAT:
# {agent_mode} Agent Context

## Project Relevance
(How this project relates to {agent_mode} specialty)

## Current Focus
(Active work items for this agent)

## Key Decisions
(Technical decisions in this agent's domain)

## Technical Notes
(Important details, constraints, patterns)

## Dependencies
(What this agent needs from other agents)

Keep it concise (under 500 words). Focus on actionable, project-specific information.
Return ONLY the context file content."""

        # Use Qwen for fast generation
        llm = glm_system.get_model_instance("Qwen2.5:32B (Fast)")
        if llm:
            result = llm.invoke(prompt)
            return result.strip()
        return None

    except Exception as e:
        print(f"Error generating agent context suggestion: {e}")
        return None


def render_agent_suggestion_approval(glm_system, project_name: str, agent_mode: str, suggestion_key: str):
    """Render agent context suggestion with approve/reject buttons."""
    st.write("---")
    st.markdown("**📝 Suggested Context Update**")

    suggestion = st.session_state[suggestion_key]

    with st.expander("Preview suggested context", expanded=True):
        st.code(suggestion, language="markdown")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Apply", type="primary", key=f"apply_agent_suggestion_{project_name}_{agent_mode}"):
            if glm_system.save_agent_meta(project_name, agent_mode, suggestion):
                st.success("Context updated!")
                st.session_state[suggestion_key] = None
                st.rerun()
            else:
                st.error("Failed to save")

    with col2:
        if st.button("❌ Discard", key=f"discard_agent_suggestion_{project_name}_{agent_mode}"):
            st.session_state[suggestion_key] = None
            st.rerun()


def get_code_language_from_content(content: str) -> str:
    """Detect programming language from code content"""
    # FAUST detection
    faust_keywords = ["import", "declare", "process", "library", "component", "with", "letrec", "fi.", "os.", "ma.", "de.", "re.", "en."]
    if any(keyword in content for keyword in faust_keywords):
        return "javascript"  # Use JavaScript as fallback for FAUST

    # Other language detection
    if "def " in content or "import " in content or "class " in content:
        return "python"
    elif "#include" in content or "int main" in content or "std::" in content:
        return "c_cpp"
    elif "function" in content and "{" in content:
        return "javascript"
    elif "package " in content and "public class" in content:
        return "java"

    return None


def extract_thinking_and_answer(response: str) -> tuple:
    """Extract thinking/reasoning and final answer from DeepSeek-R1 response.

    DeepSeek-R1 outputs reasoning in <think>...</think> tags.

    Returns:
        (thinking, answer) tuple - thinking may be None if not present
    """
    import re

    # Try to find <think> tags (DeepSeek-R1 format)
    think_pattern = r'<think>(.*?)</think>'
    think_match = re.search(think_pattern, response, re.DOTALL)

    if think_match:
        thinking = think_match.group(1).strip()
        # Remove thinking from response to get the answer
        answer = re.sub(think_pattern, '', response, flags=re.DOTALL).strip()
        return thinking, answer

    # No thinking tags found - return as-is
    return None, response


def display_response_with_thinking(answer: str, selected_model: str):
    """Display response with optional thinking section for R1 models."""
    thinking, final_answer = extract_thinking_and_answer(answer)

    # Show thinking section if present (R1 models)
    if thinking and "R1" in selected_model:
        with st.expander("🧠 **Reasoning Process** (click to expand)", expanded=False):
            st.markdown(thinking)
        st.markdown("---")

    # Show the final answer
    st.markdown(f"**🤖 {selected_model}:**")
    if "```" in final_answer:
        st.markdown(final_answer)
    else:
        st.write(final_answer)


def render_project_management(glm_system):
    """Render project management section with file handling"""
    # Add styling for better visibility
    st.markdown(
        """
    <style>
    .project-management {
        background: linear-gradient(135deg, #313244 0%, #1e1e2e 100%);
        padding: 20px 25px;
        border-radius: 12px;
        border: 2px solid #a6e3a1;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(166, 227, 161, 0.15);
    }
    .project-management h3 {
        color: #a6e3a1 !important;
        font-size: 1.4rem !important;
        margin-bottom: 15px !important;
        padding-bottom: 10px;
        border-bottom: 1px solid #45475a;
    }
    /* Style selectbox and inputs in project section */
    .project-management .stSelectbox label,
    .project-management .stTextInput label {
        color: #cdd6f4 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    .project-management .stSelectbox > div > div,
    .project-management .stTextInput > div > div > input {
        background-color: #45475a !important;
        border: 1px solid #585b70 !important;
        color: #cdd6f4 !important;
    }
    .project-management .stButton > button {
        background-color: #a6e3a1 !important;
        color: #1e1e2e !important;
        font-weight: 600 !important;
        border: none !important;
    }
    .project-management .stButton > button:hover {
        background-color: #94e2d5 !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="project-management">', unsafe_allow_html=True)
        st.markdown("""
        <h2 style="
            font-size: 1.5rem;
            font-weight: 700;
            color: #a6e3a1;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #45475a;
        ">📁 Project Management</h2>
        """, unsafe_allow_html=True)

        # Initialize current project - check URL params first for persistence across refreshes
        available_projects = glm_system.project_manager.get_project_list()

        if "current_project" not in st.session_state:
            # Check URL query params for persisted project
            query_params = st.query_params
            url_project = query_params.get("project", "Default")
            if url_project in available_projects:
                st.session_state.current_project = url_project
            else:
                st.session_state.current_project = "Default"

        col1, col2, col3 = st.columns(3)

        with col1:
            available_projects = glm_system.project_manager.get_project_list()
            selected_project = st.selectbox(
                "📂 Current Project:",
                options=available_projects,
                index=(
                    available_projects.index(st.session_state.current_project)
                    if st.session_state.current_project in available_projects
                    else 0
                ),
                help="Organize your chats and work by project",
                key="project_selector",
            )

        with col2:
            # Initialize new project input key for clearing
            if "new_project_input" not in st.session_state:
                st.session_state.new_project_input = ""

            new_project = st.text_input(
                "➕ New Project:",
                placeholder="e.g., MyAudioApp",
                value=st.session_state.new_project_input,
                key="new_project_field"
            )
            if new_project and st.button("Create Project", key="create_proj"):
                success, message = glm_system.project_manager.create_project(
                    new_project
                )
                if success:
                    # Switch to the new project and clear input
                    st.session_state.current_project = new_project
                    st.session_state.new_project_input = ""
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

        with col3:
            if selected_project != "Default" and st.button(
                "🗑️ Delete", key="delete_proj"
            ):
                success, message = glm_system.project_manager.delete_project(
                    selected_project
                )
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

        # Handle project change
        if selected_project != st.session_state.current_project:
            handle_project_change(selected_project)
            # Update URL params for persistence across refreshes
            st.query_params["project"] = selected_project

        st.session_state.current_project = selected_project

        st.markdown("</div>", unsafe_allow_html=True)
        st.divider()
        return selected_project


def handle_project_change(new_project):
    """Handle project change with file management options"""
    # Check if there are open files
    open_files = st.session_state.get("editor_open_files", {})

    if open_files:
        # Check if any files have unsaved changes
        unsaved_files = []
        for file_path, file_data in open_files.items():
            if file_data.get("has_unsaved_changes") or file_data.get(
                "has_ai_suggestions"
            ):
                unsaved_files.append(Path(file_path).name)

        # Show file management dialog
        st.warning(f"🔄 **Switching to project: {new_project}**")

        if unsaved_files:
            st.error(f"⚠️ **You have {len(unsaved_files)} files with unsaved changes:**")
            for filename in unsaved_files:
                st.write(f"• {filename}")

        st.info(f"📁 **Currently open files:** {len(open_files)} files")

        # File management options
        st.subheader("🤔 What would you like to do with your open files?")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button(
                "💾 **Save All & Close**", key="save_all_close", type="primary"
            ):
                save_all_and_close_files()
                st.success("✅ All files saved and closed!")
                st.rerun()

        with col2:
            if st.button("🗙 **Close Without Saving**", key="close_all_no_save"):
                if unsaved_files:
                    # Show confirmation for unsaved changes
                    if "confirm_close_all" not in st.session_state:
                        st.session_state.confirm_close_all = False

                    if not st.session_state.confirm_close_all:
                        st.error("⚠️ **This will discard all unsaved changes!**")
                        if st.button(
                            "⚠️ **Confirm: Close Without Saving**",
                            key="confirm_close_all_btn",
                        ):
                            st.session_state.confirm_close_all = True
                            close_all_files()
                            st.success("🗙 All files closed without saving")
                            st.rerun()
                    else:
                        close_all_files()
                        st.success("🗙 All files closed")
                        st.rerun()
                else:
                    close_all_files()
                    st.success("🗙 All files closed")
                    st.rerun()

        with col3:
            if st.button("📌 **Keep Files Open**", key="keep_files_open"):
                st.info("📌 Files will remain open for reference across projects")
                # Just clear the confirmation state and continue
                if "confirm_close_all" in st.session_state:
                    del st.session_state.confirm_close_all
                st.rerun()

        # Add informational note
        st.caption(
            "💡 **Tip:** Keeping files open lets you reference code from other projects while working"
        )

        # Prevent further execution until user makes choice
        st.stop()


def save_all_and_close_files():
    """Save all open files and close them"""
    open_files = st.session_state.get("editor_open_files", {})

    for file_path, file_data in open_files.items():
        try:
            # Determine what content to save
            content_to_save = file_data.get("ai_suggested_content") or file_data.get(
                "current_content", ""
            )

            if content_to_save and (
                file_data.get("has_unsaved_changes")
                or file_data.get("has_ai_suggestions")
            ):
                # Save the file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content_to_save)
        except Exception as e:
            st.error(f"Error saving {Path(file_path).name}: {e}")

    # Clear all open files
    st.session_state.editor_open_files = {}

    # Clear confirmation states
    keys_to_clear = []
    for key in list(st.session_state.keys()):
        # Ensure key is a string before using startswith()
        if isinstance(key, str) and key.startswith("confirm_close"):
            keys_to_clear.append(key)

    for key in keys_to_clear:
        try:
            del st.session_state[key]
        except KeyError:
            pass  # Key might have been deleted already


def close_all_files():
    """Close all open files without saving"""
    # Clear all open files
    st.session_state.editor_open_files = {}

    # Clear all editor-related session state
    keys_to_clear = []
    for key in list(st.session_state.keys()):
        # Ensure key is a string before using startswith()
        if isinstance(key, str) and any(
            key.startswith(prefix)
            for prefix in ["editor_", "confirm_close", "ai_prompt_", "ai_model_"]
        ):
            keys_to_clear.append(key)

    for key in keys_to_clear:
        try:
            del st.session_state[key]
        except KeyError:
            pass  # Key might have been deleted already


# Keep all other functions the same...
def render_model_selection(glm_system):
    """Render model and agent mode selection"""
    st.markdown(
        """
    <style>
    .model-selection {
        background: linear-gradient(135deg, #313244 0%, #1e1e2e 100%);
        padding: 20px 25px;
        border-radius: 12px;
        border: 2px solid #fab387;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(250, 179, 135, 0.15);
    }
    .model-selection h3 {
        color: #fab387 !important;
        font-size: 1.4rem !important;
        margin-bottom: 15px !important;
    }
    .agent-mode-info {
        background-color: #45475a;
        padding: 10px;
        border-radius: 8px;
        margin-top: 10px;
        border-left: 3px solid #fab387;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="model-selection">', unsafe_allow_html=True)
        st.subheader("🤖 Model & Agent Selection")

        # Get URL params for persistence
        query_params = st.query_params
        model_options = list(glm_system.models.keys())
        agent_options = list(AGENT_MODES.keys())

        # Determine default model index from URL or session state
        url_model = query_params.get("model", "")
        default_model_idx = 0
        if url_model and url_model in model_options:
            default_model_idx = model_options.index(url_model)

        # Determine default agent index from URL or session state
        url_agent = query_params.get("agent", "General")
        default_agent_idx = 0
        if url_agent in agent_options:
            default_agent_idx = agent_options.index(url_agent)

        col1, col2, col3 = st.columns(3)

        with col1:
            selected_model = st.selectbox(
                "Choose Model",
                options=model_options,
                index=default_model_idx,
                help="DeepSeek for reasoning (slower but smarter), Qwen for quick tasks (faster)",
            )
            st.caption("🧠 **DeepSeek** - Complex tasks")
            st.caption("⚡ **Qwen** - Quick tasks")

            # Update URL if model changed
            if selected_model != url_model:
                st.query_params["model"] = selected_model

        with col2:
            # Agent mode selection
            agent_labels = [f"{AGENT_MODES[a]['icon']} {a}" for a in agent_options]

            selected_agent_idx = st.selectbox(
                "Specialist Mode",
                options=range(len(agent_options)),
                format_func=lambda x: agent_labels[x],
                index=default_agent_idx,
                help="Choose domain-specific expertise",
            )
            selected_agent = agent_options[selected_agent_idx]

            # Show agent description
            agent_info = AGENT_MODES[selected_agent]
            st.caption(f"*{agent_info['description']}*")

            # Update URL if agent changed
            if selected_agent != url_agent:
                st.query_params["agent"] = selected_agent

        with col3:
            use_context = st.checkbox(
                "📚 Use Knowledge Base",
                value=True,
                help="Include FAUST/JUCE documentation in responses",
            )

            # Store selected agent in session state for save filename
            st.session_state.selected_agent = selected_agent
            st.session_state.agent_file_prefix = agent_info['file_prefix']

        st.markdown('</div>', unsafe_allow_html=True)

        # Return values (cleaned up - no more HRM references)
        return selected_model, use_context, selected_agent


def render_sidebar(glm_system):
    """Render sidebar with system status only (KB management moved to Knowledge tab)"""
    with st.sidebar:
        # Model and system status only
        render_model_status(glm_system)


def render_file_upload_section(glm_system):
    """Render file upload and organization section"""
    st.subheader("📂 File Upload & Organization")

    subfolder_options = [
        "📁 Root (uploads/)",
        "🎵 FAUST",
        "💻 C++",
        "🐍 Python",
        "🎵 JUCE",
        "🔊 DSP",
        "📊 General",
        "🖼️ Images",
        "📝 Documentation",
        "🔧 Custom...",
    ]

    selected_subfolder = st.selectbox("Choose subfolder:", subfolder_options)

    # Handle custom subfolder
    target_subfolder = ""
    if selected_subfolder == "🔧 Custom...":
        custom_folder = st.text_input(
            "Enter custom folder name:", placeholder="e.g., my_project"
        )
        if custom_folder:
            target_subfolder = custom_folder.strip()
    elif selected_subfolder != "📁 Root (uploads/)":
        folder_mapping = {
            "🎵 FAUST": "faust",
            "💻 C++": "cpp",
            "🐍 Python": "python",
            "🎵 JUCE": "juce",
            "🔊 DSP": "dsp",
            "📊 General": "general",
            "🖼️ Images": "images",
            "📝 Documentation": "docs",
        }
        target_subfolder = folder_mapping.get(selected_subfolder, "")

    # File upload
    uploaded_files = st.file_uploader(
        "Upload Files",
        accept_multiple_files=True,
        type=[
            "pdf",
            "txt",
            "md",
            "py",
            "cpp",
            "h",
            "c",
            "hpp",
            "cc",
            "dsp",
            "lib",
            "jpg",
            "png",
            "bmp",
            "tiff",
        ],
        help=(
            f"Files will be saved to: uploads/{target_subfolder}"
            if target_subfolder
            else "Files will be saved to: uploads/"
        ),
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            if target_subfolder:
                upload_path = Path("./uploads") / target_subfolder / uploaded_file.name
            else:
                upload_path = Path("./uploads") / uploaded_file.name

            upload_path.parent.mkdir(parents=True, exist_ok=True)

            with open(upload_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner(f"Processing {uploaded_file.name}..."):
                result = glm_system.file_processor.process_file(str(upload_path))

            folder_display = f"{target_subfolder}/" if target_subfolder else "root/"
            st.success(f"✅ Saved to {folder_display} - {result}")


def render_bulk_operations(glm_system):
    """Render bulk operations section"""
    st.subheader("🔄 Bulk Operations")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 Scan All Subfolders"):
            with st.spinner("Scanning all subfolders..."):
                result = glm_system.file_processor.scan_uploads_recursive()
            st.success(result)

    with col2:
        if st.button("📊 Folder Stats"):
            stats = glm_system.file_processor.get_folder_stats()
            if stats:
                st.write("📂 **File counts by folder:**")
                for folder, count in stats.items():
                    emoji = {
                        "faust": "🎵",
                        "cpp": "💻",
                        "python": "🐍",
                        "juce": "🎵",
                        "dsp": "🔊",
                        "general": "📊",
                        "images": "🖼️",
                        "docs": "📝",
                        "root": "📁",
                    }.get(folder, "📁")
                    st.write(f"{emoji} {folder}: {count} files")
            else:
                st.info("No files found in uploads/")


def render_faust_docs_section(glm_system):
    """Render FAUST documentation section"""
    st.subheader("🎵 FAUST Documentation")
    if st.button("📥 Load FAUST Docs"):
        with st.spinner("Loading FAUST documentation..."):
            result = glm_system.file_processor.load_faust_documentation()
        st.success(result)

    if st.button("🌐 Download FAUST Docs"):
        st.info("Run: python download_faust_docs_complete.py in your project directory")


def render_model_status(glm_system):
    """Render model status section - simplified without HRM"""
    st.subheader("🔧 System Status")

    # Ollama Model Status
    st.write("**🤖 Models (via Ollama):**")
    for model_name, model_id in glm_system.models.items():
        try:
            if model_name in glm_system._model_instances:
                st.success(f"✅ {model_name} (in memory)")
            else:
                st.info(f"✅ {model_name} (ready)")
        except:
            st.error(f"❌ {model_name}")

    st.caption("💡 Models load into memory on first use")

    if st.button("🔍 Test Model Connection"):
        with st.spinner("Testing Ollama connection..."):
            status = glm_system.check_model_availability()
        for model_name, status_text in status.items():
            if "✅" in status_text:
                st.success(f"{status_text} {model_name}")
            elif "❌" in status_text:
                st.error(f"{status_text} {model_name}")
                st.code(f"ollama pull {glm_system.models[model_name]}")
            else:
                st.warning(f"{status_text} {model_name}")

    # Knowledge Base Status
    st.write("---")
    st.write("**📚 Knowledge Base:**")
    kb_status = glm_system.check_vectorstore_status()
    if kb_status["status"] == "✅ Ready":
        st.success(f"✅ {kb_status['document_count']} documents loaded")
    else:
        st.warning(kb_status["message"])


def render_chat_interface(glm_system, selected_model, use_context, selected_project, selected_agent="General"):
    """Render main chat interface with specialist agent modes"""
    agent_info = AGENT_MODES.get(selected_agent, AGENT_MODES["General"])
    st.header(f"{agent_info['icon']} Chat with {selected_model}")
    st.caption(f"Project: {selected_project} | Mode: **{selected_agent}**")

    # Project-based chat history
    chat_key = f"chat_history_{selected_model}_{selected_project}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = glm_system.project_manager.load_project_chats(
            selected_project, selected_model
        )

    # 1. CHAT INPUT FIRST (at the top)
    render_chat_input(
        glm_system, selected_model, use_context, selected_project, chat_key, selected_agent
    )

    # Add some spacing
    st.write("---")

    # 2. SUMMARIZATION TOOLS (uses Qwen for speed)
    render_summarization_tools(glm_system, st.session_state[chat_key], selected_project)

    st.write("---")

    # 3. AGENT CONTEXT (the meta file - above chat history)
    render_agent_context(glm_system, selected_project, selected_agent)

    # 4. RECENT CONVERSATIONS (below agent context)
    render_recent_conversations(st.session_state[chat_key], selected_model)

    # 5. FULL CHAT HISTORY (at the bottom)
    render_full_chat_history(st.session_state[chat_key], selected_model)


def render_summarization_tools(glm_system, chat_history, selected_project):
    """Render summarization tools using Qwen for speed"""
    if not chat_history:
        return

    st.subheader("⚡ Quick Tools (Qwen - Fast)")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📝 Generate Title", help="Use Qwen to generate a chat title"):
            with st.spinner("Generating title..."):
                # Get chat content
                chat_text = "\n".join([f"Q: {q}\nA: {a[:200]}" for q, a in chat_history[-3:]])
                title = glm_system.generate_title(chat_text)
                st.session_state.chat_title = title
                st.success(f"**Title:** {title}")

    with col2:
        if st.button("⚡ Quick Summary", help="Summarize current chat session"):
            with st.spinner("Summarizing..."):
                chat_text = "\n".join([f"Q: {q}\nA: {a}" for q, a in chat_history])
                summary = glm_system.quick_summarize(chat_text, max_words=100)
                st.info(f"**Summary:** {summary}")

    with col3:
        if st.button("📤 Export Summary for Claude", help="Create context summary for Claude"):
            with st.spinner("Creating context summary..."):
                chat_text = "\n".join([f"Q: {q}\nA: {a}" for q, a in chat_history])
                summary = glm_system.quick_summarize(chat_text, max_words=200)

                formatted = f"""## Context from DeepSeek Session
Project: {selected_project}

### Summary
{summary}

---
Please continue with this context and implement the discussed approach."""

                st.code(formatted, language="markdown")
                st.info("Copy above and paste into Claude Code")

    # Show current title if set
    if "chat_title" in st.session_state and st.session_state.chat_title:
        st.caption(f"📌 Current Title: **{st.session_state.chat_title}**")


def render_chat_input(
    glm_system, selected_model, use_context, selected_project, chat_key, selected_agent="General"
):
    """Render chat input section with specialist agent mode"""
    # Add styling for the input section
    st.markdown(
        """
    <style>
    .chat-input-section {
        background: linear-gradient(135deg, #313244 0%, #1e1e2e 100%);
        padding: 20px 25px;
        border-radius: 12px;
        border: 2px solid #89b4fa;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(137, 180, 250, 0.15);
    }
    .chat-input-section h3 {
        color: #89b4fa !important;
        font-size: 1.4rem !important;
        margin-bottom: 15px !important;
        padding-bottom: 10px;
        border-bottom: 1px solid #45475a;
    }
    .chat-input-section .stTextArea label {
        color: #cdd6f4 !important;
        font-weight: 600 !important;
    }
    .chat-input-section .stButton > button {
        background-color: #89b4fa !important;
        color: #1e1e2e !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 10px 25px !important;
    }
    .chat-input-section .stButton > button:hover {
        background-color: #b4befe !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="chat-input-section">', unsafe_allow_html=True)
        st.subheader("💬 Ask Your Question")

        # Show context status
        col1, col2, col3 = st.columns(3)

        with col1:
            # Knowledge base status
            kb_status = glm_system.check_vectorstore_status()
            if kb_status["status"] == "✅ Ready":
                st.success(f"📚 KB: {kb_status['document_count']} docs")
            elif kb_status["status"] == "⚠️ Empty":
                st.warning("📚 KB: Empty")
            else:
                st.error("📚 KB: Error")

        with col2:
            # Chat history status
            current_history = st.session_state.get(chat_key, [])
            if len(current_history) > 0:
                st.info(f"💬 History: {len(current_history)} exchanges")
            else:
                st.info("💬 History: New conversation")

        with col3:
            # Context toggle status
            if use_context:
                st.success("🧠 Context: ON")
            else:
                st.warning("🧠 Context: OFF")

        # Handle clear input flag
        default_value = ""
        if st.session_state.get("clear_chat_input", False):
            st.session_state.clear_chat_input = False  # Reset flag
            default_value = ""
        else:
            default_value = st.session_state.get("main_chat_input", "")

        question = st.text_area(
            "Type your question or request:",
            value=default_value,
            placeholder="""Examples:
        - Create a reverb effect in FAUST
        - Explain the uploaded C++ code
        - Design a low-pass filter
        - Help me debug this Python script
        - Continue our discussion about [previous topic]

        Press Enter for new lines, use the Send button when ready.""",
            key="main_chat_input",
            height=350,
            help="Multi-line input supported - great for code snippets and detailed questions!",
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            send_button = st.button(
                "🚀 Send", type="primary", disabled=not question.strip()
            )

        with col2:
            if st.button("🗑️ Clear Input"):
                # Clear the text area by deleting its session state key
                if "main_chat_input" in st.session_state:
                    del st.session_state["main_chat_input"]
                st.rerun()

        with col3:
            if question.strip():
                st.success(f"✅ Ready to send ({len(question)} characters)")
            else:
                st.info("💡 Type your question above")

        # Additional controls
        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "🔄 New Conversation", help="Start fresh without clearing history"
            ):
                st.session_state.main_chat_input = ""
                st.success("Ready for a new conversation!")

        with col2:
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🔄 Reload History"):
                    # Reload history from file
                    st.session_state[chat_key] = glm_system.project_manager.load_project_chats(
                        selected_project, selected_model
                    )
                    st.success(f"Reloaded {len(st.session_state[chat_key])} conversations")
                    st.rerun()
            with col_b:
                if st.button("🗑️ Clear History"):
                    st.session_state[chat_key] = []
                    st.success("Chat history cleared!")
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # Handle send button
        if send_button and question:
            # Get current chat history
            current_history = st.session_state.get(chat_key, [])

            with st.spinner(f"🧠 {selected_model} is thinking..."):
                # Show what context is being used
                with st.expander("🔍 Context Details", expanded=False):
                    st.write(f"**Using Context:** {'Yes' if use_context else 'No'}")
                    st.write(f"**Chat History Length:** {len(current_history)} exchanges")

                    if use_context:
                        kb_status = glm_system.check_vectorstore_status()
                        st.write(f"**Knowledge Base:** {kb_status['message']}")

                # Call model with agent mode
                response_data = glm_system.generate_response(
                    prompt=question,
                    selected_model=selected_model,
                    use_context=use_context,
                    project_name=selected_project,
                    chat_history=current_history,
                    agent_mode=selected_agent,
                )

                response = response_data["response"]
                routing_info = response_data.get("routing", {})

            # Add to chat history
            st.session_state[chat_key].append((question, response))

            # Display model used
            actual_model = routing_info.get('selected_model', selected_model)
            st.success(f"✅ Response from {actual_model}")

            # Save to project file
            glm_system.project_manager.save_chat_to_project(
                selected_project, actual_model, question, response
            )

            st.rerun()


def render_agent_context(glm_system, project_name: str, agent_mode: str):
    """Render agent context meta file with view/edit capability.

    Shows the current agent's summarized context above chat history.
    Users can view, edit, and save the context manually.
    """
    # Don't show for Default project
    if project_name == "Default":
        return

    agent_meta = glm_system.read_agent_meta(project_name, agent_mode)

    # Add styling for the agent context box (blue/purple theme to distinguish from green project box)
    st.markdown(
        """
    <style>
    .agent-context {
        background: linear-gradient(135deg, #313244 0%, #1e1e2e 100%);
        padding: 20px 25px;
        border-radius: 12px;
        border: 2px solid #89b4fa;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(137, 180, 250, 0.15);
    }
    .agent-context h3 {
        color: #89b4fa !important;
        font-size: 1.4rem !important;
        margin-bottom: 15px !important;
        padding-bottom: 10px;
        border-bottom: 1px solid #45475a;
    }
    .agent-context .stTextArea label {
        color: #cdd6f4 !important;
        font-weight: 600 !important;
    }
    .agent-context .stTextArea textarea {
        background-color: #45475a !important;
        border: 1px solid #585b70 !important;
        color: #cdd6f4 !important;
        font-family: monospace !important;
    }
    .agent-context .stButton > button {
        background-color: #89b4fa !important;
        color: #1e1e2e !important;
        font-weight: 600 !important;
        border: none !important;
    }
    .agent-context .stButton > button:hover {
        background-color: #b4befe !important;
    }
    .agent-context .stMarkdown {
        color: #cdd6f4 !important;
    }
    .agent-context-content {
        background-color: #45475a;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-family: monospace;
        white-space: pre-wrap;
        max-height: 400px;
        overflow-y: auto;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Unique key for this agent's editor state
    editing_key = f"meta_editing_{project_name}_{agent_mode}"

    # Header with agent info
    agent_config = AGENT_MODES.get(agent_mode, AGENT_MODES["General"])
    icon = agent_config.get("icon", "🤖")

    with st.container():
        st.markdown('<div class="agent-context">', unsafe_allow_html=True)
        st.markdown(f"### {icon} {agent_mode} Agent Context")

        if agent_meta:
            # Show word count
            word_count = len(agent_meta.split())
            st.caption(f"📊 {word_count} words | Auto-updated by Qwen after each exchange")

            # Check if we're in edit mode
            if st.session_state.get(editing_key, False):
                # Edit mode - show text area
                edited_content = st.text_area(
                    "Edit context:",
                    value=agent_meta,
                    height=400,
                    key=f"meta_edit_{project_name}_{agent_mode}",
                )

                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    if st.button("💾 Save", key=f"save_meta_{project_name}_{agent_mode}"):
                        if glm_system.save_agent_meta(project_name, agent_mode, edited_content):
                            st.success("✅ Context saved!")
                            st.session_state[editing_key] = False
                            st.rerun()
                        else:
                            st.error("❌ Failed to save")

                with col2:
                    if st.button("❌ Cancel", key=f"cancel_meta_{project_name}_{agent_mode}"):
                        st.session_state[editing_key] = False
                        st.rerun()
            else:
                # View mode - show content in styled div
                st.markdown(
                    f'<div class="agent-context-content">{agent_meta}</div>',
                    unsafe_allow_html=True
                )

                col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
                with col1:
                    if st.button("✏️ Edit", key=f"edit_meta_{project_name}_{agent_mode}"):
                        st.session_state[editing_key] = True
                        st.rerun()

                with col2:
                    if st.button("✨ Suggest", key=f"suggest_meta_{project_name}_{agent_mode}",
                                 help="Generate improved context using PROJECT_META.md + recent chat"):
                        suggestion_key = f"agent_suggestion_{project_name}_{agent_mode}"
                        with st.spinner("Generating suggestion..."):
                            suggestion = generate_agent_context_suggestion(
                                glm_system, project_name, agent_mode
                            )
                            if suggestion:
                                st.session_state[suggestion_key] = suggestion
                                st.rerun()
                            else:
                                st.warning("Could not generate suggestion")

                with col3:
                    if st.button("🗑️ Clear", key=f"clear_meta_{project_name}_{agent_mode}"):
                        if glm_system.clear_agent_meta(project_name, agent_mode):
                            st.success("✅ Context cleared!")
                            st.rerun()

                # Check if there's a pending suggestion
                suggestion_key = f"agent_suggestion_{project_name}_{agent_mode}"
                if st.session_state.get(suggestion_key):
                    render_agent_suggestion_approval(glm_system, project_name, agent_mode, suggestion_key)

        else:
            st.info(f"💡 No context yet for {agent_mode} agent. It will be created after your first exchange.")
            # Still offer Suggest button even when no context exists
            if st.button("✨ Generate Initial Context", key=f"init_suggest_{project_name}_{agent_mode}",
                         help="Generate initial context from PROJECT_META.md"):
                suggestion_key = f"agent_suggestion_{project_name}_{agent_mode}"
                with st.spinner("Generating initial context..."):
                    suggestion = generate_agent_context_suggestion(
                        glm_system, project_name, agent_mode
                    )
                    if suggestion:
                        st.session_state[suggestion_key] = suggestion
                        st.rerun()

            # Check for pending suggestion
            suggestion_key = f"agent_suggestion_{project_name}_{agent_mode}"
            if st.session_state.get(suggestion_key):
                render_agent_suggestion_approval(glm_system, project_name, agent_mode, suggestion_key)

        st.markdown('</div>', unsafe_allow_html=True)


def render_recent_conversations(chat_history, selected_model):
    """Render recent conversations section with export buttons"""
    # Display recent chat (last 5 exchanges) - collapsible
    recent_chats = chat_history[-5:]  # Show last 5 exchanges

    if recent_chats:
        st.subheader("💬 Recent Conversations")

        for i, (question, answer) in enumerate(reversed(recent_chats), 1):
            # Create preview text for collapsed state
            question_preview = question.replace("\n", " ")[:80] + (
                "..." if len(question) > 80 else ""
            )

            # Detect content type for better icons
            if "```" in answer:
                content_icon = "💻"  # Code
            elif any(
                keyword in answer.lower()
                for keyword in ["faust", "dsp", "audio", "signal"]
            ):
                content_icon = "🎵"  # Audio/DSP
            elif len(answer) > 500:
                content_icon = "📄"  # Long text
            else:
                content_icon = "💡"  # General

            # Create expandable container for each chat
            with st.expander(
                f"{content_icon} Q{len(recent_chats) - i + 1}: {question_preview}",
                expanded=i <= 2,  # Keep last 2 exchanges expanded by default
            ):
                # Question section
                st.markdown("**🙋 Your Question:**")
                # Detect language for syntax highlighting
                question_lang = get_code_language_from_content(question)
                st.code(question, language=question_lang)

                # Answer section - use helper to show R1 thinking if present
                display_response_with_thinking(answer, selected_model)

                # Export buttons section
                st.markdown("---")
                st.markdown("**📤 Export Options:**")
                col1, col2, col3 = st.columns(3)

                msg_id = len(recent_chats) - i + 1

                with col1:
                    if st.button("📋 Copy Response", key=f"copy_{msg_id}"):
                        st.session_state.clipboard_content = answer
                        st.success("✓ Copied! Paste into Claude Code")

                with col2:
                    if st.button("💾 Save to Project", key=f"save_{msg_id}"):
                        from datetime import datetime
                        from pathlib import Path

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        project = st.session_state.get("current_project", "Default")
                        agent_prefix = st.session_state.get("agent_file_prefix", "general")
                        agent_name = st.session_state.get("selected_agent", "General")

                        save_dir = Path(f"./projects/{project}/reasoning")
                        save_dir.mkdir(parents=True, exist_ok=True)

                        # Include agent mode in filename for easy distinction
                        save_path = save_dir / f"{agent_prefix}_{timestamp}.md"

                        content = f"""# {agent_name} Specialist Session
Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}
Project: {project}
Model: {selected_model}
Agent Mode: {agent_name}

## Query
{question}

## Response
{answer}

---
*Export this to Claude Code for implementation*
"""
                        save_path.write_text(content)
                        st.success(f"✓ Saved to {save_path.name}")

                with col3:
                    if st.button("📤 Format for Claude", key=f"format_{msg_id}"):
                        formatted = f"""Based on this reasoning from DeepSeek:

{answer}

---
Please implement the above approach."""
                        st.code(formatted, language="markdown")
                        st.info("Copy above and paste into Claude Code")

                # Add metadata footer
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption(f"📝 Q: {len(question)} chars")
                with col2:
                    st.caption(f"📋 A: {len(answer)} chars")
                with col3:
                    # Detect content type
                    if "```" in answer:
                        st.caption("💻 Contains Code")
                    elif any(
                        keyword in answer.lower()
                        for keyword in ["faust", "dsp", "audio"]
                    ):
                        st.caption("🎵 Audio/DSP")
                    else:
                        st.caption("💬 Text")

            # Add spacing between exchanges
            if i < len(recent_chats):
                st.write("")
    else:
        st.info(
            "💡 No recent conversations. Start chatting to see your exchanges here!"
        )


def render_full_chat_history(chat_history, selected_model):
    """Render full chat history section"""
    if chat_history:
        total_messages = len(chat_history)
        with st.expander(
            f"📜 Complete Chat History ({total_messages} conversations)",
            expanded=False,
        ):
            # Show last 10 conversations in reverse order (newest first)
            for i, (question, answer) in enumerate(reversed(chat_history[-10:]), 1):
                question_preview = question.replace("\n", " ")[:100] + (
                    "..." if len(question) > 100 else ""
                )

                with st.expander(
                    f"🔹 Conversation {total_messages - i + 1}: {question_preview}",
                    expanded=False,
                ):
                    col1, col2 = st.columns([1, 3])

                    with col1:
                        st.write("**Question:**")
                    with col2:
                        question_lang = get_code_language_from_content(question)
                        st.code(question, language=question_lang)

                    # Answer section - use helper to show R1 thinking if present
                    st.write("**Answer:**")
                    display_response_with_thinking(answer, selected_model)

                    # Show token/character count
                    st.caption(f"📊 Q: {len(question)} chars | A: {len(answer)} chars")

                if i < 10 and i < total_messages:  # Don't add divider after last item
                    st.write("---")


