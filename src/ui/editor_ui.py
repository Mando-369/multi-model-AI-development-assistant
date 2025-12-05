import streamlit as st
from streamlit_ace import st_ace
from pathlib import Path
from typing import Dict, List, Optional
import difflib
import re
import hashlib
from src.core.prompts import AGENT_MODES


class EditorUI:
    def __init__(self, file_editor, multi_glm_system):
        self.file_editor = file_editor
        self.multi_glm_system = multi_glm_system

        # Initialize open_files in session state if not present
        if "editor_open_files" not in st.session_state:
            st.session_state.editor_open_files = {}

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
            ".dsp": "c_cpp",  # FAUST files - use C++ as closest syntax (has similar operators)
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

        # Ensure file_path is a string
        file_path = str(file_path)

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
            st.markdown("""
            <style>
            /* FAUST syntax highlighting - Monaco Editor vs-dark theme inspired */
            .ace_editor {
                font-family: 'Consolas', 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
                background-color: #1e1e1e !important;
            }
            /* Comments - green like in Monaco */
            .ace_editor .ace_comment {
                color: #6A9955 !important;
                font-style: italic !important;
            }
            /* Strings - reddish/orange like Monaco */
            .ace_editor .ace_string {
                color: #CE9178 !important;
            }
            /* Numbers - light green like Monaco */
            .ace_editor .ace_constant.ace_numeric {
                color: #B5CEA8 !important;
            }
            /* Keywords - blue like Monaco (import, declare, process, with, etc.) */
            .ace_editor .ace_keyword {
                color: #569CD6 !important;
                font-weight: bold !important;
            }
            /* Identifiers and variables - light gray */
            .ace_editor .ace_identifier {
                color: #D4D4D4 !important;
            }
            /* Functions - yellow like Monaco */
            .ace_editor .ace_support.ace_function {
                color: #DCDCAA !important;
            }
            /* Function names and method calls */
            .ace_editor .ace_entity.ace_name.ace_function {
                color: #DCDCAA !important;
            }
            /* Parentheses and brackets */
            .ace_editor .ace_paren {
                color: #D4D4D4 !important;
            }
            /* Operators and punctuation - light gray */
            .ace_editor .ace_punctuation.ace_operator {
                color: #D4D4D4 !important;
            }
            /* Types and classes - light blue/teal */
            .ace_editor .ace_support.ace_type {
                color: #4EC9B0 !important;
            }
            /* Constants and built-ins */
            .ace_editor .ace_support.ace_constant {
                color: #4FC1FF !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Add informational note about FAUST highlighting
            st.info("🎵 **FAUST file detected** - Using Monaco Editor-inspired color scheme with C++ syntax highlighting for optimal FAUST code readability.")

        # Store the content in a separate session state key for the editor
        editor_value_key = f"editor_value_{file_hash}"
        if (
            editor_value_key not in st.session_state
            or st.session_state[editor_value_key] != content_to_display
        ):
            st.session_state[editor_value_key] = content_to_display

        try:
            # Use st_ace with proper configuration
            editor_content = st_ace(
                value=st.session_state[editor_value_key],  # Use session state value
                language=file_data.get("language", "text"),
                theme=self.get_editor_theme(),
                key=editor_key,
                height=1400,
                font_size=14,
                tab_size=4,
                wrap=False,
                auto_update=False,  # Important: set to False
                show_gutter=True,
                show_print_margin=True,
                annotations=None,  # Simplify for now
            )

            # Update content if changed
            if editor_content is not None and editor_content != "":
                # Only update if actually changed
                if editor_content != file_data["current_content"]:
                    st.session_state.editor_open_files[file_path][
                        "current_content"
                    ] = editor_content
                    st.session_state.editor_open_files[file_path][
                        "has_unsaved_changes"
                    ] = True
                    st.session_state[editor_value_key] = editor_content

        except Exception as e:
            st.error(f"Editor error: {e}")
            # Fallback to text_area
            st.warning("Using fallback text editor")
            editor_content = st.text_area(
                "Edit File (Fallback Mode)",
                value=content_to_display,
                height=1400,
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
                placeholder="""Examples:
                    • Add comments to explain the code
                    • Optimize this function for performance
                    • Convert this C++ code to Python
                    • Add error handling
                    • Fix any bugs you find
                    • Refactor this code to be more readable""",
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
        file_path = str(file_path)
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
        file_path = str(file_path)
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
        file_path = str(file_path)
        st.write("---")
        col1, col2, col3, col4, col5 = st.columns(5)

        file_data = st.session_state.editor_open_files[file_path]
        filename = Path(file_path).name

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
        file_path = str(file_path)

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

        # Debug output
        st.success(
            f"✅ Opened: {Path(file_path).name} ({len(file_content['content'])} chars)"
        )

        return True
