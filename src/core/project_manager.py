import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set


class ProjectManager:
    def __init__(self):
        self.projects_dir = Path("./projects")
        self.projects_dir.mkdir(exist_ok=True)

    def get_project_list(self):
        """Get list of available projects"""
        projects = ["Default"]  # Always have a default project

        for project_dir in self.projects_dir.iterdir():
            if project_dir.is_dir() and project_dir.name != "Default":
                projects.append(project_dir.name)

        return sorted(projects)

    def create_project(self, project_name):
        """Create a new project"""
        if not project_name or project_name.strip() == "":
            return False, "Project name cannot be empty"

        project_path = self.projects_dir / project_name.strip()
        if project_path.exists():
            return False, f"Project '{project_name}' already exists"

        try:
            project_path.mkdir(parents=True, exist_ok=True)
            metadata = {
                "name": project_name,
                "created": datetime.now().isoformat(),
                "description": "",
                "models_used": [],
                "files": {
                    "included": [],
                    "excluded": [],
                    "include_patterns": [
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
                    ],
                    "exclude_patterns": [
                        "__pycache__",
                        "*.pyc",
                        ".git",
                        "node_modules",
                        "*.exe",
                        "*.dll",
                        "*.so",
                        "*.dylib",
                    ],
                },
                "editor_settings": {
                    "theme": "monokai",
                    "font_size": 14,
                    "tab_size": 4,
                    "wrap_lines": False,
                },
            }

            with open(project_path / "project_metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)

            return True, f"Project '{project_name}' created successfully"

        except Exception as e:
            return False, f"Error creating project: {e}"

    def get_project_path(self, project_name: str) -> str:
        """Get the file system path for a project"""
        if project_name == "Default":
            return str(Path.cwd())
        else:
            return str(self.projects_dir / project_name)

    def get_project_metadata(self, project_name: str) -> Dict:
        """Get project metadata"""
        if project_name == "Default":
            # Return default metadata for the default project
            return {
                "name": "Default",
                "created": datetime.now().isoformat(),
                "description": "Default workspace project",
                "models_used": [],
                "files": {
                    "included": [],
                    "excluded": [],
                    "include_patterns": [
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
                    ],
                    "exclude_patterns": [
                        "__pycache__",
                        "*.pyc",
                        ".git",
                        "node_modules",
                        "*.exe",
                        "*.dll",
                        "*.so",
                        "*.dylib",
                    ],
                },
                "editor_settings": {
                    "theme": "monokai",
                    "font_size": 14,
                    "tab_size": 4,
                    "wrap_lines": False,
                },
            }

        project_path = self.projects_dir / project_name
        metadata_file = project_path / "project_metadata.json"

        if not metadata_file.exists():
            # Create default metadata if it doesn't exist
            return self.create_default_metadata(project_name)

        try:
            with open(metadata_file, "r") as f:
                return json.load(f)
        except Exception:
            return self.create_default_metadata(project_name)

    def create_default_metadata(self, project_name: str) -> Dict:
        """Create default metadata for a project"""
        metadata = {
            "name": project_name,
            "created": datetime.now().isoformat(),
            "description": "",
            "models_used": [],
            "files": {
                "included": [],
                "excluded": [],
                "include_patterns": [
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
                ],
                "exclude_patterns": [
                    "__pycache__",
                    "*.pyc",
                    ".git",
                    "node_modules",
                    "*.exe",
                    "*.dll",
                    "*.so",
                    "*.dylib",
                ],
            },
            "editor_settings": {
                "theme": "monokai",
                "font_size": 14,
                "tab_size": 4,
                "wrap_lines": False,
            },
        }

        # Save the metadata
        project_path = self.projects_dir / project_name
        project_path.mkdir(parents=True, exist_ok=True)

        with open(project_path / "project_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        return metadata

    def update_project_metadata(self, project_name: str, metadata: Dict) -> bool:
        """Update project metadata"""
        if project_name == "Default":
            return True  # Don't save metadata for default project

        try:
            project_path = self.projects_dir / project_name
            project_path.mkdir(parents=True, exist_ok=True)

            with open(project_path / "project_metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)

            return True
        except Exception:
            return False

    def update_file_patterns(
        self,
        project_name: str,
        include_patterns: List[str],
        exclude_patterns: List[str],
    ) -> bool:
        """Update file include/exclude patterns for a project"""
        metadata = self.get_project_metadata(project_name)

        # Ensure 'files' key exists
        if "files" not in metadata:
            metadata["files"] = {
                "included": [],
                "excluded": [],
                "include_patterns": [],
                "exclude_patterns": [],
            }

        # Ensure the patterns are lists
        metadata["files"]["include_patterns"] = (
            list(include_patterns) if include_patterns else []
        )
        metadata["files"]["exclude_patterns"] = (
            list(exclude_patterns) if exclude_patterns else []
        )

        # Add timestamp to main metadata, not files
        metadata["last_updated"] = datetime.now().isoformat()

        return self.update_project_metadata(project_name, metadata)

    def add_included_file(self, project_name: str, file_path: str) -> bool:
        """Add a file to the project's included files list"""
        metadata = self.get_project_metadata(project_name)

        if file_path not in metadata["files"]["included"]:
            metadata["files"]["included"].append(file_path)

            # Remove from excluded if it's there
            if file_path in metadata["files"]["excluded"]:
                metadata["files"]["excluded"].remove(file_path)

            return self.update_project_metadata(project_name, metadata)

        return True

    def add_excluded_file(self, project_name: str, file_path: str) -> bool:
        """Add a file to the project's excluded files list"""
        metadata = self.get_project_metadata(project_name)

        if file_path not in metadata["files"]["excluded"]:
            metadata["files"]["excluded"].append(file_path)

            # Remove from included if it's there
            if file_path in metadata["files"]["included"]:
                metadata["files"]["included"].remove(file_path)

            return self.update_project_metadata(project_name, metadata)

        return True

    def remove_file_from_project(self, project_name: str, file_path: str) -> bool:
        """Remove a file from both included and excluded lists"""
        metadata = self.get_project_metadata(project_name)

        removed = False
        if file_path in metadata["files"]["included"]:
            metadata["files"]["included"].remove(file_path)
            removed = True

        if file_path in metadata["files"]["excluded"]:
            metadata["files"]["excluded"].remove(file_path)
            removed = True

        if removed:
            return self.update_project_metadata(project_name, metadata)

        return True

    def get_project_files(self, project_name: str) -> Dict[str, List[str]]:
        """Get included and excluded files for a project"""
        metadata = self.get_project_metadata(project_name)
        return {
            "included": metadata["files"].get("included", []),
            "excluded": metadata["files"].get("excluded", []),
            "include_patterns": metadata["files"].get("include_patterns", []),
            "exclude_patterns": metadata["files"].get("exclude_patterns", []),
        }

    def update_editor_settings(self, project_name: str, settings: Dict) -> bool:
        """Update editor settings for a project"""
        metadata = self.get_project_metadata(project_name)
        metadata["editor_settings"].update(settings)
        return self.update_project_metadata(project_name, metadata)

    def get_editor_settings(self, project_name: str) -> Dict:
        """Get editor settings for a project"""
        metadata = self.get_project_metadata(project_name)
        return metadata.get(
            "editor_settings",
            {"theme": "monokai", "font_size": 14, "tab_size": 4, "wrap_lines": False},
        )

    def get_project_context(self, project_name):
        """Get comprehensive project context for enhanced responses"""
        if project_name == "Default":
            return "Working in Default project (current directory)"

        try:
            project_path = self.projects_dir / project_name
            if not project_path.exists():
                return f"Project '{project_name}' directory not found"

            context_parts = []

            # Project metadata
            metadata = self.get_project_metadata(project_name)
            if metadata:
                context_parts.append(f"Project: {project_name}")
                if metadata.get("description"):
                    context_parts.append(f"Description: {metadata['description']}")

                models_used = metadata.get("models_used", [])
                if models_used:
                    context_parts.append(f"Models used: {', '.join(models_used)}")

            # Recent chat context from saved files
            recent_conversations = []
            chat_count = 0

            for chat_file in project_path.glob("*_chat.json"):
                try:
                    with open(chat_file, "r", encoding="utf-8") as f:
                        chats = json.load(f)

                    # Get last 2 conversations per model for broader context
                    model_name = chat_file.stem.replace("_chat", "").replace("_", " ")
                    recent_chats = chats[-2:] if len(chats) >= 2 else chats

                    for chat in recent_chats:
                        chat_count += 1
                        # Include more of the question and answer for better context
                        question = chat["question"][:200] + (
                            "..." if len(chat["question"]) > 200 else ""
                        )
                        answer = chat["answer"][:300] + (
                            "..." if len(chat["answer"]) > 300 else ""
                        )

                        recent_conversations.append(f"Previous Q: {question}")
                        recent_conversations.append(f"Previous A: {answer}")
                        recent_conversations.append("")  # spacing

                except Exception as e:
                    print(f"Error reading {chat_file}: {e}")
                    continue

            if recent_conversations:
                context_parts.append("Recent project discussions:")
                context_parts.extend(
                    recent_conversations[-10:]
                )  # Last 10 items to avoid too much context

            # File information
            try:
                files_info = self.get_project_files(project_name)
                include_patterns = files_info.get("include_patterns", [])
                if include_patterns:
                    context_parts.append(
                        f"File types in project: {', '.join(include_patterns)}"
                    )
            except:
                pass

            final_context = "\n".join(context_parts)
            print(
                f"📋 Project context for {project_name}: {len(final_context)} chars, {chat_count} recent conversations"
            )

            return final_context

        except Exception as e:
            print(f"Error getting project context: {e}")
            return f"Error loading context for project '{project_name}'"

    def save_chat_to_project(self, project_name, model_name, question, answer):
        """Save chat to specific project with better error handling"""
        try:
            project_path = self.projects_dir / project_name
            project_path.mkdir(parents=True, exist_ok=True)

            clean_model_name = (
                model_name.replace(" ", "_")
                .replace("(", "")
                .replace(")", "")
                .replace("&", "and")
                .replace(",", "")
                .replace("-", "_")
                .replace(":", "_")
            )

            chat_file = project_path / f"{clean_model_name}_chat.json"

            # Load existing chats
            chats = []
            if chat_file.exists():
                try:
                    with open(chat_file, "r", encoding="utf-8") as f:
                        chats = json.load(f)
                except Exception as e:
                    print(f"Error loading existing chats: {e}")
                    chats = []

            # Add new chat
            new_chat = {
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "answer": answer,
                "model": model_name,
            }

            chats.append(new_chat)

            # Keep only last 50 chats per model (reduced from 100 for better performance)
            if len(chats) > 50:
                chats = chats[-50:]

            # Save updated chats
            with open(chat_file, "w", encoding="utf-8") as f:
                json.dump(chats, f, indent=2, ensure_ascii=False)

            print(f"✅ Saved chat to {project_name}/{clean_model_name}_chat.json")

        except Exception as e:
            print(f"❌ Error saving chat to project: {e}")

    def load_project_chats(self, project_name, model_name):
        """Load chats for specific project and model with better error handling"""
        try:
            project_path = self.projects_dir / project_name

            clean_model_name = (
                model_name.replace(" ", "_")
                .replace("(", "")
                .replace(")", "")
                .replace("&", "and")
                .replace(",", "")
                .replace("-", "_")
                .replace(":", "_")
            )

            chat_file = project_path / f"{clean_model_name}_chat.json"

            if not chat_file.exists():
                print(f"📝 No previous chats found for {model_name} in {project_name}")
                return []

            with open(chat_file, "r", encoding="utf-8") as f:
                chats = json.load(f)

            chat_pairs = [(chat["question"], chat["answer"]) for chat in chats]
            print(
                f"📚 Loaded {len(chat_pairs)} previous conversations for {model_name}"
            )

            return chat_pairs

        except Exception as e:
            print(f"❌ Error loading project chats: {e}")
            return []

    def delete_project(self, project_name):
        """Delete a project and all its data"""
        if project_name == "Default":
            return False, "Cannot delete the Default project"

        try:
            project_path = self.projects_dir / project_name
            if project_path.exists():
                shutil.rmtree(project_path)
                return True, f"Project '{project_name}' deleted successfully"
            else:
                return False, f"Project '{project_name}' not found"
        except Exception as e:
            return False, f"Error deleting project: {e}"

    def get_project_stats(self, project_name: str) -> Dict:
        """Get statistics about a project"""
        metadata = self.get_project_metadata(project_name)
        project_path = Path(self.get_project_path(project_name))

        stats = {
            "name": project_name,
            "created": metadata.get("created", "Unknown"),
            "total_files": 0,
            "included_files": len(metadata["files"].get("included", [])),
            "excluded_files": len(metadata["files"].get("excluded", [])),
            "models_used": len(set(metadata.get("models_used", []))),
            "last_activity": "Unknown",
        }

        # Count total files if project path exists
        if project_path.exists():
            try:
                all_files = list(project_path.rglob("*"))
                stats["total_files"] = len([f for f in all_files if f.is_file()])

                # Get last activity from chat files
                chat_files = list(
                    (self.projects_dir / project_name).glob("*_chat.json")
                )
                if chat_files:
                    last_modified = max(f.stat().st_mtime for f in chat_files)
                    stats["last_activity"] = datetime.fromtimestamp(
                        last_modified
                    ).isoformat()
            except:
                pass

        return stats
