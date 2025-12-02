import streamlit as st
from pathlib import Path
from ..core.prompts import MODEL_INFO
import re


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
        st.subheader("📁 Project Management")

        # Initialize current project if not set
        if "current_project" not in st.session_state:
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
    """Render hybrid model selection section with routing modes"""
    # Add styling for better visibility
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
        padding-bottom: 10px;
        border-bottom: 1px solid #45475a;
    }
    .routing-mode {
        background-color: #45475a;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #89b4fa;
        margin: 15px 0;
        color: #cdd6f4;
    }
    .model-selection .stRadio label {
        color: #cdd6f4 !important;
        font-weight: 500 !important;
    }
    .model-selection .stSelectbox label {
        color: #cdd6f4 !important;
        font-weight: 600 !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="model-selection">', unsafe_allow_html=True)
        
        # Routing Mode Selection
        st.markdown('<div class="routing-mode">', unsafe_allow_html=True)
        st.subheader("🤖 Model Selection & Routing")
        
        col1, col2 = st.columns(2)
        with col1:
            routing_mode = st.radio(
                "Routing Mode",
                ["🚀 Auto (HRM Decides)", "🎯 Manual Selection", "💡 Assisted (See Recommendations)"],
                index=0,
                help="Choose how models are selected for your tasks"
            )
        
        with col2:
            use_context = st.checkbox(
                "📚 Use Knowledge Base",
                value=True,
                help="Include uploaded documents in responses",
            )
            
            # HRM Debug Mode
            hrm_wrapper = getattr(glm_system, 'hrm_wrapper', None)
            if hrm_wrapper:
                debug_hrm = st.checkbox(
                    "🔍 HRM Debug Mode",
                    value=False,
                    help="Show HRM task decomposition details in responses",
                    key="hrm_debug_mode"
                )
            else:
                debug_hrm = False
        
        # Convert routing mode to simple string
        routing_mode_map = {
            "🚀 Auto (HRM Decides)": "auto",
            "🎯 Manual Selection": "manual", 
            "💡 Assisted (See Recommendations)": "assisted"
        }
        routing_mode_key = routing_mode_map[routing_mode]
        
        # Model Selection based on routing mode
        if routing_mode == "🎯 Manual Selection":
            model_options = list(glm_system.models.keys())
            selected_model = st.selectbox(
                "Choose Model",
                options=model_options,
                help="DeepSeek-R1 for reasoning/debugging, Qwen2.5-Coder for implementation, Qwen2.5 for math/physics",
            )
            
            # Show model info
            if selected_model in MODEL_INFO:
                st.info(MODEL_INFO[selected_model])
                
        else:
            selected_model = "auto"
            if routing_mode == "🚀 Auto (HRM Decides)":
                hrm_status = "🧠 HRM will analyze your request and route to the optimal model automatically"
                if getattr(glm_system, 'hrm_wrapper', None):
                    device = getattr(glm_system.hrm_wrapper, 'device', 'unknown')
                    if device == 'mps':
                        hrm_status += " ⚡ (M4 Max MPS acceleration)"
                    elif device == 'cuda':
                        hrm_status += " 🚀 (CUDA acceleration)"
                st.info(hrm_status)
            else:  # Assisted mode
                st.info("💡 HRM will analyze your request and show recommendations, but you can override")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        return selected_model, use_context, routing_mode_key, debug_hrm


def render_sidebar(glm_system):
    """Render sidebar with file management"""
    with st.sidebar:
        st.header("📚 Knowledge Base Management")

        # File upload section
        render_file_upload_section(glm_system)

        # Bulk operations
        render_bulk_operations(glm_system)

        # FAUST Documentation Section
        render_faust_docs_section(glm_system)

        # Model status
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
    """Render model status section with HRM integration"""
    st.subheader("🔧 System Status")
    
    # HRM Status Section
    st.write("**🧠 HRM Integration:**")
    hrm_wrapper = getattr(glm_system, 'hrm_wrapper', None)
    if hrm_wrapper:
        # Display HRM device status
        device = getattr(hrm_wrapper, 'device', 'unknown')
        if device == 'mps':
            st.success("⚡ M4 Max MPS acceleration active")
        elif device == 'cuda':
            st.success("🚀 CUDA acceleration active")
        elif device == 'cpu':
            st.info("💻 CPU processing mode")
        else:
            st.warning(f"❓ Unknown device: {device}")
        
        # Display HRM availability
        try:
            # Check if HRM can decompose tasks
            test_decomp = hrm_wrapper.decompose_task("test", context={})
            if hasattr(test_decomp, 'subtasks'):
                st.success("✅ HRM task decomposition ready")
            else:
                st.warning("⚠️ HRM using pattern-based fallback")
        except Exception:
            st.warning("⚠️ HRM using pattern-based fallback")
            
        # HRM configuration info
        with st.expander("🔍 HRM Configuration", expanded=False):
            st.write("**Architecture:** HRM ACT v1")
            st.write("**Device:** " + device.upper())
            st.write("**Caching:** Enabled" if getattr(hrm_wrapper, 'enable_caching', False) else "Disabled")
    else:
        st.error("❌ HRM not initialized")
    
    st.write("---")
    
    # Ollama Model Status
    st.write("**🤖 Ollama Models:**")
    for model_name, model_id in glm_system.models.items():
        try:
            if model_name in glm_system._model_instances:
                st.success(f"✅ {model_name}")
            else:
                st.info(f"💤 {model_name} (not loaded)")
        except:
            st.error(f"❌ {model_name}")

    if st.button("🔍 Check Model Availability"):
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


def render_chat_interface(glm_system, selected_model, use_context, selected_project, routing_mode="manual", debug_hrm=False):
    """Render main chat interface with hybrid routing support"""
    if selected_model == "auto":
        st.header(f"💬 Chat with AI Assistant (Auto-Routing)")
    else:
        st.header(f"💬 Chat with {selected_model}")
    st.caption(f"Project: {selected_project} | Mode: {routing_mode.title()}")

    # Project-based chat history
    chat_key = f"chat_history_{selected_model}_{selected_project}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = glm_system.project_manager.load_project_chats(
            selected_project, selected_model
        )

    # 1. CHAT INPUT FIRST (at the top)
    render_chat_input(
        glm_system, selected_model, use_context, selected_project, chat_key, routing_mode, debug_hrm
    )

    # Add some spacing
    st.write("---")

    # 2. RECENT CONVERSATIONS (below input)
    render_recent_conversations(st.session_state[chat_key], selected_model)

    # 3. FULL CHAT HISTORY (at the bottom)
    render_full_chat_history(st.session_state[chat_key], selected_model)


