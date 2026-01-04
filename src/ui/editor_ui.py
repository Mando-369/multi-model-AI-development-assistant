import streamlit as st
from streamlit_ace import st_ace
from pathlib import Path
from typing import Dict, List, Optional
import difflib
import re
import hashlib
import urllib.parse
from src.core.prompts import AGENT_MODES


class EditorUI:
    def __init__(self, file_editor, multi_glm_system):
        self.file_editor = file_editor
        self.multi_glm_system = multi_glm_system

        # Initialize open_files in session state if not present
        if "editor_open_files" not in st.session_state:
            st.session_state.editor_open_files = {}

        # Restore from URL query params on first load (check flag in session state)
        if "editor_url_restored" not in st.session_state:
            st.session_state.editor_url_restored = True
            self._restore_from_url()

    def _restore_from_url(self):
        """Restore open files from URL query params."""
        try:
            file_param = st.query_params.get("file", "")

            if file_param:
                # Decode URL-encoded path and normalize to absolute
                file_path = urllib.parse.unquote(file_param)
                file_path = str(Path(file_path).resolve())  # Normalize to absolute path
                path = Path(file_path)

                if path.exists() and path.is_file():
                    if file_path not in st.session_state.editor_open_files:
                        try:
                            content = path.read_text(encoding="utf-8", errors="replace")
                            st.session_state.editor_open_files[file_path] = {
                                "original_content": content,
                                "current_content": content,
                                "language": self.get_language_from_extension(file_path),
                                "has_unsaved_changes": False,
                                "has_ai_suggestions": False,
                                "ai_suggested_content": None,
                                "is_binary": False,
                            }
                            st.toast(f"Restored: {path.name}", icon="📂")
                        except Exception as e:
                            st.warning(f"Could not restore file: {e}")
                else:
                    st.warning(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error restoring from URL: {e}")

    def _save_to_url(self):
        """Save current open file to URL query params."""
        try:
            open_files = list(st.session_state.get("editor_open_files", {}).keys())
            if open_files:
                # Save the first/active file to URL (use absolute path)
                file_path = str(Path(open_files[0]).resolve())
                st.query_params["file"] = file_path
            else:
                # Clear file param if no files open
                if "file" in st.query_params:
                    del st.query_params["file"]
        except Exception as e:
            print(f"Error saving to URL: {e}")

    def get_language_from_extension(self, file_path: str) -> str:
        """Get ACE editor language mode from file extension"""
        ext = Path(file_path).suffix.lower()

        language_map = {
            ".py": "python",
            ".cpp": "c_cpp",
            ".cc": "c_cpp",
            ".cxx": "c_cpp",
            ".h": "c_cpp",
            ".hpp": "c_cpp",
            ".hxx": "c_cpp",
            ".c": "c_cpp",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".cs": "csharp",
            ".go": "golang",
            ".rs": "rust",
            ".php": "php",
            ".rb": "ruby",
            ".html": "html",
            ".css": "css",
            ".scss": "scss",
            ".less": "less",
            ".xml": "xml",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".md": "markdown",
            ".sql": "sql",
            ".sh": "sh",
            ".bash": "sh",
            ".ps1": "powershell",
            ".bat": "batchfile",
            ".dsp": "c_cpp",  # FAUST files - C++ mode for best available highlighting
            ".fst": "c_cpp",
            ".lib": "c_cpp",
            ".txt": "text",
            ".log": "text",
            ".ini": "ini",
            ".cfg": "ini",
            ".conf": "ini",
            ".toml": "toml",
        }

        return language_map.get(ext, "text")

    def get_code_language_for_display(self, content: str, file_path: str = None) -> str:
        """Get appropriate language for st.code() based on content or file extension"""
        if file_path:
            ext = Path(file_path).suffix.lower()
            if ext in [".dsp", ".fst", ".lib"]:
                return "javascript"  # Use JavaScript highlighting as fallback for FAUST (closest syntax)
        
        # Detect FAUST code by keywords
        faust_keywords = ["import", "declare", "process", "library", "component", "with", "letrec"]
        if any(keyword in content for keyword in faust_keywords):
            return "javascript"  # Use JavaScript highlighting as fallback
            
        return "text"


    def get_editor_theme(self) -> str:
        """Get editor theme based on Streamlit theme"""
        return "monokai"  # Dark theme that works well with most Streamlit themes

    def render_editor_interface(
        self, file_path: str, project_name: str = "Default"
    ) -> Dict:
        """Render main code editor interface"""

        # Normalize to absolute path for consistent keying
        file_path = str(Path(file_path).resolve())

        # Initialize session state for open files if not present
        if "editor_open_files" not in st.session_state:
            st.session_state.editor_open_files = {}

        # Read file content if not already loaded
        if file_path not in st.session_state.editor_open_files:
            with st.spinner(f"Loading {Path(file_path).name}..."):
                file_content = self.file_editor.read_file_content(file_path)

                if "error" in file_content:
                    st.error(file_content["error"])
                    return {"error": file_content["error"]}

                # Store in session state
                st.session_state.editor_open_files[file_path] = {
                    "original_content": file_content["content"],
                    "current_content": file_content["content"],
                    "has_unsaved_changes": False,
                    "has_ai_suggestions": False,
                    "ai_suggested_content": None,
                    "language": self.get_language_from_extension(file_path),
                    "is_binary": file_content.get("is_binary", False),
                }
                # Persist open files list
                self._save_to_url()

        file_data = st.session_state.editor_open_files[file_path]

        # Handle binary files
        if file_data["is_binary"]:
            st.warning(f"Binary file cannot be edited: {Path(file_path).name}")
            st.code(file_data["current_content"])
            return {"binary_file": True}

        # File header with info
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

        with col1:
            st.subheader(f"📝 {Path(file_path).name}")
            st.caption(f"📍 {file_path}")

        with col2:
            lines_count = len(file_data["current_content"].splitlines())
            st.metric("Lines", lines_count)

        with col3:
            chars_count = len(file_data["current_content"])
            st.metric("Characters", chars_count)

        with col4:
            if file_data["has_unsaved_changes"]:
                st.error("● Unsaved")
            elif file_data["has_ai_suggestions"]:
                st.warning("🤖 AI Changes")
            else:
                st.success("✅ Saved")

        # AI Integration Section
        self.render_ai_integration(file_path, project_name)

        st.write("---")

        # Show diff if AI suggestions exist
        if file_data["has_ai_suggestions"] and file_data.get("ai_suggested_content"):
            self.render_diff_view(file_path)

        # Get the content to display
        content_to_display = file_data.get("ai_suggested_content") or file_data.get(
            "current_content", ""
        )

        # IMPORTANT: Ensure content is a string and not None
        if content_to_display is None:
            content_to_display = ""
        else:
            content_to_display = str(content_to_display)

        # Create unique editor key that includes file path hash for uniqueness
        file_hash = hashlib.md5(file_path.encode()).hexdigest()[:8]
        editor_key = f"ace_{file_hash}_{Path(file_path).stem}"

        st.subheader("📝 Code Editor")

        # Add FAUST-specific styling when editing FAUST files
        if Path(file_path).suffix.lower() in [".dsp", ".fst", ".lib"]:
            from src.ui.theme import get_faust_editor_css
            st.markdown(get_faust_editor_css(), unsafe_allow_html=True)
            st.info("🎵 **FAUST file** - Monaco-inspired syntax highlighting")

        # Store the content in a separate session state key for the editor
        # IMPORTANT: Only initialize if not already present - preserve user edits across reruns
        editor_value_key = f"editor_value_{file_hash}"
        if editor_value_key not in st.session_state:
            st.session_state[editor_value_key] = content_to_display

        try:
            # Use st_ace with proper configuration
            editor_content = st_ace(
                value=st.session_state[editor_value_key],  # Use session state value
                language=file_data.get("language", "text"),
                theme=self.get_editor_theme(),
                key=editor_key,
                height=1200,
                font_size=12,
                tab_size=4,
                wrap=False,
                auto_update=False,  # Important: set to False
                show_gutter=True,
                show_print_margin=True,
                annotations=None,  # Simplify for now
            )

            # Update content if changed (comparing against editor value, not file data)
            if editor_content is not None and editor_content != "":
                # Check if content differs from what we passed to st_ace
                if editor_content != st.session_state[editor_value_key]:
                    # User made edits - update session state
                    st.session_state[editor_value_key] = editor_content
                    st.session_state.editor_open_files[file_path][
                        "current_content"
                    ] = editor_content
                    st.session_state.editor_open_files[file_path][
                        "has_unsaved_changes"
                    ] = True
                    # Rerun to show updated content in editor
                    st.rerun()

        except Exception as e:
            st.error(f"Editor error: {e}")
            # Fallback to text_area
            st.warning("Using fallback text editor")
            editor_content = st.text_area(
                "Edit File (Fallback Mode)",
                value=content_to_display,
                height=1200,
                key=f"fallback_{editor_key}",
            )

            if editor_content != file_data["current_content"]:
                st.session_state.editor_open_files[file_path][
                    "current_content"
                ] = editor_content
                st.session_state.editor_open_files[file_path][
                    "has_unsaved_changes"
                ] = True

        # File actions
        self.render_file_actions(file_path)

        return {"success": True, "content": editor_content or content_to_display}

    def render_ai_integration(self, file_path: str, project_name: str):
        """Render AI integration controls"""
        st.subheader("🤖 AI Assistant")

        # Create unique key prefix for this file
        file_key = Path(file_path).name.replace(".", "_")

        col1, col2 = st.columns([2, 1])

        with col1:
            # Use session state to persist prompt across reruns
            prompt_key = f"editor_ai_prompt_{file_key}"
            if prompt_key not in st.session_state:
                st.session_state[prompt_key] = ""

            ai_prompt = st.text_area(
                "What would you like the AI to do with this file?",
                value=st.session_state[prompt_key],
                placeholder="Examples: Add comments, Optimize for performance, Fix bugs, Refactor...",
                height=350,
                key=f"ai_prompt_{file_key}",
            )
            # Store in session state
            st.session_state[prompt_key] = ai_prompt

        with col2:
            # Model selection for file editing
            available_models = list(self.multi_glm_system.models.keys())
            selected_model = st.selectbox(
                "AI Model:",
                available_models,
                key=f"ai_model_{file_key}",
                help="DeepSeek for complex tasks, Qwen for quick edits",
            )

            # Agent mode selection (same as AI Chat tab)
            agent_options = list(AGENT_MODES.keys())
            agent_labels = [f"{AGENT_MODES[a]['icon']} {a}" for a in agent_options]
            selected_agent_idx = st.selectbox(
                "Specialist Mode:",
                options=range(len(agent_options)),
                format_func=lambda x: agent_labels[x],
                index=0,
                key=f"ai_agent_{file_key}",
                help="Choose domain-specific expertise",
            )
            selected_agent = agent_options[selected_agent_idx]
            agent_info = AGENT_MODES[selected_agent]
            st.caption(f"*{agent_info['description']}*")

            use_context = st.checkbox(
                "Use project context",
                value=True,
                key=f"ai_context_{file_key}",
                help="Include other project files and documentation",
            )

            if st.button("🚀 Apply AI", key=f"ai_apply_{file_key}"):
                if ai_prompt.strip() and selected_model:
                    self.apply_ai_to_file(
                        file_path, ai_prompt, selected_model, use_context, project_name, selected_agent
                    )
                elif not ai_prompt.strip():
                    st.warning("Please enter a prompt for the AI")
                else:
                    st.error("Please select a model")

    def is_analysis_task(self, prompt: str) -> bool:
        """Detect if the task is analysis/explanation (vs code modification)."""
        prompt_lower = prompt.lower()
        analysis_keywords = [
            "summary", "summarize", "explain", "describe", "what does",
            "how does", "tell me", "review", "analyze", "analysis",
            "understand", "documentation", "comment on", "overview",
            "what is", "why does", "purpose", "function of",
        ]
        return any(keyword in prompt_lower for keyword in analysis_keywords)

    def apply_ai_to_file(
        self,
        file_path: str,
        prompt: str,
        model_name: str,
        use_context: bool,
        project_name: str,
        agent_mode: str = "General",
    ):
        """Apply AI assistance to file content"""
        file_path = str(file_path)
        file_data = st.session_state.editor_open_files[file_path]

        # Detect if this is an analysis task (summary, explain, etc.) vs modification
        is_analysis = self.is_analysis_task(prompt)

        if is_analysis:
            # Analysis task - ask for explanation, not code
            enhanced_prompt = f"""Please analyze this file: {Path(file_path).name}

File content:
```{file_data['language']}
{file_data['current_content']}
```

Task: {prompt}

Provide a clear, helpful response. Focus on explaining and analyzing, not modifying the code.
"""
            spinner_text = f"🤖 {model_name} is analyzing your file..."
        else:
            # Modification task - ask for code changes
            enhanced_prompt = f"""Please help me modify this file: {Path(file_path).name}

Current file content:
```{file_data['language']}
{file_data['current_content']}
```

Task: {prompt}

Please provide the complete modified file content. Only return the code/content, no explanations unless specifically requested.
"""
            spinner_text = f"🤖 {model_name} is modifying your file..."

        with st.spinner(spinner_text):
            try:
                response = self.multi_glm_system.chat_with_model(
                    enhanced_prompt, model_name, use_context, project_name, None, agent_mode
                )

                if is_analysis:
                    # For analysis tasks, just display the response
                    st.success("✅ Analysis complete!")
                    st.markdown("### 📝 AI Analysis")
                    st.markdown(response)
                else:
                    # For modification tasks, extract code and apply changes
                    ai_content = self.extract_code_from_response(
                        response, file_data["language"]
                    )

                    result = self.file_editor.apply_ai_suggestion(file_path, ai_content)

                    if result.get("success"):
                        st.session_state.editor_open_files[file_path][
                            "ai_suggested_content"
                        ] = ai_content
                        st.session_state.editor_open_files[file_path][
                            "has_ai_suggestions"
                        ] = True
                        # Clear editor value to show AI suggestions
                        file_hash = hashlib.md5(file_path.encode()).hexdigest()[:8]
                        editor_value_key = f"editor_value_{file_hash}"
                        if editor_value_key in st.session_state:
                            del st.session_state[editor_value_key]

                        st.success(
                            f"✅ AI suggestions applied! {result['changes_count']} changes detected."
                        )
                        st.rerun()
                    else:
                        st.error(result.get("error", "Failed to apply AI suggestions"))

            except Exception as e:
                st.error(f"Error applying AI: {e}")

    def extract_code_from_response(self, response: str, language: str) -> str:
        """Extract code content from AI response, removing markdown formatting"""
        # Try to find code blocks first
        code_block_pattern = rf"```{language}(.*?)```"
        matches = re.findall(code_block_pattern, response, re.DOTALL | re.IGNORECASE)

        if matches:
            return matches[0].strip()

        # Try generic code blocks
        generic_pattern = r"```(.*?)```"
        matches = re.findall(generic_pattern, response, re.DOTALL)

        if matches:
            return matches[0].strip()

        # If no code blocks found, return the response as-is (might be pure code)
        return response.strip()

    def render_diff_view(self, file_path: str):
        """Render diff visualization for AI changes"""
        file_path = str(Path(file_path).resolve())
        file_data = st.session_state.editor_open_files[file_path]

        if not file_data.get("ai_suggested_content"):
            return

        st.subheader("🔍 AI Changes Preview")

        # Get diff data
        diff_data = self.file_editor.generate_detailed_diff(
            file_data["original_content"], file_data["ai_suggested_content"]
        )

        # Summary of changes
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "➕ Added", diff_data["summary"]["lines_added"], delta_color="normal"
            )
        with col2:
            st.metric(
                "➖ Removed",
                diff_data["summary"]["lines_removed"],
                delta_color="inverse",
            )
        with col3:
            st.metric(
                "✏️ Modified", diff_data["summary"]["lines_modified"], delta_color="off"
            )
        with col4:
            st.metric("📊 Total Changes", diff_data["summary"]["total_changes"])

        # Diff display options
        diff_display = st.radio(
            "Diff View:",
            ["Side by Side", "Unified Diff", "Changed Sections Only"],
            horizontal=True,
            key=f"diff_view_{Path(file_path).name}",
        )

        if diff_display == "Side by Side":
            self.render_side_by_side_diff(diff_data, file_path)
        elif diff_display == "Unified Diff":
            self.render_unified_diff(diff_data)
        else:
            self.render_changed_sections(diff_data, file_path)

    def render_side_by_side_diff(self, diff_data: Dict, file_path: str = None):
        """Render side-by-side diff comparison"""
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Original**")
            original_text = "\n".join(diff_data["original_lines"])
            lang = self.get_code_language_for_display(original_text, file_path)
            st.code(original_text, language=lang)

        with col2:
            st.write("**AI Suggested**")
            modified_text = "\n".join(diff_data["modified_lines"])
            lang = self.get_code_language_for_display(modified_text, file_path)
            st.code(modified_text, language=lang)

    def render_unified_diff(self, diff_data: Dict):
        """Render unified diff format"""
        unified_diff = "\n".join(diff_data["unified_diff"])
        st.code(unified_diff, language="diff")

    def render_changed_sections(self, diff_data: Dict, file_path: str = None):
        """Render only the sections with changes"""
        for i, section in enumerate(diff_data["changed_sections"]):
            st.write(f"**Change {i+1}: {section['operation'].title()}**")

            col1, col2 = st.columns(2)

            with col1:
                if section["original_lines"]:
                    st.write("*Original:*")
                    original_text = "\n".join(section["original_lines"])
                    lang = self.get_code_language_for_display(original_text, file_path)
                    st.code(original_text, language=lang)

            with col2:
                if section["modified_lines"]:
                    st.write("*Modified:*")
                    modified_text = "\n".join(section["modified_lines"])
                    lang = self.get_code_language_for_display(modified_text, file_path)
                    st.code(modified_text, language=lang)

            st.write("---")

    def get_editor_annotations(self, file_path: str) -> List[Dict]:
        """Get annotations for highlighting changes in the editor"""
        file_path = str(Path(file_path).resolve())
        if file_path not in self.file_editor.file_states:
            return []

        highlights = self.file_editor.get_file_diff_highlights(file_path)
        if not highlights:
            return []

        annotations = []

        # Add annotations for additions (green)
        for line_num in highlights["additions"]:
            annotations.append(
                {"row": line_num, "column": 0, "text": "AI Addition", "type": "info"}
            )

        # Add annotations for deletions (red)
        for line_num in highlights["deletions"]:
            annotations.append(
                {"row": line_num, "column": 0, "text": "AI Deletion", "type": "warning"}
            )

        # Add annotations for modifications (blue)
        for line_num in highlights["modifications"]:
            annotations.append(
                {
                    "row": line_num,
                    "column": 0,
                    "text": "AI Modification",
                    "type": "error",
                }
            )

        return annotations

    def render_file_actions(self, file_path: str):
        """Render file action buttons"""
        file_path = str(Path(file_path).resolve())
        st.write("---")

        file_data = st.session_state.editor_open_files[file_path]
        filename = Path(file_path).name

        # Check if this is a FAUST file
        is_faust_file = Path(file_path).suffix.lower() in [".dsp", ".fst", ".lib"]

        # Adjust columns based on whether FAUST tools are available
        if is_faust_file:
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
        else:
            col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            # Save file
            if st.button("💾 Save", key=f"save_{filename}"):
                content_to_save = file_data.get(
                    "ai_suggested_content", file_data["current_content"]
                )
                result = self.file_editor.save_file_content(file_path, content_to_save)

                if result.get("success"):
                    st.session_state.editor_open_files[file_path][
                        "original_content"
                    ] = content_to_save
                    st.session_state.editor_open_files[file_path][
                        "current_content"
                    ] = content_to_save
                    st.session_state.editor_open_files[file_path][
                        "has_unsaved_changes"
                    ] = False
                    st.session_state.editor_open_files[file_path][
                        "has_ai_suggestions"
                    ] = False
                    st.session_state.editor_open_files[file_path][
                        "ai_suggested_content"
                    ] = None
                    st.success(result["message"])
                    st.rerun()
                else:
                    st.error(result.get("error", "Save failed"))

        with col2:
            # Revert changes
            if file_data["has_unsaved_changes"] or file_data["has_ai_suggestions"]:
                if st.button("↩️ Revert", key=f"revert_{filename}"):
                    st.session_state.editor_open_files[file_path]["current_content"] = (
                        file_data["original_content"]
                    )
                    st.session_state.editor_open_files[file_path][
                        "has_unsaved_changes"
                    ] = False
                    st.session_state.editor_open_files[file_path][
                        "has_ai_suggestions"
                    ] = False
                    st.session_state.editor_open_files[file_path][
                        "ai_suggested_content"
                    ] = None
                    # Clear editor value to force refresh
                    file_hash = hashlib.md5(file_path.encode()).hexdigest()[:8]
                    editor_value_key = f"editor_value_{file_hash}"
                    if editor_value_key in st.session_state:
                        del st.session_state[editor_value_key]
                    st.success("Changes reverted!")
                    st.rerun()

        with col3:
            # Accept AI suggestions
            if file_data["has_ai_suggestions"]:
                if st.button("✅ Accept AI", key=f"accept_ai_{filename}"):
                    st.session_state.editor_open_files[file_path]["current_content"] = (
                        file_data["ai_suggested_content"]
                    )
                    st.session_state.editor_open_files[file_path][
                        "has_ai_suggestions"
                    ] = False
                    st.session_state.editor_open_files[file_path][
                        "has_unsaved_changes"
                    ] = True
                    # Clear editor value to force refresh
                    file_hash = hashlib.md5(file_path.encode()).hexdigest()[:8]
                    editor_value_key = f"editor_value_{file_hash}"
                    if editor_value_key in st.session_state:
                        del st.session_state[editor_value_key]
                    st.success("AI suggestions accepted!")
                    st.rerun()

        with col4:
            # Reject AI suggestions
            if file_data["has_ai_suggestions"]:
                if st.button("❌ Reject AI", key=f"reject_ai_{filename}"):
                    st.session_state.editor_open_files[file_path][
                        "has_ai_suggestions"
                    ] = False
                    st.session_state.editor_open_files[file_path][
                        "ai_suggested_content"
                    ] = None
                    st.success("AI suggestions rejected!")
                    st.rerun()

        with col5:
            # Close file - FIXED LOGIC
            self.render_close_button(file_path, file_data, filename)

        # FAUST tools (only for FAUST files)
        syntax_check_triggered = False
        analyze_triggered = False
        run_triggered = False
        stop_triggered = False

        if is_faust_file:
            with col6:
                # Syntax Check (fast, local)
                if st.button("✓ Syntax", key=f"faust_syntax_{filename}"):
                    syntax_check_triggered = True

            with col7:
                # Full Analysis (offline, via MCP)
                if st.button("🎛️ Analyze", key=f"faust_analyze_{filename}"):
                    analyze_triggered = True

            with col8:
                # Run/Stop Realtime
                is_running = st.session_state.faust_realtime.get("running", False)
                if is_running:
                    if st.button("⏹️ Stop", key=f"faust_stop_{filename}"):
                        stop_triggered = True
                else:
                    if st.button("▶️ Run", key=f"faust_run_{filename}"):
                        run_triggered = True

        # Show realtime status if running
        if st.session_state.faust_realtime.get("running", False):
            st.success("🔊 DSP Running - [Open Parameter UI](http://127.0.0.1:8787/)")

        # Input source controls for FAUST files (for testing effects)
        # Always show and keep expanded to preserve file_uploader state
        if is_faust_file:
            is_running = st.session_state.faust_realtime.get("running", False)
            expander_label = "🔊 Test Input (for effects)" + (" - DSP Running" if is_running else "")
            with st.expander(expander_label, expanded=True):
                # Preserve input source selection across reruns
                source_key = f"faust_input_source_persist_{filename}"
                if source_key not in st.session_state:
                    st.session_state[source_key] = "none"

                options = ["none", "sine", "noise", "file"]
                current_idx = options.index(st.session_state[source_key]) if st.session_state[source_key] in options else 0

                col_src, col_opt = st.columns([1, 2])
                with col_src:
                    input_source = st.selectbox(
                        "Input Source",
                        options=options,
                        index=current_idx,
                        key=f"faust_input_source_{filename}",
                        help="Test signal for effects (DSPs with inputs)"
                    )
                    # Persist selection
                    st.session_state[source_key] = input_source

                with col_opt:
                    if input_source == "sine":
                        input_freq = st.number_input(
                            "Frequency (Hz)",
                            min_value=20,
                            max_value=20000,
                            value=1000,
                            step=100,
                            key=f"faust_input_freq_{filename}"
                        )
                    elif input_source == "file":
                        # Toggle between local file and URL
                        file_mode = st.radio(
                            "Source",
                            ["Local File", "HTTP URL"],
                            key=f"faust_file_mode_{filename}",
                            horizontal=True
                        )

                        if file_mode == "Local File":
                            uploaded_file = st.file_uploader(
                                "Audio File",
                                type=["wav", "mp3", "ogg", "flac", "aiff"],
                                key=f"faust_input_file_{filename}",
                                help="Drag & drop an audio file here"
                            )
                            if uploaded_file:
                                # Save to temp file for FAUST to access
                                import tempfile
                                import os
                                temp_dir = tempfile.gettempdir()
                                temp_path = os.path.join(temp_dir, f"faust_input_{uploaded_file.name}")
                                with open(temp_path, "wb") as f:
                                    f.write(uploaded_file.getbuffer())
                                st.caption(f"📁 {uploaded_file.name}")
                                st.session_state[f"faust_input_file_path_{filename}"] = temp_path
                        else:
                            # HTTP URL input
                            url_input = st.text_input(
                                "Audio URL",
                                placeholder="http://localhost:8080/myfile.wav",
                                key=f"faust_input_url_{filename}",
                                help="HTTP/HTTPS URL to audio file"
                            )
                            if url_input:
                                st.session_state[f"faust_input_file_path_{filename}"] = url_input
                    else:
                        st.caption("No options for this source")

                # Store in session state for use by run_faust_realtime
                if "faust_input_settings" not in st.session_state:
                    st.session_state.faust_input_settings = {}

                settings = {"source": input_source, "freq": None, "file": None}
                if input_source == "sine":
                    settings["freq"] = st.session_state.get(f"faust_input_freq_{filename}", 1000)
                elif input_source == "file":
                    settings["file"] = st.session_state.get(f"faust_input_file_path_{filename}", "")

                st.session_state.faust_input_settings[file_path] = settings

        # Handle FAUST actions OUTSIDE columns for full-width display
        if is_faust_file:
            if syntax_check_triggered:
                self.check_faust_syntax_file(file_path, file_data)
            if analyze_triggered:
                self.analyze_faust_file(file_path, file_data)
            if run_triggered:
                self.run_faust_realtime(file_path, file_data)
            if stop_triggered:
                self.stop_faust_realtime()

    def analyze_faust_file(self, file_path: str, file_data: dict):
        """Analyze FAUST code using faust-mcp server"""
        from src.core.faust_mcp_client import analyze_faust_code, check_faust_server
        from src.ui.ui_components import render_faust_analysis

        # Get current content (use AI suggested if available, otherwise current)
        faust_code = file_data.get("ai_suggested_content") or file_data.get("current_content", "")

        if not faust_code.strip():
            st.warning("No FAUST code to analyze")
            return

        # Check if server is running
        if not check_faust_server():
            st.error("🎛️ faust-mcp server is not running")
            st.info("Start it with: `./start_assistant.sh` or manually run the faust-mcp server on port 8765")
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

    def check_faust_syntax_file(self, file_path: str, file_data: dict):
        """Quick syntax check - uses realtime server (WASM) or local faust CLI as fallback"""
        from src.core.faust_realtime_client import check_faust_syntax_realtime, check_realtime_server
        from src.core.faust_mcp_client import check_faust_syntax

        # Get current content (use AI suggested if available)
        faust_code = file_data.get("ai_suggested_content") or file_data.get("current_content", "")

        if not faust_code.strip():
            st.warning("No FAUST code to check")
            return

        with st.spinner("Checking syntax..."):
            # Try realtime server first (WASM-based, no local faust needed)
            if check_realtime_server():
                result = check_faust_syntax_realtime(faust_code)
                if result.success:
                    st.success("✓ **Syntax OK** - No errors found")
                    if result.params:
                        with st.expander("Parameters detected"):
                            for p in result.params:
                                st.text(f"  {p.get('label', p.get('address', '?'))}: {p.get('init', 0)}")
                else:
                    st.error("**✗ Syntax Error**")
                    st.code(result.error, language="text")
            else:
                # Fallback to local faust CLI
                result = check_faust_syntax(faust_code)
                if result["success"]:
                    st.success("✓ **Syntax OK** - No errors found")
                else:
                    st.error("**✗ Syntax Error**")
                    st.code(result["errors"], language="text")

    def _detect_faust_has_inputs(self, faust_code: str) -> bool:
        """Detect if FAUST code expects audio inputs (is an effect vs generator)."""
        # Look for input indicators:
        # - Underscore `_` in process definition (explicit input)
        # - Common effect patterns that take input
        # - fi.*, ef.*, aa.* library functions that process input

        import re

        # Remove comments
        code = re.sub(r'//.*$', '', faust_code, flags=re.MULTILINE)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

        # Check for underscore input in process
        # Patterns: `process = _ ...`, `process = something(_)`, `_ : something`
        if re.search(r'process\s*=\s*[^;]*_', code):
            return True

        # Check for common effect library prefixes that need input
        effect_patterns = [
            r'\bfi\.\w+',  # filters (fi.lowpass, fi.highpass, etc.)
            r'\bef\.\w+',  # effects (ef.echo, ef.flanger, etc.)
            r'\baa\.\w+',  # analyzers
            r'\bve\.\w+',  # virtual analog effects
            r'\bco\.\w+',  # compressors
            r'\bde\.\w+',  # delays
            r'\bre\.\w+',  # reverbs (re.mono_freeverb, etc.)
        ]
        for pattern in effect_patterns:
            if re.search(pattern, code):
                return True

        return False

    def run_faust_realtime(self, file_path: str, file_data: dict):
        """Compile and start FAUST code in realtime"""
        from src.core.faust_realtime_client import run_faust, check_realtime_server

        # Get current content (use AI suggested if available)
        faust_code = file_data.get("ai_suggested_content") or file_data.get("current_content", "")

        if not faust_code.strip():
            st.warning("No FAUST code to run")
            return

        # Check if realtime server is running
        if not check_realtime_server():
            st.error("Realtime server not running on :8000")
            st.info("Start with: `WEBAUDIO_ROOT=... MCP_TRANSPORT=sse MCP_PORT=8000 python3 faust_realtime_server.py`")
            return

        # Get input source settings
        input_settings = st.session_state.get("faust_input_settings", {}).get(file_path, {})
        input_source = input_settings.get("source", "none")
        input_freq = input_settings.get("freq")
        input_file = input_settings.get("file")

        # Safety check: warn if DSP has inputs but no input source selected
        has_inputs = self._detect_faust_has_inputs(faust_code)
        if has_inputs and input_source == "none":
            st.warning("⚠️ **Effect detected** - This DSP expects audio input but 'none' is selected.")
            st.info("Select a test input (sine, noise, or file) in the 'Test Input' expander above, then click Run again.")
            return

        with st.spinner("Compiling and starting DSP..."):
            result = run_faust(
                faust_code,
                input_source=input_source,
                input_freq=input_freq,
                input_file=input_file
            )

            if result.success:
                st.session_state.faust_realtime["running"] = True
                st.session_state.faust_realtime["current_file"] = file_path
                input_info = f" (input: {input_source})" if input_source != "none" else ""
                st.success(f"▶️ DSP Started{input_info}: {result.message}")
                st.rerun()
            else:
                st.error(f"Failed to start: {result.error}")

    def stop_faust_realtime(self):
        """Stop the currently running FAUST DSP"""
        from src.core.faust_realtime_client import stop_faust

        with st.spinner("Stopping DSP..."):
            result = stop_faust()

            st.session_state.faust_realtime["running"] = False
            st.session_state.faust_realtime["current_file"] = None

            if result.success:
                st.success("⏹️ DSP Stopped")
            else:
                st.warning(f"Stop command sent (may have already stopped): {result.error}")

            st.rerun()

    def render_close_button(self, file_path: str, file_data: dict, filename: str):
        """Render close button with proper confirmation logic"""
        has_changes = (
            file_data["has_unsaved_changes"] or file_data["has_ai_suggestions"]
        )
        confirm_key = f"confirm_close_{filename}_{hash(file_path) % 1000}"  # Unique key

        if has_changes:
            # Show warning state if there are unsaved changes
            if confirm_key not in st.session_state:
                st.session_state[confirm_key] = False

            if not st.session_state[confirm_key]:
                # First click - show warning
                if st.button("⚠️ Close", key=f"close_warn_{filename}"):
                    st.session_state[confirm_key] = True
                    st.rerun()

                if st.session_state.get(confirm_key, False):
                    st.warning("⚠️ Unsaved changes will be lost!")
            else:
                # Second state - show confirmation buttons
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button(
                        "✅ Close", key=f"confirm_close_{filename}", type="secondary"
                    ):
                        # Close the file
                        del st.session_state.editor_open_files[file_path]
                        self._save_to_url()
                        # Clean up confirmation state
                        if confirm_key in st.session_state:
                            del st.session_state[confirm_key]
                        # Clean up any related editor states
                        self._cleanup_editor_states(filename)
                        st.success(f"Closed {filename}")
                        st.rerun()

                with col_b:
                    if st.button("❌ Cancel", key=f"cancel_close_{filename}"):
                        # Cancel close operation
                        st.session_state[confirm_key] = False
                        st.rerun()
        else:
            # No unsaved changes - close immediately
            if st.button("🗙 Close", key=f"close_{filename}"):
                del st.session_state.editor_open_files[file_path]
                self._save_to_url()
                self._cleanup_editor_states(filename)
                st.success(f"Closed {filename}")
                st.rerun()

    def _cleanup_editor_states(self, filename: str):
        """Clean up editor-related session states for a file"""
        keys_to_remove = []
        for key in st.session_state.keys():
            if (
                isinstance(key, str)
                and filename in key
                and any(
                    prefix in key
                    for prefix in [
                        "editor_value_",
                        "confirm_close_",
                        "ai_prompt_",
                        "ai_model_",
                        "ai_context_",
                    ]
                )
            ):
                keys_to_remove.append(key)

        for key in keys_to_remove:
            try:
                del st.session_state[key]
            except KeyError:
                pass  # Key might have been deleted already

    def render_multi_file_editor(
        self, project_path: str, project_name: str = "Default"
    ):
        """Render multi-file tabbed editor interface"""
        st.header("📝 Code Editor")

        # Ensure editor_open_files exists
        if "editor_open_files" not in st.session_state:
            st.session_state.editor_open_files = {}

        # Sync URL with open files (ensure URL always reflects current state)
        open_files = list(st.session_state.editor_open_files.keys())
        current_url_file = st.query_params.get("file", "")
        if open_files:
            first_file = str(Path(open_files[0]).resolve())
            if current_url_file != first_file:
                st.query_params["file"] = first_file
        elif current_url_file:
            # No files open but URL has one - will be restored below
            pass

        # Restore file from URL if not already open (URL is source of truth)
        file_param = st.query_params.get("file", "")
        if file_param:
            file_path = urllib.parse.unquote(file_param)
            file_path = str(Path(file_path).resolve())  # Normalize to absolute path

            # Restore if not already in open files
            if file_path not in st.session_state.editor_open_files:
                path = Path(file_path)
                if path.exists() and path.is_file():
                    try:
                        content = path.read_text(encoding="utf-8", errors="replace")
                        st.session_state.editor_open_files[file_path] = {
                            "original_content": content,
                            "current_content": content,
                            "language": self.get_language_from_extension(file_path),
                            "has_unsaved_changes": False,
                            "has_ai_suggestions": False,
                            "ai_suggested_content": None,
                            "is_binary": False,
                        }
                        st.toast(f"Restored: {path.name}", icon="📂")

                        # Auto-expand folder containing this file in browser
                        if "browser_expanded_dirs" not in st.session_state:
                            st.session_state.browser_expanded_dirs = set()

                        # Try to get relative folder path
                        try:
                            rel_path = path.parent
                            parts = str(rel_path).replace("\\", "/").split("/")
                            for i in range(1, len(parts) + 1):
                                partial = "/".join(parts[:i])
                                if partial and partial not in [".", ".."]:
                                    st.session_state.browser_expanded_dirs.add(partial)
                        except Exception:
                            pass

                    except Exception as e:
                        st.warning(f"Could not restore file: {e}")

        # File tabs
        if st.session_state.editor_open_files:
            # Create file tabs
            file_paths = list(st.session_state.editor_open_files.keys())
            file_names = []

            for fp in file_paths:
                name = Path(fp).name
                if st.session_state.editor_open_files[fp].get("has_unsaved_changes"):
                    name += " ●"
                if st.session_state.editor_open_files[fp].get("has_ai_suggestions"):
                    name += " 🤖"
                file_names.append(name)

            # Add the "+" button as a tab
            tab_names = file_names + ["➕ Open File"]
            tabs = st.tabs(tab_names)

            # Render content for each file tab
            for i, (file_path, tab) in enumerate(zip(file_paths, tabs[:-1])):
                with tab:
                    self.render_editor_interface(file_path, project_name)

            # Handle the "+" tab for opening new files
            with tabs[-1]:
                st.write(
                    "Select a file from the browser on the left to open it in the editor."
                )

        else:
            st.info(
                "No files open. Use the file browser on the left to open files for editing."
            )

        return len(st.session_state.editor_open_files) > 0

    def open_file_in_editor(self, file_path: str) -> bool:
        """Open a file in the editor"""
        file_path = str(Path(file_path).resolve())  # Normalize to absolute path

        # Check if file is already open
        if file_path in st.session_state.editor_open_files:
            st.info(f"File already open: {Path(file_path).name}")
            return False

        # Read the file content
        file_content = self.file_editor.read_file_content(file_path)

        if "error" in file_content:
            st.error(f"Failed to open file: {file_content['error']}")
            return False

        # Add to open files in session state
        st.session_state.editor_open_files[file_path] = {
            "original_content": file_content["content"],
            "current_content": file_content["content"],
            "has_unsaved_changes": False,
            "has_ai_suggestions": False,
            "ai_suggested_content": None,
            "language": self.get_language_from_extension(file_path),
            "is_binary": file_content.get("is_binary", False),
        }

        # Save to URL for persistence
        self._save_to_url()

        return True
