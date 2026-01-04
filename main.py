import streamlit as st
import urllib.parse
from pathlib import Path
from src.core import MultiModelGLMSystem
from src.ui import (
    FileEditor,
    FileBrowser,
    EditorUI,
    render_project_management,
    render_model_selection,
    render_sidebar,
    render_chat_interface,
    render_system_monitor,
)
from src.ui.project_meta_ui import render_project_meta_tab
from src.ui.model_setup_ui import render_model_setup_tab
from src.ui.theme import inject_global_styles


def main():
    st.set_page_config(
        page_title="Multi-Model AI Development Assistant",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Inject consolidated global styles
    inject_global_styles()

    st.title("Multi-Model AI Development Assistant")

    # Initialize system
    if "multi_glm_system" not in st.session_state:
        with st.spinner("Initializing AI system..."):
            st.session_state.multi_glm_system = MultiModelGLMSystem()
            st.success("✅ AI system initialized (Reasoning + Fast models)")

    # Initialize editor components
    if "file_editor" not in st.session_state:
        st.session_state.file_editor = FileEditor(
            st.session_state.multi_glm_system.project_manager
        )

    if "file_browser" not in st.session_state:
        st.session_state.file_browser = FileBrowser(st.session_state.file_editor)

    if "editor_ui" not in st.session_state:
        st.session_state.editor_ui = EditorUI(
            st.session_state.file_editor, st.session_state.multi_glm_system
        )

    # Initialize FAUST realtime state
    if "faust_realtime" not in st.session_state:
        st.session_state.faust_realtime = {
            "running": False,
            "current_file": None,
        }

    # Project management (shared across all tabs)
    selected_project = render_project_management(st.session_state.multi_glm_system)

    # Tab options
    tab_options = ["📋 Project Meta", "💬 AI Chat", "📝 Code Editor", "📚 Knowledge Base", "🖥️ System Monitor", "⚙️ Model Setup"]
    tab_keys = ["meta", "chat", "editor", "kb", "monitor", "models"]  # Short keys for URL

    # Initialize active tab - check URL params first for persistence across refreshes
    if "active_tab" not in st.session_state:
        query_params = st.query_params
        url_tab = query_params.get("tab", "meta")
        if url_tab in tab_keys:
            st.session_state.active_tab = tab_options[tab_keys.index(url_tab)]
        else:
            st.session_state.active_tab = "📋 Project Meta"

    # Render tab buttons using columns
    tab_cols = st.columns(len(tab_options))
    for i, (tab_name, tab_key) in enumerate(zip(tab_options, tab_keys)):
        with tab_cols[i]:
            is_active = st.session_state.active_tab == tab_name
            # Use different button type for active/inactive
            if is_active:
                # Active tab - green style using primary
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #1e5a3a 0%, #2d8a57 100%);
                    padding: 12px 8px;
                    border-radius: 8px;
                    border: 2px solid #a6e3a1;
                    text-align: center;
                    font-weight: 700;
                    font-size: 0.9rem;
                    color: #ffffff;
                    box-shadow: 0 4px 15px rgba(166, 227, 161, 0.4);
                    cursor: default;
                ">{tab_name}</div>
                """, unsafe_allow_html=True)
            else:
                # Inactive tab - blue style, clickable
                if st.button(tab_name, key=f"tab_btn_{tab_key}", use_container_width=True):
                    st.session_state.active_tab = tab_name
                    st.query_params["tab"] = tab_key
                    st.rerun()

    # Tab button styling is handled by theme.py

    selected_tab = st.session_state.active_tab

    st.divider()

    # Render content based on selected tab
    if selected_tab == "📋 Project Meta":
        render_project_meta_tab(st.session_state.multi_glm_system, selected_project)

    elif selected_tab == "💬 AI Chat":
        st.header("🤖 AI Assistant Chat")
        selected_model, use_context, selected_agent = render_model_selection(
            st.session_state.multi_glm_system
        )
        render_chat_interface(
            st.session_state.multi_glm_system,
            selected_model,
            use_context,
            selected_project,
            selected_agent,
        )

    elif selected_tab == "📝 Code Editor":
        render_code_editor_tab(selected_project)

    elif selected_tab == "📚 Knowledge Base":
        render_knowledge_base_tab()

    elif selected_tab == "🖥️ System Monitor":
        render_system_monitor(st.session_state.multi_glm_system)

    elif selected_tab == "⚙️ Model Setup":
        render_model_setup_tab(st.session_state.multi_glm_system)

    # Sidebar with condensed controls
    render_sidebar(st.session_state.multi_glm_system)

    # Instructions
    with st.expander("ℹ️ How To Use AI Project and Coding Assistant"):
        st.markdown(
            """
## ⚙️ **Model Setup Tab** (Configure First)
- **Dynamic model selection** - choose any Ollama model for Reasoning or Fast roles
- **Auto-discovery** of installed models
- **Test connections** to verify models are working
- **Persistent configuration** saved to model_config.json

## 📋 **Project Meta Tab**
- **Strategic planning** with PROJECT_META.md for vision, roadmap, milestones
- **Orchestrator agent** for cross-agent coordination and progress tracking
- **Sync from Agents** to synthesize all specialist work into master plan
- **Export Queue** for items ready for Claude Code implementation

## 💬 **AI Chat Tab**
- **Specialist agent modes**: General, FAUST, JUCE, Math, Physics, Orchestrator
- **Configurable models**: Reasoning model for deep thinking, Fast model for quick tasks
- **Project-based chat history** with automatic context summarization
- **Agent meta files** that evolve with your conversations

## 📝 **Code Editor Tab**
- **File browser** with project organization
- **Syntax-highlighted editor** for 20+ programming languages
- **AI-powered code assistance** with change highlighting
- **Diff view** to review AI suggestions before applying

## 📚 **Knowledge Base Tab**
- **FAUST, JUCE documentation** integration
- **File upload** and vector search

## 🚀 **Hybrid Workflow**
1. **Configure models** in Model Setup tab (or use defaults)
2. **Create a named project** (Project Meta not available for Default)
3. **Define vision & roadmap** in Project Meta tab
4. **Work with specialist agents** (FAUST, JUCE, etc.) in AI Chat
5. **Sync progress** back to Project Meta using Orchestrator
6. **Export refined items** to Claude Code for implementation

## 🎯 **Context Hierarchy**
All agents see: Project Meta → Agent Context → Last Exchange → Your Question

This ensures every agent knows the master plan while focusing on their specialty.
"""
        )


def render_code_editor_tab(selected_project: str):
    """Render the code editor tab interface"""
    col1, col2 = st.columns([1, 2])

    # Compute project_path first (needed for both containers)
    if selected_project == "Default":
        base_project_path = str(Path.cwd())
    else:
        base_project_path = str(Path("./projects") / selected_project)

    # Always check URL param and sync with session state
    browse_folder_url = st.query_params.get("browse", "")
    if browse_folder_url:
        browse_folder = urllib.parse.unquote(browse_folder_url)
        if Path(browse_folder).exists() and Path(browse_folder).is_dir():
            # URL has valid folder - always use it (URL is source of truth)
            if st.session_state.get("current_browse_folder") != browse_folder:
                st.session_state.current_browse_folder = browse_folder

    if "current_browse_folder" in st.session_state:
        project_path = st.session_state.current_browse_folder
    else:
        project_path = base_project_path

    with col1:
        # ===== CONTAINER 1: File Browser Controls =====
        with st.container(border=True):
            st.subheader("📁 File Browser")

            # Show which project/folder we're working with
            st.write("**📂 Current Project/Folder:**")

            if "current_browse_folder" in st.session_state:
                st.info(f"📂 **Custom Folder:** `{project_path}`")
                if st.button("🔙 Return to Project Folder", key="return_to_project"):
                    del st.session_state.current_browse_folder
                    if "show_folder_picker" in st.session_state:
                        del st.session_state.show_folder_picker
                    # Clear browse param from URL
                    if "browse" in st.query_params:
                        del st.query_params["browse"]
                    st.rerun()
            else:
                if selected_project == "Default":
                    st.code(f"📁 Default Project: {project_path}")
                else:
                    st.code(f"📁 Project '{selected_project}': {project_path}")
                    if not Path(project_path).exists():
                        st.warning(f"Project directory doesn't exist. Creating: {project_path}")
                        Path(project_path).mkdir(parents=True, exist_ok=True)
                        st.success("Project directory created!")
                        st.rerun()

            # Folder selection buttons
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📂 Browse Folder", key="browse_folder", use_container_width=True):
                    st.session_state.show_folder_picker = not st.session_state.get("show_folder_picker", False)
            with col_b:
                if st.button("🔄 Refresh", key="refresh_files", use_container_width=True):
                    st.session_state.file_browser.expanded_dirs.clear()
                    keys_to_clear = [k for k in st.session_state.keys() if isinstance(k, str) and
                                     (k.startswith("dir_expanded_") or k.startswith("file_select_"))]
                    for key in keys_to_clear:
                        del st.session_state[key]
                    st.rerun()

            # Folder picker
            if st.session_state.get("show_folder_picker", False):
                st.markdown("---")
                st.markdown("**📂 Select Project Folder**")
                selected_folder = st.session_state.file_browser.render_folder_picker()
                if selected_folder == "CANCEL":
                    st.session_state.show_folder_picker = False
                    st.rerun()
                elif selected_folder and selected_folder != project_path:
                    st.session_state.current_browse_folder = selected_folder
                    st.session_state.show_folder_picker = False
                    # Save browse folder to URL for persistence across reloads
                    st.query_params["browse"] = selected_folder
                    st.rerun()

            # File filtering controls
            st.markdown("---")
            include_patterns, exclude_patterns = st.session_state.file_browser.render_file_filter_controls()
            st.session_state.multi_glm_system.project_manager.update_file_patterns(
                selected_project, include_patterns, exclude_patterns
            )

            # File operations
            st.markdown("---")
            new_file = st.session_state.file_browser.render_file_operations(project_path)
            if new_file:
                if st.session_state.editor_ui.open_file_in_editor(new_file):
                    st.rerun()

        # ===== CONTAINER 2: File Tree =====
        with st.container(border=True):
            st.subheader("📁 File Tree")
            selected_file = None

            # Check if Show All Files is enabled - bypass filters
            if st.session_state.get("show_all_files", False):
                tree_include = ["*"]
                tree_exclude = ["__pycache__", ".git", "node_modules", "*.pyc"]
            else:
                tree_include = include_patterns
                tree_exclude = exclude_patterns

            try:
                selected_file = st.session_state.file_browser.render_file_tree(
                    project_path, tree_include, tree_exclude
                )
            except Exception as e:
                st.error(f"**❌ Error rendering file tree:** {e}")
                import traceback
                st.code(traceback.format_exc())

            # Open selected file in editor
            if selected_file:
                selected_file = str(Path(selected_file).resolve())
                success = st.session_state.editor_ui.open_file_in_editor(selected_file)
                if success:
                    st.rerun()
                elif selected_file in st.session_state.get("editor_open_files", {}):
                    st.info(f"File already open: {Path(selected_file).name}")

    with col2:
        # ===== CONTAINER 3: Code Editor =====
        with st.container(border=True):
            st.subheader("💻 Code Editor")

            # Multi-file editor interface
            has_open_files = st.session_state.editor_ui.render_multi_file_editor(
                project_path, selected_project
            )

            if not has_open_files:
                # More helpful instructions when no files are open
                st.markdown(
                    """
                ### 🚀 **Getting Started with the Code Editor**

                **To open files for editing:**
                1. 👈 **Click on any file name** in the file browser on the left
                2. **Use the "📝 Create New File"** button to start from scratch
                3. **Browse different folders** using the folder browser above

                **Features you'll have access to:**
                - ✨ **Syntax highlighting** for 20+ programming languages
                - 🤖 **AI-powered code assistance** with change highlighting
                - 💾 **Direct file saving** - no copy-paste needed
                - 🔍 **Diff viewer** to review AI suggestions
                - 📁 **Multi-file tabs** for working on several files at once

                **Perfect for:**
                - 🎵 **FAUST DSP development**
                - 💻 **C++/Python coding**
                - 📝 **Documentation editing**
                - 🎛️ **JUCE audio applications**
                """
                )

                # Show project stats
                project_stats = (
                    st.session_state.multi_glm_system.project_manager.get_project_stats(
                        selected_project
                    )
                )

                st.write("### 📊 **Project Overview**")
                stat_col1, stat_col2, stat_col3 = st.columns(3)
                with stat_col1:
                    st.metric("📁 Total Files", project_stats["total_files"])
                with stat_col2:
                    st.metric("✅ Included", project_stats["included_files"])
                with stat_col3:
                    st.metric("❌ Excluded", project_stats["excluded_files"])


def render_knowledge_base_tab():
    """Render the knowledge base management tab"""
    st.header("📚 Knowledge Base Management")

    col1, col2 = st.columns([1, 1])

    with col1:
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
                    upload_path = (
                        Path("./uploads") / target_subfolder / uploaded_file.name
                    )
                else:
                    upload_path = Path("./uploads") / uploaded_file.name

                upload_path.parent.mkdir(parents=True, exist_ok=True)

                with open(upload_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                with st.spinner(f"Processing {uploaded_file.name}..."):
                    result = (
                        st.session_state.multi_glm_system.file_processor.process_file(
                            str(upload_path)
                        )
                    )

                folder_display = f"{target_subfolder}/" if target_subfolder else "root/"
                st.success(f"✅ Saved to {folder_display} - {result}")

    with col2:
        st.subheader("🔄 Bulk Operations")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Scan All Subfolders"):
                with st.spinner("Scanning all subfolders..."):
                    result = (
                        st.session_state.multi_glm_system.file_processor.scan_uploads_recursive()
                    )
                st.success(result)

        with col2:
            if st.button("📊 Folder Stats"):
                stats = (
                    st.session_state.multi_glm_system.file_processor.get_folder_stats()
                )
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

        st.subheader("🎵 FAUST Documentation")
        if st.button("📥 Load FAUST Docs"):
            with st.spinner("Loading FAUST documentation..."):
                result = (
                    st.session_state.multi_glm_system.file_processor.load_faust_documentation()
                )
            st.success(result)

        if st.button("🌐 Download FAUST Docs"):
            st.info(
                "Run: python download_faust_docs_complete.py in your project directory"
            )


if __name__ == "__main__":
    main()
