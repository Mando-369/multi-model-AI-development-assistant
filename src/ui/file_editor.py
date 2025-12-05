import os
import shutil
import difflib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json


class FileEditor:
    def __init__(self, project_manager):
        self.project_manager = project_manager
        self.temp_changes = {}  # Store temporary changes before applying
        self.file_states = {}  # Track original file states for diff

    def get_project_files(
        self,
        project_path: str,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
    ) -> Dict:
        """Get all files in a project directory with include/exclude filtering"""
        project_path_obj = Path(project_path)

        if not project_path_obj.exists():
            return {"error": f"Project path {project_path_obj} does not exist"}

        files_structure = {
            "directories": {},
            "files": [],
            "total_files": 0,
            "included_files": 0,
        }

        # Default patterns
        if include_patterns is None:
            include_patterns = [
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
        if exclude_patterns is None:
            exclude_patterns = [
                "__pycache__",
                "*.pyc",
                ".git",
                "node_modules",
                "*.exe",
                "*.dll",
                "*.so",
                "*.dylib",
            ]

        def should_include_file(file_path: Path) -> bool:
            """Check if file should be included based on patterns"""
            file_name = file_path.name
            file_str = str(file_path)

            # Skip hidden files unless explicitly showing all
            if file_name.startswith(".") and "*" not in include_patterns:
                return False

            # Check exclude patterns first
            for pattern in exclude_patterns:
                if pattern.startswith("*"):
                    if file_name.endswith(pattern[1:]):
                        return False
                elif pattern in file_str:
                    return False

            # Check include patterns
            # Handle "*" pattern explicitly - match everything
            if "*" in include_patterns:
                return True

            for pattern in include_patterns:
                if pattern.startswith("*"):
                    if file_name.endswith(pattern[1:]):
                        return True
                elif pattern == file_name:
                    return True

            return False

        # Walk through directory structure
        for root, dirs, files in os.walk(project_path_obj):
            root_path = Path(root)
            relative_root = root_path.relative_to(project_path_obj)

            # Skip excluded directories
            dirs[:] = [
                d for d in dirs if not any(pattern in d for pattern in exclude_patterns)
            ]

            current_level = files_structure["directories"]

            # Create nested directory structure
            if str(relative_root) != ".":
                for part in relative_root.parts:
                    if part not in current_level:
                        current_level[part] = {"directories": {}, "files": []}
                    current_level = current_level[part]["directories"]

            # Add files to current level
            for file_name in files:
                file_path = root_path / file_name
                files_structure["total_files"] += 1

                if should_include_file(file_path):
                    files_structure["included_files"] += 1

                    file_info = {
                        "name": file_name,
                        "path": str(file_path),
                        "relative_path": str(file_path.relative_to(project_path_obj)),
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(
                            file_path.stat().st_mtime
                        ).isoformat(),
                        "extension": file_path.suffix.lower(),
                        "included": True,
                    }

                    # Add to current directory level
                    if str(relative_root) == ".":
                        files_structure["files"].append(file_info)
                    else:
                        # Navigate to correct nested location
                        nested_level = files_structure["directories"]
                        for part in relative_root.parts[:-1]:
                            nested_level = nested_level[part]["directories"]

                        if relative_root.parts[-1] not in nested_level:
                            nested_level[relative_root.parts[-1]] = {
                                "directories": {},
                                "files": [],
                            }
                        nested_level[relative_root.parts[-1]]["files"].append(file_info)

        return files_structure

    def read_file_content(self, file_path: str) -> Dict:
        """Read file content and store original state"""
        try:
            file_path_obj = Path(file_path)

            if not file_path_obj.exists():
                return {"error": f"File {file_path_obj} does not exist"}

            # Try to read as text
            try:
                with open(file_path_obj, "r", encoding="utf-8") as f:
                    content = f.read()

                # Store original state for diff comparison
                self.file_states[file_path] = {
                    "original_content": content,
                    "current_content": content,
                    "has_changes": False,
                    "ai_suggested_content": None,
                    "change_summary": None,
                }

                return {
                    "content": content,
                    "encoding": "utf-8",
                    "size": len(content),
                    "lines": len(content.splitlines()),
                    "file_path": file_path,
                    "is_binary": False,
                }

            except UnicodeDecodeError:
                # Handle binary files
                with open(file_path_obj, "rb") as f:
                    content = f.read()

                return {
                    "content": f"<Binary file - {len(content)} bytes>",
                    "encoding": "binary",
                    "size": len(content),
                    "file_path": file_path,
                    "is_binary": True,
                }

        except Exception as e:
            return {"error": f"Error reading file: {e}"}

    def save_file_content(
        self, file_path: str, content: str, create_backup: bool = True
    ) -> Dict:
        """Save file content with optional backup"""
        try:
            file_path_obj = Path(file_path)

            # Create backup if requested and file exists
            if create_backup and file_path_obj.exists():
                backup_path = file_path_obj.with_suffix(
                    file_path_obj.suffix
                    + f".backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
                shutil.copy2(file_path_obj, backup_path)

            # Save new content
            with open(file_path_obj, "w", encoding="utf-8") as f:
                f.write(content)

            # Update file state
            if file_path in self.file_states:
                self.file_states[file_path]["current_content"] = content
                self.file_states[file_path]["has_changes"] = False
                self.file_states[file_path]["ai_suggested_content"] = None

            return {
                "success": True,
                "message": f"File saved successfully: {file_path_obj.name}",
                "backup_created": create_backup and file_path_obj.exists(),
            }

        except Exception as e:
            return {"error": f"Error saving file: {e}"}

    def apply_ai_suggestion(self, file_path: str, ai_suggested_content: str) -> Dict:
        """Apply AI suggestion and prepare diff for review"""
        if str(file_path) not in self.file_states:
            return {"error": "File not loaded. Please open the file first."}

        file_state = self.file_states[str(file_path)]
        original_content = file_state["original_content"]

        # Generate detailed diff
        diff_data = self.generate_detailed_diff(original_content, ai_suggested_content)

        # Update file state
        file_state["ai_suggested_content"] = ai_suggested_content
        file_state["has_changes"] = True
        file_state["change_summary"] = diff_data["summary"]

        return {
            "success": True,
            "diff": diff_data,
            "changes_count": diff_data["summary"]["total_changes"],
            "ready_for_review": True,
        }

    def generate_detailed_diff(self, original: str, modified: str) -> Dict:
        """Generate detailed diff with line-by-line changes"""
        original_lines = original.splitlines()
        modified_lines = modified.splitlines()

        # Generate unified diff
        unified_diff = list(
            difflib.unified_diff(original_lines, modified_lines, lineterm="", n=3)
        )

        # Generate HTML diff for better visualization
        html_diff = difflib.HtmlDiff()
        html_table = html_diff.make_table(
            original_lines,
            modified_lines,
            "Original",
            "AI Suggested",
            context=True,
            numlines=3,
        )

        # Analyze changes
        changes_summary = {
            "lines_added": 0,
            "lines_removed": 0,
            "lines_modified": 0,
            "total_changes": 0,
        }

        # Count changes from unified diff
        for line in unified_diff:
            if line.startswith("+") and not line.startswith("+++"):
                changes_summary["lines_added"] += 1
            elif line.startswith("-") and not line.startswith("---"):
                changes_summary["lines_removed"] += 1

        # Detect modified lines (lines that appear in both + and -)
        opcodes = list(
            difflib.SequenceMatcher(None, original_lines, modified_lines).get_opcodes()
        )
        for op, i1, i2, j1, j2 in opcodes:
            if op == "replace":
                changes_summary["lines_modified"] += max(i2 - i1, j2 - j1)

        changes_summary["total_changes"] = (
            changes_summary["lines_added"]
            + changes_summary["lines_removed"]
            + changes_summary["lines_modified"]
        )

        # Extract changed sections for highlighting
        changed_sections = []
        for op, i1, i2, j1, j2 in opcodes:
            if op != "equal":
                changed_sections.append(
                    {
                        "operation": op,
                        "original_start": i1,
                        "original_end": i2,
                        "modified_start": j1,
                        "modified_end": j2,
                        "original_lines": (
                            original_lines[i1:i2] if op != "insert" else []
                        ),
                        "modified_lines": (
                            modified_lines[j1:j2] if op != "delete" else []
                        ),
                    }
                )

        return {
            "unified_diff": unified_diff,
            "html_diff": html_table,
            "summary": changes_summary,
            "changed_sections": changed_sections,
            "original_lines": original_lines,
            "modified_lines": modified_lines,
        }

    def get_file_diff_highlights(self, file_path: str) -> Optional[Dict]:
        """Get diff highlights for editor display"""
        if str(file_path) not in self.file_states:
            return None

        file_state = self.file_states[str(file_path)]

        if not file_state["ai_suggested_content"]:
            return None

        diff_data = self.generate_detailed_diff(
            file_state["original_content"], file_state["ai_suggested_content"]
        )

        # Convert to editor-friendly format
        highlights = {"additions": [], "deletions": [], "modifications": []}

        for section in diff_data["changed_sections"]:
            if section["operation"] == "insert":
                highlights["additions"].extend(
                    range(section["modified_start"], section["modified_end"])
                )
            elif section["operation"] == "delete":
                highlights["deletions"].extend(
                    range(section["original_start"], section["original_end"])
                )
            elif section["operation"] == "replace":
                highlights["modifications"].extend(
                    range(section["modified_start"], section["modified_end"])
                )

        return highlights

    def create_new_file(self, file_path: str, content: str = "") -> Dict:
        """Create a new file"""
        try:
            file_path_obj = Path(file_path)

            if file_path_obj.exists():
                return {"error": f"File {file_path_obj} already exists"}

            # Create parent directories if they don't exist
            file_path_obj.parent.mkdir(parents=True, exist_ok=True)

            # Create file with content
            with open(file_path_obj, "w", encoding="utf-8") as f:
                f.write(content)

            return {
                "success": True,
                "message": f"File created successfully: {file_path_obj.name}",
                "file_path": file_path,
            }

        except Exception as e:
            return {"error": f"Error creating file: {e}"}

    def delete_file(self, file_path: str, create_backup: bool = True) -> Dict:
        """Delete a file with optional backup"""
        try:
            file_path_obj = Path(file_path)

            if not file_path_obj.exists():
                return {"error": f"File {file_path_obj} does not exist"}

            # Create backup if requested
            if create_backup:
                backup_path = file_path_obj.with_suffix(
                    file_path_obj.suffix
                    + f".deleted.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
                shutil.move(file_path_obj, backup_path)
                message = f"File moved to backup: {backup_path.name}"
            else:
                file_path_obj.unlink()
                message = f"File deleted: {file_path_obj.name}"

            # Clean up file state
            if file_path in self.file_states:
                del self.file_states[file_path]

            return {
                "success": True,
                "message": message,
                "backup_created": create_backup,
            }

        except Exception as e:
            return {"error": f"Error deleting file: {e}"}
