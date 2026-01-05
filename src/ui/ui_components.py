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

        # Get recent chat history for this agent (handle both 2-tuple and 3-tuple formats)
        chat_key = f"chat_history_{project_name}"
        chat_history = st.session_state.get(chat_key, [])
        recent_exchanges = chat_history[-5:] if chat_history else []
        chat_summary = ""
        if recent_exchanges:
            chat_summary = "\n\n".join([
                f"Q: {entry[0][:200]}...\nA: {entry[1][:300]}..."
                for entry in recent_exchanges
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

        # Use fast model for generation
        fast_model = glm_system.get_fast_model_name()
        llm = glm_system.get_model_instance(fast_model)
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


def _read_file_for_attachment(file_path: str, project_path: Optional[Path]) -> Optional[str]:
    """Read a file for attachment to chat context."""
    try:
        # Try as absolute path first
        path = Path(file_path)
        if path.is_absolute() and path.exists():
            return path.read_text(encoding='utf-8', errors='replace')

        # Try relative to project
        if project_path:
            relative_path = project_path / file_path
            if relative_path.exists():
                return relative_path.read_text(encoding='utf-8', errors='replace')

        # Try relative to current working directory
        cwd_path = Path.cwd() / file_path
        if cwd_path.exists():
            return cwd_path.read_text(encoding='utf-8', errors='replace')

        return None
    except Exception as e:
        print(f"Error reading file for attachment: {e}")
        return None


def _render_file_browser_popup(glm_system, selected_project: str, attached_file_key: str):
    """Render an improved file browser for selecting files to attach."""
    st.markdown("---")

    # Supported file extensions
    CODE_EXTENSIONS = {
        '.py', '.js', '.ts', '.tsx', '.jsx', '.cpp', '.c', '.h', '.hpp', '.java',
        '.rs', '.go', '.rb', '.php', '.swift', '.kt', '.scala', '.dsp', '.faust',
        '.md', '.txt', '.json', '.yaml', '.yml', '.toml', '.xml', '.html', '.css',
        '.scss', '.sql', '.sh', '.bash', '.zsh', '.cmake', '.make', '.gradle'
    }

    # Get/set browse directory - use a global key not tied to project for navigation
    browse_dir_key = "file_browser_current_dir"
    project_path = glm_system.project_manager.get_project_path(selected_project)
    default_path = str(project_path) if project_path else str(Path.cwd())

    # Initialize only if not set
    if browse_dir_key not in st.session_state:
        st.session_state[browse_dir_key] = default_path

    browse_path = Path(st.session_state[browse_dir_key])

    # Header with current path (shows actual value from session state)
    st.markdown(f"**📂 File Browser**")
    st.info(f"📍 Current: {st.session_state[browse_dir_key]}")

    # Navigation buttons
    col_up, col_home, col_project = st.columns(3)

    with col_up:
        if st.button("⬆️ Parent", key="nav_up_btn", use_container_width=True):
            parent = browse_path.parent
            if parent.exists():
                st.session_state[browse_dir_key] = str(parent)
                st.rerun()

    with col_home:
        if st.button("🏠 Home", key="nav_home_btn", use_container_width=True):
            st.session_state[browse_dir_key] = str(Path.home())
            st.rerun()

    with col_project:
        if st.button("📁 Project", key="nav_project_btn", use_container_width=True):
            st.session_state[browse_dir_key] = default_path
            st.rerun()

    # Manual path input
    col_input, col_go = st.columns([4, 1])
    with col_input:
        manual_path = st.text_input(
            "Go to path:",
            value="",
            placeholder=str(browse_path),
            key="manual_path_input",
            label_visibility="collapsed"
        )
    with col_go:
        if st.button("Go", key="go_path_btn", use_container_width=True):
            if manual_path and Path(manual_path).exists():
                st.session_state[browse_dir_key] = manual_path
                st.session_state["manual_path_input"] = ""
                st.rerun()

    st.markdown("---")

    # List directory contents
    if browse_path.exists() and browse_path.is_dir():
        try:
            # Separate directories and files
            dirs = []
            files = []

            for item in sorted(browse_path.iterdir(), key=lambda x: x.name.lower()):
                if item.name.startswith('.'):
                    continue
                if item.is_dir():
                    dirs.append(item)
                elif item.suffix.lower() in CODE_EXTENSIONS:
                    # Get file size
                    try:
                        size = item.stat().st_size
                        if size < 1024:
                            size_str = f"{size} B"
                        elif size < 1024 * 1024:
                            size_str = f"{size // 1024} KB"
                        else:
                            size_str = f"{size // (1024 * 1024)} MB"
                    except:
                        size_str = "?"
                    files.append((item, size_str))

            # Generate unique key base from current path to avoid key conflicts
            path_id = abs(hash(str(browse_path))) % 1000000

            # Show directories first (in scrollable container)
            if dirs:
                st.markdown(f"**Folders:** ({len(dirs)})")
                dir_cols = st.columns(3)
                for i, d in enumerate(dirs):
                    with dir_cols[i % 3]:
                        if st.button(f"📁 {d.name}", key=f"d{i}_{path_id}", use_container_width=True):
                            st.session_state[browse_dir_key] = str(d)
                            st.rerun()

            # Show files (no limit - page scrolls naturally)
            if files:
                st.markdown(f"**Files:** ({len(files)})")
                for i, (f, size_str) in enumerate(files):
                    col_name, col_size, col_btn = st.columns([3, 1, 1])
                    with col_name:
                        st.text(f"📄 {f.name}")
                    with col_size:
                        st.caption(size_str)
                    with col_btn:
                        if st.button("Select", key=f"f{i}_{path_id}"):
                            # Read file content and attach
                            content = _read_file_for_attachment(str(f), None)
                            if content:
                                st.session_state[attached_file_key] = str(f)
                                st.session_state[f"attached_content_{selected_project}"] = content
                            st.session_state[f"show_file_browser_{selected_project}"] = False
                            st.rerun()

            if not dirs and not files:
                st.info("No supported files in this directory")

        except PermissionError:
            st.error("❌ Permission denied")
    else:
        st.warning("⚠️ Directory not found")

    st.markdown("---")
    if st.button("❌ Close Browser", key="close_browser_btn", use_container_width=True):
        st.session_state[f"show_file_browser_{selected_project}"] = False
        st.rerun()


def get_code_language_from_content(content: str) -> Optional[str]:
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
    from src.ui.theme import get_project_management_css
    st.markdown(get_project_management_css(), unsafe_allow_html=True)

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
            import urllib.parse
            query_params = st.query_params
            url_project_raw = query_params.get("project", "Default")
            # URL decode the project name (+ becomes space, %20 becomes space, etc.)
            url_project = urllib.parse.unquote_plus(url_project_raw)
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
    # Clear file from URL
    _clear_file_from_url()

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


def _clear_file_from_url():
    """Clear the file param from URL."""
    try:
        if "file" in st.query_params:
            del st.query_params["file"]
    except Exception:
        pass


def close_all_files():
    """Close all open files without saving"""
    # Clear all open files
    st.session_state.editor_open_files = {}
    _clear_file_from_url()

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
    from src.ui.theme import get_model_selection_css
    st.markdown(get_model_selection_css(), unsafe_allow_html=True)

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
                help="Reasoning model for complex tasks (slower), Fast model for quick tasks (faster)",
            )
            st.caption("🧠 **Reasoning** - Complex tasks")
            st.caption("⚡ **Fast** - Quick tasks")

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

    if st.button("📖 Load FAUST Libraries", help="Load .lib files directly from faustlibraries submodule"):
        with st.spinner("Loading FAUST libraries..."):
            result = glm_system.file_processor.load_faust_libraries()
        st.success(result)

    st.caption("Source: faust_documentation/faustlibraries/ (git submodule)")


def _expand_faust_query(query: str) -> str:
    """Expand search query with FAUST library aliases for better matching."""
    # Map common terms to library prefixes
    LIBRARY_ALIASES = {
        "wave digital": "wd. wdmodels wave digital filter",
        "analyzer": "an. analyzers",
        "basic": "ba. basics",
        "compressor": "co. compressors",
        "delay": "de. delays",
        "demo": "dm. demos",
        "dx7": "dx. dx7",
        "envelope": "en. envelopes adsr asr",
        "filter": "fi. filters lowpass highpass bandpass",
        "fds": "fd. finite difference schemes",
        "miscellaneous": "mi. mi. misceffects",
        "effects": "ef. misceffects",
        "noise": "no. noises",
        "oscillator": "os. oscillators",
        "phaflangers": "pf. phaflangers",
        "physical model": "pm. physmodels",
        "quantize": "qu. quantizers",
        "reverb": "re. reverbs",
        "route": "ro. routes",
        "signal": "si. signals",
        "soundfile": "sf. soundfiles",
        "synth": "sp. spat sy. synths",
        "spatial": "sp. spat",
        "interpolation": "it. interpolators",
        "vaeffect": "ve. vaeffects moog",
        "virtual analog": "ve. vaeffects",
        "version": "vl. version",
        "wah": "wa. webaudio",
    }

    expanded = query.lower()
    additions = []

    for term, aliases in LIBRARY_ALIASES.items():
        if term in expanded:
            additions.append(aliases)

    if additions:
        return f"{query} {' '.join(additions)}"
    return query


def render_knowledge_search(glm_system):
    """Render knowledge base search interface with AI-powered search"""
    st.subheader("🔍 Search Knowledge Base")

    # Search input
    search_query = st.text_input(
        "Search query",
        placeholder="e.g., wave digital filter, adsr envelope, moog filter...",
        key="kb_search_query"
    )

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        num_results = st.selectbox("Results", [5, 10, 20], index=0, key="kb_num_results")
    with col2:
        use_ai = st.checkbox("🤖 AI Search", value=True, help="Use AI to understand intent and filter by library")
    with col3:
        search_clicked = st.button("🔍 Search", key="kb_search_btn")

    if search_clicked and search_query.strip():
        with st.spinner(f"Searching for '{search_query}'..."):
            try:
                filter_dict = None
                search_terms = search_query

                # AI-powered search: use fast model to identify relevant library
                if use_ai:
                    fast_model = glm_system.get_fast_model_name()
                    llm = glm_system.get_model_instance(fast_model)

                    if llm:
                        # Ask AI to identify the library prefix
                        ai_prompt = f"""Identify the FAUST library prefix for this query. Return ONLY the 2-letter prefix.

FAUST libraries:
- wd: wave digital filters (resistor, capacitor, inductor, diode, buildtree)
- an: analyzers (rms, peak, amp_follower)
- ba: basics (if, select, beat)
- co: compressors (limiter, compressor)
- de: delays (delay, fdelay)
- en: envelopes (adsr, asr, ar)
- fi: filters (lowpass, highpass, bandpass, resonlp)
- ef: effects (echo, flanger, chorus)
- no: noises (noise, pink_noise)
- os: oscillators (osc, saw, square, triangle)
- pm: physical models (waveguide, chain)
- re: reverbs (freeverb, jcrev)
- ve: virtual analog (moog_vcf, oberheim)
- sy: synths (dubDub, fm)

Query: {search_query}

Return ONLY the 2-letter prefix (e.g., "wd" or "fi"), nothing else:"""

                        response = llm.invoke(ai_prompt).strip().lower()
                        # Extract just the prefix
                        prefix = response[:2] if len(response) >= 2 else None

                        if prefix and prefix.isalpha():
                            filter_dict = {"library": prefix}
                            st.caption(f"🤖 AI detected library: **{prefix}**")

                # Search with optional filter
                if filter_dict:
                    results = glm_system.vectorstore.similarity_search(
                        search_query,
                        k=num_results,
                        filter=filter_dict
                    )
                else:
                    results = glm_system.vectorstore.similarity_search(search_query, k=num_results)

                if results:
                    st.success(f"Found {len(results)} results")

                    for i, doc in enumerate(results):
                        source = doc.metadata.get("source", "unknown")
                        func = doc.metadata.get("function", "")
                        lib = doc.metadata.get("library", "")

                        # Create header
                        if func:
                            header = f"**{i+1}. {func}** ({lib})"
                        else:
                            header = f"**{i+1}. {source.split('/')[-1]}**"

                        with st.expander(header, expanded=(i == 0)):
                            # Show metadata
                            st.caption(f"Source: {source}")
                            if doc.metadata:
                                meta_str = " | ".join([f"{k}: {v}" for k, v in doc.metadata.items() if k != "source"])
                                if meta_str:
                                    st.caption(meta_str)

                            # Show content
                            content = doc.page_content
                            if len(content) > 1500:
                                st.markdown(content[:1500] + "...")
                            else:
                                st.markdown(content)
                else:
                    st.warning("No results found. Try different keywords or disable AI filter.")

            except Exception as e:
                st.error(f"Search error: {e}")

    elif search_clicked:
        st.warning("Enter a search query")

    # Show database stats and management
    with st.expander("📊 Database Stats & Management"):
        kb_status = glm_system.check_vectorstore_status()
        st.write(f"**Documents:** {kb_status.get('document_count', 0)}")
        st.write(f"**Status:** {kb_status.get('status', 'Unknown')}")
        if kb_status.get('test_count', 0) > 0:
            st.caption(f"({kb_status['test_count']} test documents excluded)")

        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Database", help="Delete all documents from ChromaDB"):
                try:
                    import shutil
                    from pathlib import Path
                    db_path = Path("chroma_db")
                    if db_path.exists():
                        shutil.rmtree(db_path)
                        st.success("✅ Database cleared. Restart app to reinitialize.")
                        st.info("Then click 'Load FAUST Libraries' to reload.")
                    else:
                        st.info("Database already empty")
                except Exception as e:
                    st.error(f"Error: {e}")

        with col2:
            if st.button("🔄 Show Sources", help="List unique document sources"):
                try:
                    collection = glm_system.vectorstore._collection
                    docs = collection.get(limit=100, include=['metadatas'])
                    sources = {}
                    for meta in docs['metadatas']:
                        src = meta.get('source', 'unknown')
                        # Shorten path
                        short = src.split('/')[-1] if '/' in src else src
                        sources[short] = sources.get(short, 0) + 1

                    if sources:
                        st.write("**Sources:**")
                        for src, count in sorted(sources.items(), key=lambda x: -x[1])[:10]:
                            st.caption(f"- {src}: {count} chunks")
                    else:
                        st.info("No documents found")
                except Exception as e:
                    st.error(f"Error: {e}")


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
    """Render summarization tools using fast model for speed"""
    if not chat_history:
        return

    st.subheader("⚡ Quick Tools (Fast Model)")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📝 Generate Title", help="Use fast model to generate a chat title"):
            with st.spinner("Generating title..."):
                # Get chat content (handle both 2-tuple and 3-tuple formats)
                chat_text = "\n".join([f"Q: {entry[0]}\nA: {entry[1][:200]}" for entry in chat_history[-3:]])
                title = glm_system.generate_title(chat_text)
                st.session_state.chat_title = title
                st.success(f"**Title:** {title}")

    with col2:
        if st.button("⚡ Quick Summary", help="Summarize current chat session"):
            with st.spinner("Summarizing..."):
                chat_text = "\n".join([f"Q: {entry[0]}\nA: {entry[1]}" for entry in chat_history])
                summary = glm_system.quick_summarize(chat_text, max_words=100)
                st.session_state.quick_summary_result = summary

    with col3:
        if st.button("📤 Export for Claude", help="Create context summary for Claude"):
            with st.spinner("Creating context summary..."):
                chat_text = "\n".join([f"Q: {entry[0]}\nA: {entry[1]}" for entry in chat_history])
                summary = glm_system.quick_summarize(chat_text, max_words=200)
                st.session_state.export_summary_result = f"""## Context from Reasoning Session
Project: {selected_project}

### Summary
{summary}

---
Please continue with this context and implement the discussed approach."""

    # Show current title if set
    if "chat_title" in st.session_state and st.session_state.chat_title:
        st.caption(f"📌 Current Title: **{st.session_state.chat_title}**")

    # Show quick summary result (full width)
    if st.session_state.get("quick_summary_result"):
        st.info(f"**Summary:** {st.session_state.quick_summary_result}")
        if st.button("✖️ Clear Summary", key="clear_quick_summary"):
            st.session_state.quick_summary_result = None
            st.rerun()

    # Show export summary result (full width, easier to read and copy)
    if st.session_state.get("export_summary_result"):
        st.markdown("**📤 Export for Claude Code:**")
        st.code(st.session_state.export_summary_result, language="markdown")
        st.caption("Copy above and paste into Claude Code")
        if st.button("✖️ Clear Export", key="clear_export_summary"):
            st.session_state.export_summary_result = None
            st.rerun()


def render_chat_input(
    glm_system, selected_model, use_context, selected_project, chat_key, selected_agent="General"
):
    """Render chat input section with specialist agent mode"""
    from src.ui.theme import get_chat_input_css
    st.markdown(get_chat_input_css(), unsafe_allow_html=True)

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

        # File attachment section
        attached_file_key = f"attached_file_{selected_project}"
        attached_content_key = f"attached_content_{selected_project}"
        show_browser_key = f"show_file_browser_{selected_project}"

        # Keep expander open if file attached OR browser is open
        expander_open = bool(st.session_state.get(attached_file_key)) or st.session_state.get(show_browser_key, False)

        with st.expander("📎 Attach File", expanded=expander_open):
            st.caption("Attach a file from your project for the model to read")

            # Get project path for file browsing
            project_path = glm_system.project_manager.get_project_path(selected_project)

            col_path, col_browse = st.columns([3, 1])

            with col_path:
                file_path_input = st.text_input(
                    "File path:",
                    value=st.session_state.get(attached_file_key, ""),
                    placeholder="e.g., src/main.py or paste full path",
                    key=f"file_path_input_{selected_project}",
                    help="Enter relative path from project or absolute path"
                )

            with col_browse:
                st.write("")  # Spacing
                if st.button("📂 Browse", key=f"browse_file_{selected_project}"):
                    st.session_state[show_browser_key] = True
                    st.rerun()

            # Simple file browser
            if st.session_state.get(show_browser_key):
                _render_file_browser_popup(glm_system, selected_project, attached_file_key)

            # Attach/Clear buttons
            col_attach, col_clear, col_status = st.columns([1, 1, 2])

            with col_attach:
                if st.button("📎 Attach", key=f"attach_btn_{selected_project}"):
                    if file_path_input:
                        content = _read_file_for_attachment(file_path_input, project_path)
                        if content:
                            st.session_state[attached_file_key] = file_path_input
                            st.session_state[attached_content_key] = content
                            st.success(f"✅ Attached!")
                            st.rerun()
                        else:
                            st.error("❌ Could not read file")

            with col_clear:
                if st.button("🗑️ Clear", key=f"clear_attach_{selected_project}"):
                    st.session_state[attached_file_key] = ""
                    st.session_state[attached_content_key] = ""
                    st.rerun()

            with col_status:
                if st.session_state.get(attached_content_key):
                    content = st.session_state[attached_content_key]
                    lines = content.count('\n') + 1
                    st.success(f"📄 {lines} lines attached")

            # Show attached file name and preview
            if st.session_state.get(attached_file_key):
                file_path = st.session_state[attached_file_key]
                file_name = Path(file_path).name
                st.info(f"📎 **{file_name}**")
                st.caption(f"Full path: {file_path}")

            if st.session_state.get(attached_content_key):
                with st.expander("Preview attached content", expanded=False):
                    # Full content in scrollable container (auto-detect syntax)
                    with st.container(height=400):
                        st.code(st.session_state[attached_content_key])

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
            placeholder="Examples: Create a reverb in FAUST, Explain this C++ code, Design a low-pass filter...",
            key="main_chat_input",
            height=350,
            help="Multi-line input supported. Press Enter for new lines, use the Send button when ready.",
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

            # Build prompt with attached file if present
            final_prompt = question
            attached_content = st.session_state.get(attached_content_key, "")
            attached_file = st.session_state.get(attached_file_key, "")

            if attached_content:
                final_prompt = f"""I'm attaching a file for you to read and reference.

=== ATTACHED FILE: {attached_file} ===
{attached_content}
=== END OF ATTACHED FILE ===

My question/request:
{question}"""

            with st.spinner(f"🧠 {selected_model} is thinking..."):
                # Show what context is being used
                with st.expander("🔍 Context Details", expanded=False):
                    st.write(f"**Using Context:** {'Yes' if use_context else 'No'}")
                    st.write(f"**Chat History Length:** {len(current_history)} exchanges")
                    if attached_file:
                        st.write(f"**Attached File:** {attached_file}")

                    if use_context:
                        kb_status = glm_system.check_vectorstore_status()
                        st.write(f"**Knowledge Base:** {kb_status['message']}")

                # Call model with agent mode
                response_data = glm_system.generate_response(
                    prompt=final_prompt,
                    selected_model=selected_model,
                    use_context=use_context,
                    project_name=selected_project,
                    chat_history=current_history,
                    agent_mode=selected_agent,
                )

                response = response_data["response"]
                routing_info = response_data.get("routing", {})

            # Add to chat history (with agent_mode)
            st.session_state[chat_key].append((question, response, selected_agent))

            # Display model used
            actual_model = routing_info.get('selected_model', selected_model)
            st.success(f"✅ Response from {actual_model}")

            # Save to project file (with agent_mode)
            glm_system.project_manager.save_chat_to_project(
                selected_project, actual_model, question, response, selected_agent
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

    # Use consolidated theme CSS
    from src.ui.theme import get_agent_context_css
    st.markdown(get_agent_context_css(), unsafe_allow_html=True)

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
            st.caption(f"📊 {word_count} words | Auto-updated by fast model after each exchange")

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
        # Header with collapse button
        col_header, col_btn = st.columns([4, 1])
        with col_header:
            st.subheader("💬 Recent Conversations")
        with col_btn:
            if st.button("🔽 Collapse All", key="collapse_all_chats", use_container_width=True):
                st.session_state.collapse_all_conversations = True
                st.rerun()

        # Check if we should collapse all
        collapse_all = st.session_state.get("collapse_all_conversations", False)
        # Reset the flag after use (one-time collapse)
        if collapse_all:
            st.session_state.collapse_all_conversations = False

        for i, chat_entry in enumerate(reversed(recent_chats), 1):
            # Handle both 2-tuple (legacy) and 3-tuple (with agent_mode) formats
            if len(chat_entry) == 3:
                question, answer, agent_mode = chat_entry
            else:
                question, answer = chat_entry
                agent_mode = "General"
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

            # Determine if expanded (collapsed if collapse_all was clicked)
            should_expand = False if collapse_all else (i <= 2)

            # Get agent icon from AGENT_MODES if available
            agent_icon = AGENT_MODES.get(agent_mode, {}).get("icon", "🤖")

            # Create expandable container for each chat
            with st.expander(
                f"{content_icon} Q{len(recent_chats) - i + 1} [{agent_icon} {agent_mode}]: {question_preview}",
                expanded=should_expand,
            ):
                # Agent badge at top
                st.caption(f"🏷️ **Agent:** {agent_icon} {agent_mode}")

                # Question section
                st.markdown("**🙋 Your Question:**")
                # Detect language for syntax highlighting
                question_lang = get_code_language_from_content(question)
                st.code(question, language=question_lang)

                # Answer section - use helper to show R1 thinking if present
                display_response_with_thinking(answer, selected_model)

                # Options section
                st.markdown("---")
                st.markdown("**⚡ Options:**")

                msg_id = len(recent_chats) - i + 1

                # Check for FAUST content
                has_faust = _detect_faust_code_in_text(answer)

                col4 = None  # Initialize for non-FAUST case
                if has_faust:
                    col1, col2, col3, col4 = st.columns(4)
                else:
                    col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("📋 Copy Response", key=f"copy_{msg_id}"):
                        st.session_state[f"show_copy_{msg_id}"] = True
                        st.rerun()

                # Show copyable code block if requested
                if st.session_state.get(f"show_copy_{msg_id}"):
                    st.markdown("**📋 Copy from here (use copy button top-right):**")
                    st.code(answer, language="markdown")
                    if st.button("✖️ Hide", key=f"hide_copy_{msg_id}"):
                        st.session_state[f"show_copy_{msg_id}"] = False
                        st.rerun()

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

                # FAUST Analyze button in col4 (only if has_faust)
                if has_faust:
                    assert col4 is not None
                    with col4:
                        analyze_key = f"show_faust_analysis_{msg_id}"
                        if st.button("🎛️ Analyze FAUST", key=f"faust_{msg_id}"):
                            st.session_state[analyze_key] = True

                # Metadata footer
                st.markdown("---")
                fcol1, fcol2, fcol3 = st.columns(3)

                with fcol1:
                    st.caption(f"📝 Q: {len(question)} chars")
                with fcol2:
                    st.caption(f"📋 A: {len(answer)} chars")
                with fcol3:
                    if "```" in answer:
                        st.caption("💻 Contains Code")
                    elif any(keyword in answer.lower() for keyword in ["faust", "dsp", "audio"]):
                        st.caption("🎵 Audio/DSP")
                    else:
                        st.caption("💬 Text")

                # Show FAUST analysis results if triggered
                if has_faust and st.session_state.get(f"show_faust_analysis_{msg_id}", False):
                    _analyze_faust_in_response(answer, msg_id)
                    st.session_state[f"show_faust_analysis_{msg_id}"] = False

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
            for i, chat_entry in enumerate(reversed(chat_history[-10:]), 1):
                # Handle both 2-tuple (legacy) and 3-tuple (with agent_mode) formats
                if len(chat_entry) == 3:
                    question, answer, agent_mode = chat_entry
                else:
                    question, answer = chat_entry
                    agent_mode = "General"

                question_preview = question.replace("\n", " ")[:100] + (
                    "..." if len(question) > 100 else ""
                )

                # Get agent icon
                agent_icon = AGENT_MODES.get(agent_mode, {}).get("icon", "🤖")

                with st.expander(
                    f"🔹 Conv {total_messages - i + 1} [{agent_icon} {agent_mode}]: {question_preview}",
                    expanded=False,
                ):
                    # Agent badge
                    st.caption(f"🏷️ **Agent:** {agent_icon} {agent_mode}")

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


def _detect_faust_code_in_text(text: str) -> bool:
    """Detect if text contains FAUST code or FAUST-related content."""
    import re
    text_lower = text.lower()

    # Quick keyword check first (faster)
    faust_keywords = [
        'stdfaust.lib', 'process =', 'process=',
        'import("', "import('", 'declare ',
        'os.osc', 'fi.lowpass', 'fi.highpass', 'fi.bandpass',
        'de.delay', 're.freeverb', 'en.adsr',
        '.dsp', 'faust code', 'faust dsp',
    ]
    for keyword in faust_keywords:
        if keyword in text_lower:
            return True

    # Regex patterns for more complex matching
    faust_patterns = [
        r'import\s*\(\s*["\'].*\.lib["\']\s*\)',  # import("*.lib")
        r'process\s*=\s*',  # process = ...
        r'\b[a-z]{2}\.[a-z]+\s*\(',  # os.osc(, fi.lowpass(, etc.
        r'```\s*(?:faust|dsp)',  # code block with faust/dsp language
    ]
    for pattern in faust_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


def _extract_faust_code(text: str) -> str:
    """Extract FAUST code from text (looks for code blocks or raw FAUST)."""
    import re

    # Try to find explicitly labeled FAUST/DSP code blocks first
    faust_block_pattern = r'```(?:faust|dsp)\s*\n(.*?)```'
    matches = re.findall(faust_block_pattern, text, re.DOTALL | re.IGNORECASE)
    if matches:
        return matches[0].strip()

    # Try any code block that contains FAUST patterns
    any_block_pattern = r'```\w*\s*\n(.*?)```'
    blocks = re.findall(any_block_pattern, text, re.DOTALL)
    for block in blocks:
        if 'import(' in block and 'process' in block:
            return block.strip()
        if 'stdfaust.lib' in block:
            return block.strip()

    # Try to find code with stdfaust.lib import (not in code block)
    import_pattern = r'(import\s*\(\s*["\']stdfaust\.lib["\']\s*\)[\s\S]*?process\s*=[\s\S]*?;)'
    matches = re.findall(import_pattern, text, re.IGNORECASE)
    if matches:
        return matches[0].strip()

    # Last resort: look for process = ... pattern
    process_pattern = r'((?:import\s*\([^)]+\)\s*;\s*)*process\s*=\s*[^;]+;)'
    matches = re.findall(process_pattern, text, re.IGNORECASE)
    if matches:
        # Add stdfaust.lib import if missing
        code = matches[0].strip()
        if 'import(' not in code:
            code = 'import("stdfaust.lib");\n' + code
        return code

    return ""


def _analyze_faust_in_response(response_text: str, msg_id: int):
    """Analyze FAUST code found in a chat response."""
    from src.core.faust_mcp_client import analyze_faust_code, check_faust_server

    faust_code = _extract_faust_code(response_text)

    if not faust_code:
        st.warning("Could not extract FAUST code from response")
        return

    if not check_faust_server():
        st.error("🎛️ faust-mcp server is not running")
        st.info("Start it with: `./start_assistant.sh`")
        return

    with st.spinner("🎛️ Compiling and analyzing FAUST code..."):
        try:
            result = analyze_faust_code(faust_code)
            analysis_dict = {
                "status": result.status,
                "max_amplitude": result.max_amplitude,
                "rms": result.rms,
                "is_silent": result.is_silent,
                "waveform": result.waveform_ascii,
                "num_outputs": result.num_outputs,
                "channels": result.channels,
                "features": result.features,
                "error": result.error,
            }
            render_faust_analysis(analysis_dict)
        except Exception as e:
            st.error(f"Analysis failed: {e}")


def render_faust_analysis(analysis: dict):
    """
    Render FAUST analysis results from faust-mcp in the UI.

    Args:
        analysis: Dictionary containing analysis results from faust-mcp
    """
    if not analysis:
        return

    if analysis.get("status") == "error":
        st.error(f"🎛️ FAUST Analysis Error: {analysis.get('error', 'Unknown error')}")
        return

    # Use container for full width
    st.markdown("---")
    st.subheader("🎛️ FAUST Analysis Results")

    # Status row
    status_text = "✅ Compiled successfully" if analysis.get("status") == "success" else f"⚠️ {analysis.get('status')}"
    st.markdown(f"**Status:** {status_text}")

    # Metrics columns - use full width
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        max_amp = analysis.get("max_amplitude", 0)
        amp_color = "🔴" if max_amp > 0.95 else "🟢" if max_amp > 0.1 else "⚪"
        st.metric("Max Amplitude", f"{max_amp:.4f}", delta=amp_color)

    with col2:
        rms = analysis.get("rms", 0)
        st.metric("RMS Level", f"{rms:.4f}")

    with col3:
        num_outputs = analysis.get("num_outputs", 0)
        st.metric("Channels", str(num_outputs))

    with col4:
        is_silent = analysis.get("is_silent", True)
        silent_text = "🔇 Silent" if is_silent else "🔊 Audio"
        st.metric("Output", silent_text)

    # Warnings
    if analysis.get("is_silent"):
        st.warning("⚠️ Output is silent - check your signal flow")
    if analysis.get("max_amplitude", 0) > 0.99:
        st.warning("⚠️ Possible clipping detected - consider adding a limiter")

    # Waveform visualization
    waveform = analysis.get("waveform", "")
    if waveform:
        st.markdown("**Waveform Preview:**")
        st.code(waveform, language=None)

    # Spectral features
    features = analysis.get("features", {})
    if features and features.get("spectral_available"):
        st.markdown("**Spectral Features:**")
        feat_cols = st.columns(5)

        with feat_cols[0]:
            centroid = features.get("spectral_centroid", 0)
            st.metric("Centroid", f"{centroid:.0f} Hz")

        with feat_cols[1]:
            bandwidth = features.get("spectral_bandwidth", 0)
            st.metric("Bandwidth", f"{bandwidth:.0f} Hz")

        with feat_cols[2]:
            rolloff = features.get("spectral_rolloff", 0)
            st.metric("Rolloff", f"{rolloff:.0f} Hz")

        with feat_cols[3]:
            flatness = features.get("spectral_flatness", 0)
            st.metric("Flatness", f"{flatness:.4f}")

        with feat_cols[4]:
            crest = features.get("crest_factor", 0)
            st.metric("Crest Factor", f"{crest:.2f}")

    # Time-domain features
    if features:
        dc_offset = features.get("dc_offset", 0)
        zcr = features.get("zero_crossing_rate", 0)
        clipping = features.get("clipping_ratio", 0)

        if abs(dc_offset) > 0.01 or clipping > 0:
            st.markdown("**Additional Metrics:**")
            add_cols = st.columns(3)

            with add_cols[0]:
                if abs(dc_offset) > 0.01:
                    st.metric("DC Offset", f"{dc_offset:.6f}")
                    st.caption("⚠️ Consider adding DC blocking filter")

            with add_cols[1]:
                st.metric("Zero Crossing Rate", f"{zcr:.4f}")

            with add_cols[2]:
                if clipping > 0:
                    st.metric("Clipping Ratio", f"{clipping:.2%}")
                    st.caption("⚠️ Audio is clipping")

    # Per-channel details (collapsible)
    channels = analysis.get("channels", [])
    if channels and len(channels) > 1:
        with st.expander("Per-Channel Details", expanded=False):
            for ch in channels:
                idx = ch.get("index", 0)
                ch_max = ch.get("max_amplitude", 0)
                ch_rms = ch.get("rms", 0)
                ch_wf = ch.get("waveform_ascii", "")

                st.markdown(f"**Channel {idx + 1}:** Max: {ch_max:.4f} | RMS: {ch_rms:.4f}")
                if ch_wf:
                    st.code(ch_wf, language=None)


def render_faust_server_status(glm_system):
    """Render faust-mcp server status in the UI."""
    try:
        status = glm_system.check_faust_server_status()

        with st.expander("🎛️ FAUST Analysis Server", expanded=False):
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown(f"**Status:** {status.get('status', 'Unknown')}")
                if status.get("faust_version"):
                    st.caption(status.get("faust_version"))

            with col2:
                st.markdown(f"**Backend:** {status.get('backend', 'none')}")
                st.caption(status.get("message", ""))

            if not status.get("server_running"):
                st.info("💡 Start the server to enable FAUST code analysis")

    except Exception as e:
        st.warning(f"Could not check FAUST server status: {e}")


def render_wavesurfer_player(audio_url: str, key: str = "wavesurfer", height: int = 200) -> None:
    """Render a wavesurfer.js audio player with region loop support.

    Args:
        audio_url: URL or path to the audio file (must be accessible via HTTP)
        key: Unique key for the component (used to make waveform ID unique)
        height: Height of the waveform display in pixels
    """
    import streamlit.components.v1 as components
    # Use key to create unique element IDs
    waveform_id = f"waveform_{key}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>
        <script src="https://unpkg.com/wavesurfer.js@7/dist/plugins/regions.min.js"></script>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                background: transparent;
                padding: 10px;
            }}
            #{waveform_id} {{
                width: 100%;
                height: {height - 60}px;
                background: #1a1a2e;
                border-radius: 8px;
                margin-bottom: 10px;
            }}
            .controls {{
                display: flex;
                gap: 8px;
                align-items: center;
                flex-wrap: wrap;
            }}
            button {{
                background: #4a4a6a;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                transition: background 0.2s;
            }}
            button:hover {{ background: #5a5a8a; }}
            button:disabled {{ background: #333; cursor: not-allowed; }}
            button.active {{ background: #6366f1; }}
            .info {{
                color: #888;
                font-size: 12px;
                margin-left: auto;
            }}
            .time {{
                color: #aaa;
                font-size: 13px;
                font-family: monospace;
            }}
            .region-info {{
                color: #6366f1;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div id="{waveform_id}"></div>
        <div class="controls">
            <button id="playBtn" disabled>▶ Play</button>
            <button id="stopBtn" disabled>⏹ Stop</button>
            <button id="loopBtn" disabled>🔁 Loop Region</button>
            <button id="clearBtn" disabled>✕ Clear</button>
            <span class="time" id="timeDisplay">0:00 / 0:00</span>
            <span class="region-info" id="regionInfo"></span>
            <span class="info">Drag on waveform to select loop region</span>
        </div>

        <script>
            let wavesurfer = null;
            let regions = null;
            let activeRegion = null;
            let loopEnabled = false;

            document.addEventListener('DOMContentLoaded', function() {{
                // Initialize WaveSurfer
                wavesurfer = WaveSurfer.create({{
                    container: '#{waveform_id}',
                    waveColor: '#4a4a6a',
                    progressColor: '#6366f1',
                    cursorColor: '#fff',
                    barWidth: 2,
                    barGap: 1,
                    barRadius: 2,
                    height: {height - 60},
                    normalize: true,
                }});

                // Initialize Regions plugin
                regions = wavesurfer.registerPlugin(WaveSurfer.Regions.create());

                // Load audio
                wavesurfer.load('{audio_url}');

                const playBtn = document.getElementById('playBtn');
                const stopBtn = document.getElementById('stopBtn');
                const loopBtn = document.getElementById('loopBtn');
                const clearBtn = document.getElementById('clearBtn');
                const timeDisplay = document.getElementById('timeDisplay');
                const regionInfo = document.getElementById('regionInfo');

                function formatTime(seconds) {{
                    const mins = Math.floor(seconds / 60);
                    const secs = Math.floor(seconds % 60);
                    return mins + ':' + secs.toString().padStart(2, '0');
                }}

                wavesurfer.on('ready', function() {{
                    playBtn.disabled = false;
                    stopBtn.disabled = false;
                    loopBtn.disabled = false;
                    clearBtn.disabled = false;
                    timeDisplay.textContent = '0:00 / ' + formatTime(wavesurfer.getDuration());
                }});

                wavesurfer.on('audioprocess', function() {{
                    timeDisplay.textContent = formatTime(wavesurfer.getCurrentTime()) + ' / ' + formatTime(wavesurfer.getDuration());
                }});

                wavesurfer.on('play', function() {{
                    playBtn.textContent = '⏸ Pause';
                }});

                wavesurfer.on('pause', function() {{
                    playBtn.textContent = '▶ Play';
                }});

                // Region creation by dragging
                regions.enableDragSelection({{
                    color: 'rgba(99, 102, 241, 0.3)',
                }});

                regions.on('region-created', function(region) {{
                    // Remove previous region if exists
                    if (activeRegion && activeRegion !== region) {{
                        activeRegion.remove();
                    }}
                    activeRegion = region;
                    region.setOptions({{ color: 'rgba(99, 102, 241, 0.3)' }});
                    regionInfo.textContent = 'Region: ' + formatTime(region.start) + ' - ' + formatTime(region.end);
                }});

                regions.on('region-updated', function(region) {{
                    regionInfo.textContent = 'Region: ' + formatTime(region.start) + ' - ' + formatTime(region.end);
                }});

                // Play button
                playBtn.addEventListener('click', function() {{
                    wavesurfer.playPause();
                }});

                // Stop button
                stopBtn.addEventListener('click', function() {{
                    wavesurfer.stop();
                }});

                // Loop button
                loopBtn.addEventListener('click', function() {{
                    loopEnabled = !loopEnabled;
                    loopBtn.classList.toggle('active', loopEnabled);
                    if (loopEnabled && activeRegion) {{
                        activeRegion.play();
                    }}
                }});

                // Clear region button
                clearBtn.addEventListener('click', function() {{
                    if (activeRegion) {{
                        activeRegion.remove();
                        activeRegion = null;
                        regionInfo.textContent = '';
                        loopEnabled = false;
                        loopBtn.classList.remove('active');
                    }}
                }});

                // Loop region when reaching end
                regions.on('region-out', function(region) {{
                    if (loopEnabled && region === activeRegion) {{
                        region.play();
                    }}
                }});
            }});
        </script>
    </body>
    </html>
    """

    components.html(html_content, height=height, scrolling=False)