def render_chat_input(
    glm_system, selected_model, use_context, selected_project, chat_key, routing_mode="manual", debug_hrm=False
):
    """Render chat input section with enhanced context handling"""
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
                st.session_state.clear_chat_input = True
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
            if st.button("🗑️ Clear Chat History"):
                st.session_state[chat_key] = []
                st.success("Chat history cleared!")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # Handle send button - ENHANCED WITH CHAT HISTORY
        if send_button and question:
            # Get current chat history
            current_history = st.session_state.get(chat_key, [])

            with st.spinner(f"{selected_model} is thinking..."):
                # Show what context is being used
                with st.expander("🔍 Context Details", expanded=False):
                    st.write(f"**Using Context:** {'Yes' if use_context else 'No'}")
                    st.write(
                        f"**Chat History Length:** {len(current_history)} exchanges"
                    )

                    if use_context:
                        kb_status = glm_system.check_vectorstore_status()
                        st.write(f"**Knowledge Base:** {kb_status['message']}")

                        if len(current_history) > 0:
                            st.write("**Recent Topics:**")
                            for i, (prev_q, _) in enumerate(current_history[-3:], 1):
                                st.write(
                                    f"  {i}. {prev_q[:80]}{'...' if len(prev_q) > 80 else ''}"
                                )

                # Call model with hybrid routing system
                response_data = glm_system.generate_response(
                    prompt=question,
                    selected_model=selected_model,
                    routing_mode=routing_mode,
                    use_context=use_context,
                    project_name=selected_project,
                    chat_history=current_history,  # PASS CHAT HISTORY
                    use_hrm_decomposition=True
                )
                
                response = response_data["response"]
                routing_info = response_data.get("routing", {})

            # Add to chat history
            st.session_state[chat_key].append((question, response))
            
            # Display routing decision if available
            if routing_info:
                with st.expander("🔄 Routing Decision", expanded=debug_hrm):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Complexity", f"{routing_info.get('complexity_score', 0):.2f}")
                    with col2:
                        st.metric("Domain", routing_info.get('domain', 'general'))
                    with col3:
                        st.metric("Model Used", routing_info.get('selected_model', 'Unknown'))
                    
                    if routing_info.get('hrm_recommendation') != routing_info.get('selected_model'):
                        st.info(f"💡 HRM recommended: {routing_info.get('hrm_recommendation')}")
                    
                    if routing_info.get('subtasks', 0) > 0:
                        st.info(f"🧠 Complex task decomposed into {routing_info.get('subtasks')} subtasks")
                        
                        # Show HRM debug details if enabled
                        if debug_hrm and routing_info.get('subtasks', 0) > 0:
                            st.write("**🔍 HRM Debug Information:**")
                            st.json({
                                "execution_time": routing_info.get('execution_time', 0),
                                "confidence": routing_info.get('confidence', 0),
                                "routing_reason": routing_info.get('routing_reason', ''),
                                "mode": routing_info.get('mode', ''),
                            })
                    
                    if routing_info.get('fallback_used'):
                        st.warning(f"⚠️ Fallback used: {routing_info.get('routing_reason')}")
                        
                    # HRM device status in debug mode
                    if debug_hrm:
                        hrm_wrapper = getattr(glm_system, 'hrm_wrapper', None)
                        if hrm_wrapper:
                            device = getattr(hrm_wrapper, 'device', 'unknown')
                            st.write(f"**🖥️ HRM Device:** {device.upper()}")
                            if device == 'mps':
                                st.success("⚡ M4 Max MPS acceleration used")

            # Save to project file  
            actual_model_used = routing_info.get('selected_model', selected_model) if routing_info else selected_model
            glm_system.project_manager.save_chat_to_project(
                selected_project, actual_model_used, question, response
            )

            st.rerun()


