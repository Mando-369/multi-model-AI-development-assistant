import streamlit as st
from pathlib import Path
from typing import Dict, List, Set, Optional
import os
import platform
import datetime


class FileBrowser:
    def __init__(self, file_editor):
        self.file_editor = file_editor
        self.expanded_dirs = set()
        self.selected_files = set()

    def get_file_icon(self, file_path: str) -> str:
        """Get appropriate emoji icon for file type"""
        ext = Path(file_path).suffix.lower()

        icon_map = {
            # Programming files
            ".py": "🐍",
            ".cpp": "💻",
            ".cc": "💻",
            ".cxx": "💻",
            ".h": "📄",
            ".hpp": "📄",
            ".hxx": "📄",
            ".c": "🔧",
            ".js": "🌐",
            ".ts": "🌐",
            ".java": "☕",
            ".cs": "🔷",
            ".go": "🔵",
            ".rs": "🦀",
            # DSP and Audio
            ".dsp": "🎵",
            ".fst": "🎵",
            ".lib": "📚",
            ".wav": "🎵",
            ".mp3": "🎵",
            ".flac": "🎵",
            # JUCE
            ".jucer": "🎛️",
            # Documentation
            ".md": "📝",
            ".txt": "📄",
            ".pdf": "📕",
            ".doc": "📘",
            ".docx": "📘",
            # Data files
            ".json": "📋",
            ".xml": "📋",
            ".yaml": "📋",
            ".yml": "📋",
            ".csv": "📊",
            ".xlsx": "📊",
            # Images
            ".png": "🖼️",
            ".jpg": "🖼️",
            ".jpeg": "🖼️",
            ".gif": "🖼️",
            ".svg": "🎨",
            ".ico": "🎨",
            # Config files
            ".ini": "⚙️",
            ".conf": "⚙️",
            ".cfg": "⚙️",
            ".toml": "⚙️",
            # Build files
            ".cmake": "🔨",
            ".make": "🔨",
            ".gradle": "🔨",
            ".pro": "🔨",  # Qt project files
        }

        return icon_map.get(ext, "📄")

    def get_directory_icon(self, dir_name: str, has_children: bool = True) -> str:
        """Get appropriate icon for directory"""
        dir_name_lower = dir_name.lower()

        special_dirs = {
            "src": "📂",
            "source": "📂",
            "include": "📁",
            "headers": "📁",
            "lib": "📚",
            "libs": "📚",
            "library": "📚",
            "bin": "⚙️",
            "build": "⚙️",
            "test": "🧪",
            "tests": "🧪",
            "doc": "📖",
            "docs": "📖",
            "documentation": "📖",
            "examples": "📋",
            "example": "📋",
            "resources": "🗂️",
            "assets": "🗂️",
            "config": "⚙️",
            "scripts": "📜",
            "data": "📊",
            "images": "🖼️",
            "img": "🖼️",
            "audio": "🎵",
            "faust": "🎵",
            "cpp": "💻",
            "python": "🐍",
            "juce": "🎛️",
            "dsp": "🔊",
        }

        for key, icon in special_dirs.items():
            if key in dir_name_lower:
                return icon

        return "📁" if has_children else "📄"

    def render_file_tree(
        self,
        project_path: str,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
    ) -> Optional[str]:
        """Render interactive file tree and return selected file path"""

        # Initialize show_all_files state if needed
        if "show_all_files" not in st.session_state:
            st.session_state["show_all_files"] = False

        # Get project files structure
        files_data = self.file_editor.get_project_files(
            project_path, include_patterns, exclude_patterns
        )

        if "error" in files_data:
            st.error(files_data["error"])
            return None

        # Display project stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📁 Total Files", files_data["total_files"])
        with col2:
            st.metric("✅ Included Files", files_data["included_files"])
        with col3:
            st.metric("📂 Directories", self._count_directories(files_data))

        # Instructions
        st.info("💡 **Click on any file name to open it in the editor**")

        # Row 1: Folder controls - Expand, Collapse, Show All Files
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📂 Expand All", key="expand_all_dirs", use_container_width=True):
                self._expand_all_directories(files_data, project_path)
                st.rerun()

        with col2:
            if st.button("📁 Collapse All", key="collapse_all_dirs", use_container_width=True):
                self.expanded_dirs.clear()
                st.rerun()

        with col3:
            show_all_current = st.session_state.get("show_all_files", False)
            button_label = "✅ Show All Files" if show_all_current else "👁️ Show All Files"
            if st.button(button_label, key="show_all_btn", use_container_width=True):
                st.session_state["show_all_files"] = not show_all_current
                st.rerun()

        # Row 2: Sorting controls
        col1, col2 = st.columns(2)

        with col1:
            sort_by = st.selectbox(
                "📊 Sort files by:",
                ["name", "type", "date", "size"],
                key="file_sort_method",
            )

        with col2:
            sort_order = st.selectbox(
                "🔄 Order:",
                ["asc", "desc"],
                format_func=lambda x: "↑ Ascending" if x == "asc" else "↓ Descending",
                key="file_sort_order",
            )

        st.write("---")

        # Render tree structure
        selected_file = self._render_directory_level(
            files_data, project_path, "", is_root=True, sort_by=sort_by, sort_order=sort_order
        )

        return selected_file

    def _render_directory_level(
        self,
        files_data: Dict,
        project_path: str,
        current_path: str,
        is_root: bool = False,
        indent_level: int = 0,
        sort_by: str = "name",
        sort_order: str = "asc",
    ) -> Optional[str]:
        """Recursively render directory tree level with sorting"""
        selected_file = None

        # Indentation for visual hierarchy
        indent = "　" * indent_level  # Using full-width space for better alignment

        # Render files in current directory
        files_list = files_data.get("files", [])
        
        # Sort files based on criteria
        files_list = self._sort_files(files_list, sort_by, sort_order)
        
        for file_info in files_list:
            file_path = file_info["path"]
            file_name = file_info["name"]
            file_size = file_info["size"]

            # Format file size
            if file_size < 1024:
                size_str = f"{file_size}B"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size//1024}KB"
            else:
                size_str = f"{file_size//(1024*1024)}MB"

            # Create file button with right-aligned layout and proper indentation
            col1, col2 = st.columns([3.5, 1])
            with col1:
                button_key = f"file_{file_path.replace('/', '_').replace('\\', '_').replace('.', '_')}"
                file_display = f"{indent}{self.get_file_icon(file_name)} {file_name}"
                if st.button(
                    file_display,
                    key=button_key,
                    help=f"Click to open • {size_str} • Modified: {file_info.get('modified', 'Unknown')}",
                    use_container_width=True,
                ):
                    selected_file = file_path
            with col2:
                # File metadata on the right
                st.markdown(f"<div style='text-align: right; color: #888; font-size: 0.8em; padding-top: 8px;'>{size_str}</div>", 
                           unsafe_allow_html=True)

        # Render subdirectories
        directories = files_data.get("directories", {})
        for dir_name, dir_data in directories.items():
            dir_path = (
                os.path.join(current_path, dir_name) if current_path else dir_name
            )

            # Count items in directory
            file_count = len(dir_data.get("files", []))
            dir_count = len(dir_data.get("directories", {}))

            # Determine if expanded
            is_expanded = dir_path in self.expanded_dirs

            # Directory header button with right-aligned layout and proper indentation
            col1, col2 = st.columns([3.5, 1])
            with col1:
                # Toggle expand/collapse
                expand_icon = "▼" if is_expanded else "▶"
                dir_icon = self.get_directory_icon(
                    dir_name, dir_count > 0 or file_count > 0
                )

                button_key = f"dir_{dir_path.replace('/', '_').replace('\\', '_').replace('.', '_')}"
                dir_display = f"{indent}{expand_icon} {dir_icon} {dir_name}/"
                if st.button(
                    dir_display,
                    key=button_key,
                    help=f"Click to {'collapse' if is_expanded else 'expand'} • {file_count} files, {dir_count} folders",
                    use_container_width=True,
                ):
                    if is_expanded:
                        self.expanded_dirs.discard(dir_path)
                    else:
                        self.expanded_dirs.add(dir_path)
                    st.rerun()
            with col2:
                st.markdown(f"<div style='text-align: right; color: #888; font-size: 0.8em; padding-top: 8px;'>📄{file_count} 📁{dir_count}</div>", 
                           unsafe_allow_html=True)

            # Render contents if expanded
            if is_expanded:
                sub_selected = self._render_directory_level(
                    dir_data, project_path, dir_path, False, indent_level + 1, sort_by, sort_order
                )
                if sub_selected:
                    selected_file = sub_selected

        return selected_file

    def _sort_files(self, files_list: List[Dict], sort_by: str, sort_order: str) -> List[Dict]:
        """Sort files based on specified criteria"""
        reverse = sort_order == "desc"
        
        if sort_by == "name":
            return sorted(files_list, key=lambda f: f["name"].lower(), reverse=reverse)
        elif sort_by == "type":
            return sorted(files_list, key=lambda f: (Path(f["name"]).suffix.lower(), f["name"].lower()), reverse=reverse)
        elif sort_by == "size":
            return sorted(files_list, key=lambda f: f["size"], reverse=reverse)
        elif sort_by == "date":
            return sorted(files_list, key=lambda f: f.get("modified", 0), reverse=reverse)
        else:
            return files_list

    def _count_directories(self, files_data: Dict) -> int:
        """Count total directories recursively"""
        count = len(files_data.get("directories", {}))
        for dir_data in files_data.get("directories", {}).values():
            count += self._count_directories(dir_data)
        return count

    def _expand_all_directories(
        self, files_data: Dict, project_path: str, current_path: str = ""
    ):
        """Recursively add all directory paths to expanded_dirs"""
        directories = files_data.get("directories", {})
        for dir_name, dir_data in directories.items():
            dir_path = (
                os.path.join(current_path, dir_name) if current_path else dir_name
            )
            self.expanded_dirs.add(dir_path)
            self._expand_all_directories(dir_data, project_path, dir_path)

    def render_folder_picker(self):
        """Render an interactive folder picker dialog"""
        st.subheader("📂 Browse for Folder")

        # Initialize current path
        if "folder_picker_path" not in st.session_state:
            st.session_state.folder_picker_path = str(Path.cwd())

        current_path = Path(st.session_state.folder_picker_path)
        if not current_path.exists():
            current_path = Path.cwd()
            st.session_state.folder_picker_path = str(current_path)

        st.markdown(f"**Current Path:** `{current_path}`")

        # Path breadcrumb navigation
        path_parts = current_path.parts
        if len(path_parts) > 1:
            breadcrumb_cols = st.columns(min(len(path_parts), 5))
            for i, (part, col) in enumerate(zip(path_parts[-5:], breadcrumb_cols)):
                with col:
                    if st.button(part[:10], key=f"breadcrumb_{i}", help=part):
                        # Reconstruct path up to this part
                        new_path = Path(*path_parts[: len(path_parts) - 5 + i + 1])
                        st.session_state.folder_picker_path = str(new_path)
                        st.rerun()

        # Quick access buttons
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("⬆️ Parent", help="Go up one level"):
                parent = current_path.parent
                if parent != current_path:
                    st.session_state.folder_picker_path = str(parent)
                    st.rerun()

        with col2:
            if st.button("🏠 Home", help="Go to home directory"):
                st.session_state.folder_picker_path = str(Path.home())
                st.rerun()

        with col3:
            if st.button("📁 Desktop", help="Go to Desktop"):
                desktop = Path.home() / "Desktop"
                if desktop.exists():
                    st.session_state.folder_picker_path = str(desktop)
                    st.rerun()

        with col4:
            if st.button("📄 Documents", help="Go to Documents"):
                docs = Path.home() / "Documents"
                if docs.exists():
                    st.session_state.folder_picker_path = str(docs)
                    st.rerun()

        # Manual path entry
        manual_path = st.text_input(
            "Or enter path manually:",
            placeholder="Type or paste a directory path...",
            key="manual_path_entry",
        )

        if manual_path:
            if Path(manual_path).exists() and Path(manual_path).is_dir():
                if st.button("→ Go", key="go_manual"):
                    st.session_state.folder_picker_path = manual_path
                    st.rerun()
            else:
                st.error("Invalid directory path!")

        st.write("---")

        # List directories in current location
        st.write("**📁 Folders in current location:**")

        try:
            # Get all directories (not hidden)
            directories = [
                d
                for d in current_path.iterdir()
                if d.is_dir() and not d.name.startswith(".")
            ]
            directories.sort(key=lambda x: x.name.lower())

            # Show directories in a scrollable area
            for directory in directories[:30]:  # Limit to 30 for performance
                col1, col2 = st.columns([3, 1])

                with col1:
                    dir_icon = self.get_directory_icon(directory.name)
                    if st.button(
                        f"{dir_icon} {directory.name}",
                        key=f"pick_dir_{directory.name}",
                        use_container_width=True,
                    ):
                        st.session_state.folder_picker_path = str(directory)
                        st.rerun()

                with col2:
                    if st.button("✅", key=f"select_{directory.name}"):
                        return str(directory)

            if len(directories) > 30:
                st.info(f"Showing 30 of {len(directories)} folders")
            elif len(directories) == 0:
                st.info("No subdirectories in this location")

        except PermissionError:
            st.error("Permission denied to read this directory")
        except Exception as e:
            st.error(f"Error reading directory: {e}")

        # Action buttons
        st.write("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("✅ Select Current Folder", type="primary"):
                return str(current_path)

        with col2:
            # Create new folder option
            new_folder_name = st.text_input("New folder name:", key="new_folder_picker")
            if new_folder_name and st.button("📁 Create"):
                new_path = current_path / new_folder_name
                try:
                    new_path.mkdir(exist_ok=False)
                    return str(new_path)
                except Exception as e:
                    st.error(f"Error creating folder: {e}")

        with col3:
            if st.button("❌ Cancel"):
                return "CANCEL"

        return None

    def render_file_filter_controls(self):
        """Render file filtering controls"""
        with st.expander("🔍 File Filters", expanded=False):
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Include Patterns:**")
                default_includes = [
                    "*.py",
                    "*.cpp",
                    "*.h",
                    "*.hpp",
                    "*.c",
                    "*.cc",
                    "*.dsp",
                    "*.lib",
                    "*.fst",
                    "*.txt",
                    "*.md",
                    "*.json",
                ]

                include_patterns = st.multiselect(
                    "Include files matching:",
                    default_includes,
                    default=default_includes,
                    key="include_patterns",
                )

                custom_include = st.text_input(
                    "Add custom pattern:",
                    placeholder="e.g., *.xml",
                    key="custom_include",
                )
                if custom_include:
                    include_patterns.append(custom_include)

            with col2:
                st.write("**Exclude Patterns:**")
                default_excludes = [
                    "__pycache__",
                    "*.pyc",
                    ".git",
                    "node_modules",
                    "*.exe",
                    "*.dll",
                    "*.so",
                    "*.dylib",
                    "build",
                    "dist",
                ]

                exclude_patterns = st.multiselect(
                    "Exclude files matching:",
                    default_excludes,
                    default=default_excludes,
                    key="exclude_patterns",
                )

                custom_exclude = st.text_input(
                    "Add custom exclusion:",
                    placeholder="e.g., *.tmp",
                    key="custom_exclude",
                )
                if custom_exclude:
                    exclude_patterns.append(custom_exclude)

        return include_patterns, exclude_patterns

    def render_file_operations(self, project_path: str):
        """Render file operation controls"""
        with st.expander("➕ Create New File", expanded=False):
            col1, col2 = st.columns([2, 1])

            with col1:
                new_file_name = st.text_input(
                    "File name:", placeholder="example.py", key="new_file_name"
                )

            with col2:
                st.write("")  # Spacing
                st.write("")  # Spacing
                if new_file_name and st.button("➕ Create", type="primary"):
                    new_file_path = os.path.join(project_path, new_file_name)
                    result = self.file_editor.create_new_file(new_file_path)

                    if result.get("success"):
                        st.success(result["message"])
                        return result["file_path"]
                    else:
                        st.error(result.get("error", "Unknown error"))

        return None

    def render_project_selector(self, project_manager) -> str:
        """Render project selection with path display"""
        col1, col2 = st.columns([2, 1])

        with col1:
            projects = project_manager.get_project_list()
            selected_project = st.selectbox(
                "📂 Select Project:",
                projects,
                help="Choose which project's files to browse",
            )

        with col2:
            st.write("")  # Spacing
            if st.button("🔄 Refresh", help="Refresh project list"):
                st.rerun()

        # Get and display project path
        if selected_project == "Default":
            project_path = str(Path.cwd())
        else:
            project_path = str(Path("./projects") / selected_project)

            # Ensure project directory exists
            Path(project_path).mkdir(parents=True, exist_ok=True)

        st.info(f"📍 **Path:** `{project_path}`")

        return project_path
