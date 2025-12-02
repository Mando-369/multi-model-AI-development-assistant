import streamlit as st
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


def main():
    st.set_page_config(
        page_title="Multi-Model AI Development Assistant",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS for better tab visibility
    st.markdown("""
    <style>
    /* Tab styling - bigger fonts and better contrast */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #313244;
        padding: 10px 15px;
        border-radius: 10px;
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 18px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        background-color: #45475a;
        border-radius: 8px;
        color: #cdd6f4 !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #585b70;
        color: #ffffff !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #89b4fa !important;
        color: #1e1e2e !important;
    }

    /* Main title styling */
    h1 {
        font-size: 2.5rem !important;
        color: #89b4fa !important;
        padding-bottom: 10px;
        border-bottom: 2px solid #45475a;
        margin-bottom: 20px !important;
    }

    /* Section headers */
    h2 {
        font-size: 1.8rem !important;
        color: #cdd6f4 !important;
    }

    h3 {
        font-size: 1.4rem !important;
        color: #bac2de !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Multi-Model AI Development Assistant")

    # Initialize system
    if "multi_glm_system" not in st.session_state:
        with st.spinner("Initializing multi-model system with HRM..."):
            st.session_state.multi_glm_system = MultiModelGLMSystem()
            
            # Display HRM initialization status
            hrm_status = getattr(st.session_state.multi_glm_system, 'hrm_wrapper', None)
            if hrm_status:
                st.success("🧠 HRM Local Wrapper initialized successfully")
                if hasattr(hrm_status, 'device') and hrm_status.device == 'mps':
                    st.success("⚡ M4 Max MPS acceleration enabled")
            else:
                st.warning("⚠️ HRM initialization incomplete - using pattern-based routing")

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

    # Project management (shared across all tabs)
    selected_project = render_project_management(st.session_state.multi_glm_system)

    # Main interface tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 AI Chat", "📝 Code Editor", "📚 Knowledge Base", "🖥️ System Monitor"])

    # Tab 1: AI Chat Interface (existing functionality)
    with tab1:
        st.header("🤖 AI Assistant Chat")
        selected_model, use_context, routing_mode, debug_hrm = render_model_selection(
            st.session_state.multi_glm_system
        )
        render_chat_interface(
            st.session_state.multi_glm_system,
            selected_model,
            use_context,
            selected_project,
            routing_mode,
            debug_hrm,
        )

    # Tab 2: Code Editor Interface (new functionality)
    with tab2:
        render_code_editor_tab(selected_project)

    # Tab 3: Knowledge Base Management (moved from sidebar)
    with tab3:
        render_knowledge_base_tab()

    # Tab 4: System Monitor
    with tab4:
        render_system_monitor(st.session_state.multi_glm_system)

    # Sidebar with condensed controls
    render_sidebar(st.session_state.multi_glm_system)

    # Instructions
    with st.expander("ℹ️ How to Use the Enhanced System with Code Editor"):
        st.markdown(
            """
## 💬 **AI Chat Tab**
- **Multi-model conversations** with DeepSeek-R1, Qwen2.5-Coder, and Qwen2.5
- **Project-based chat history** and context
- **HRM-powered intelligent routing** for optimal model selection

## 📝 **Code Editor Tab**
- **File browser** with project organization
- **Syntax-highlighted editor** for 20+ programming languages
- **AI-powered code assistance** with change highlighting
- **Direct file editing** with save/revert functionality
- **Diff view** to review AI suggestions before applying

## 📚 **Knowledge Base Tab**
- **File upload and organization** by category
- **FAUST, JUCE, and Python documentation** integration
- **Bulk file processing** and statistics

## 🔧 **Key Editor Features**
- **🤖 AI Code Changes**: Highlight additions, deletions, and modifications
- **💾 Direct Save**: No copy-paste needed, edit files directly
- **🔍 Diff Viewer**: Side-by-side, unified, or changes-only views
- **📁 Project Files**: Include/exclude files, pattern-based filtering
- **🎯 Multi-language**: Python, C++, FAUST, JavaScript, and more

## 🚀 **Workflow Example**
1. **Select/Create Project** in any tab
2. **Open files** in the Code Editor tab
3. **Ask AI** to modify your code with specific instructions
4. **Review changes** in the diff viewer with highlighted modifications
5. **Accept/Reject** AI suggestions or manually edit
6. **Save directly** to your files
7. **Use AI Chat** for questions about your code

## 🎵 **FAUST Development**
- **Qwen2.5-Coder model** with FAUST documentation context
- **FAUST documentation** integrated into knowledge base
- **Audio effect templates** and examples
- **Real-time code suggestions** for signal processing

The editor integrates seamlessly with your AI models - ask them to modify code and see exactly what changes they suggest!
"""
        )


def render_code_editor_tab(selected_project: str):
    """Render the code editor tab interface"""
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📁 File Browser")

        # Get project path - fix the logic here
        if selected_project == "Default":
            base_project_path = str(Path.cwd())
        else:
            base_project_path = str(Path("./projects") / selected_project)

        # Show which project/folder we're working with
        st.write("**📂 Current Project/Folder:**")

        # Use custom folder if one was selected, otherwise use project folder
        if "current_browse_folder" in st.session_state:
            project_path = st.session_state.current_browse_folder
            st.info(f"📂 **Custom Folder:** `{project_path}`")

            # Add button to return to project folder
            if st.button("🔙 Return to Project Folder", key="return_to_project"):
                del st.session_state.current_browse_folder
                if "show_folder_picker" in st.session_state:
                    del st.session_state.show_folder_picker
                st.rerun()
        else:
            project_path = base_project_path
            if selected_project == "Default":
                st.code(f"📁 Default Project: {project_path}")
            else:
                st.code(f"📁 Project '{selected_project}': {project_path}")

                # Check if project directory exists, create if not
                if not Path(project_path).exists():
                    st.warning(
                        f"Project directory doesn't exist. Creating: {project_path}"
                    )
                    Path(project_path).mkdir(parents=True, exist_ok=True)
                    st.success("Project directory created!")
                    st.rerun()

        # Add folder selection option
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(
                "📂 Browse Different Folder",
                key="browse_folder",
                help="Browse and select a different folder to work with",
                type="secondary",
                use_container_width=True,
            ):
                st.session_state.show_folder_picker = not st.session_state.get(
                    "show_folder_picker", False
                )

        with col_b:
            if st.button(
                "🔄 Refresh Files", key="refresh_files", use_container_width=True
            ):
                # Clear expanded directories when refreshing to start collapsed
                st.session_state.file_browser.expanded_dirs.clear()

                # Clear ALL relevant session state keys more thoroughly
                keys_to_clear = []
                for key in list(st.session_state.keys()):
                    if isinstance(key, str) and (
                        key.startswith("dir_expanded_")
                        or key.startswith("file_select_")
                        or key.startswith("editor_")
                        or key.startswith("ai_prompt_")
                        or key.startswith("ai_model_")
                    ):
                        keys_to_clear.append(key)

                # Clear the keys
                for key in keys_to_clear:
                    del st.session_state[key]

                st.success("File browser refreshed and collapsed!")
                st.rerun()

        # Show folder picker if requested
        if st.session_state.get("show_folder_picker", False):
            st.write("---")
            with st.container():
                st.markdown("### 📂 **Select Project Folder**")

                selected_folder = st.session_state.file_browser.render_folder_picker()

                if selected_folder == "CANCEL":
                    st.session_state.show_folder_picker = False
                    st.rerun()
                elif selected_folder:
                    if selected_folder != project_path:
                        # Store the selected folder
                        st.session_state.current_browse_folder = selected_folder
                        st.success(f"✅ **Switched to folder:** `{selected_folder}`")
                        st.session_state.show_folder_picker = False
                        st.rerun()

        st.write("---")

        # File filtering controls
        include_patterns, exclude_patterns = (
            st.session_state.file_browser.render_file_filter_controls()
        )

        # Update project file patterns
        st.session_state.multi_glm_system.project_manager.update_file_patterns(
            selected_project, include_patterns, exclude_patterns
        )

        st.write("---")

        # File operations
        new_file = st.session_state.file_browser.render_file_operations(project_path)
        if new_file:
            # Open newly created file in editor
            if st.session_state.editor_ui.open_file_in_editor(new_file):
                st.rerun()

        st.write("---")

        # File tree browser
        st.write("**📁 File Tree:**")
        selected_file = None  # Initialize to avoid unbound variable

        try:
            # Actually call the method with comprehensive error handling
            selected_file = st.session_state.file_browser.render_file_tree(
                project_path, include_patterns, exclude_patterns
            )

        except Exception as e:
            st.error(f"**❌ Error rendering file tree:** {e}")
            st.write(f"**Error details:** {type(e).__name__}: {str(e)}")
            # Show traceback
            import traceback

            st.code(traceback.format_exc())

        # Open selected file in editor - FIXED LOGIC
        if selected_file:
            # Ensure the file path is absolute and normalized
            selected_file = str(Path(selected_file).resolve())

            # Debug info
            with st.expander("🔍 Debug: File Opening", expanded=False):
                st.write(f"Selected file: {selected_file}")
                st.write(f"File exists: {Path(selected_file).exists()}")
                st.write(
                    f"Currently open files: {list(st.session_state.get('editor_open_files', {}).keys())}"
                )

            # Try to open the file
            success = st.session_state.editor_ui.open_file_in_editor(selected_file)

            if success:
                # Force a rerun to update the UI
                st.rerun()
            else:
                # File might already be open, switch to its tab
                if selected_file in st.session_state.get("editor_open_files", {}):
                    st.info(f"File already open: {Path(selected_file).name}")

    with col2:
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
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📁 Total Files", project_stats["total_files"])
            with col2:
                st.metric("✅ Included", project_stats["included_files"])
            with col3:
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