def render_recent_conversations(chat_history, selected_model):
    """Render recent conversations section"""
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

                # Answer section
                st.markdown(f"**🤖 {selected_model}:**")
                if "```" in answer:
                    st.markdown(answer)
                else:
                    st.write(answer)

                # Add metadata footer with actions
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.caption(f"📝 Q: {len(question)} chars")
                with col2:
                    st.caption(f"📋 A: {len(answer)} chars")
                with col3:
                    # Detect content type
                    if "```" in answer:
                        st.caption("💻 Code")
                    elif any(
                        keyword in answer.lower()
                        for keyword in ["faust", "dsp", "audio"]
                    ):
                        st.caption("🎵 Audio/DSP")
                    elif "http" in answer:
                        st.caption("🔗 Links")
                    else:
                        st.caption("💬 Text")
                with col4:
                    # Quick copy button for code blocks
                    if "```" in answer:
                        if st.button(
                            "📋 Copy",
                            key=f"copy_recent_{len(recent_chats) - i + 1}",
                            help="Copy code to clipboard",
                        ):
                            # Note: Actual clipboard functionality would need additional setup
                            st.success(
                                "Code copied to clipboard! (feature coming soon)"
                            )

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

                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.write("**Answer:**")
                    with col2:
                        if "```" in answer:
                            st.markdown(answer)
                        else:
                            st.write(answer)

                    # Show token/character count
                    st.caption(f"📊 Q: {len(question)} chars | A: {len(answer)} chars")

                if i < 10 and i < total_messages:  # Don't add divider after last item
                    st.write("---")


