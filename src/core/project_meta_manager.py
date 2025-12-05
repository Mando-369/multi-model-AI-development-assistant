"""Project Meta Manager - Handles PROJECT_META.md operations for strategic planning."""

from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# Project root directory (2 levels up from this file: src/core/project_meta_manager.py)
PROJECT_ROOT = Path(__file__).parent.parent.parent


DEFAULT_PROJECT_META_TEMPLATE = """# Project: {project_name}
Last Updated: {timestamp}
Updated By: auto-created

## Vision & Goals
(Describe the project purpose and success criteria)

## Current Roadmap

| Milestone | Status | Target | Notes |
|-----------|--------|--------|-------|
| Define project scope | planned | - | - |

## Architecture Decisions

| Decision | Date | Rationale | Status |
|----------|------|-----------|--------|
| - | - | - | - |

## Agent Handoffs
(Define which specialist agent handles which aspects)

- **FAUST**: DSP algorithms, signal processing code
- **JUCE**: Plugin architecture, C++ implementation
- **Math**: Algorithm derivations, filter design
- **Physics**: Circuit modeling, acoustics

## Export Queue (Ready for Claude Code)
(Items refined enough for implementation - copy these to your coding tool)

-

## Completed Work
(Historical log of completed milestones and exported items)

-

## Cross-Cutting Concerns
(Shared patterns, conventions, technical debt, notes that span multiple agents)

-
"""


class ProjectMetaManager:
    """Manages PROJECT_META.md operations for project-level strategic planning."""

    def __init__(self):
        self.projects_dir = PROJECT_ROOT / "projects"
        self.projects_dir.mkdir(exist_ok=True)

    def get_meta_path(self, project_name: str) -> Path:
        """Get path to PROJECT_META.md for a project."""
        if project_name == "Default":
            return PROJECT_ROOT / "PROJECT_META.md"
        return self.projects_dir / project_name / "PROJECT_META.md"

    def read_project_meta(self, project_name: str) -> str:
        """Read PROJECT_META.md content.

        Returns:
            Content string, or empty string if not exists.
        """
        if project_name == "Default":
            return ""  # Skip for Default project

        meta_path = self.get_meta_path(project_name)
        if meta_path.exists():
            try:
                return meta_path.read_text(encoding="utf-8")
            except Exception as e:
                print(f"Error reading project meta: {e}")
                return ""
        return ""

    def save_project_meta(
        self,
        project_name: str,
        content: str,
        updated_by: str = "manual"
    ) -> bool:
        """Save PROJECT_META.md with timestamp update.

        Args:
            project_name: Name of the project
            content: New content for the file
            updated_by: Who/what triggered the update (manual/orchestrator/auto-sync)

        Returns:
            True if saved successfully
        """
        if project_name == "Default":
            return False  # Skip for Default project

        try:
            meta_path = self.get_meta_path(project_name)
            meta_path.parent.mkdir(parents=True, exist_ok=True)

            # Update the timestamp and updated_by fields in content
            timestamp = datetime.now().isoformat()
            lines = content.split('\n')
            updated_lines = []

            for line in lines:
                if line.startswith('Last Updated:'):
                    updated_lines.append(f'Last Updated: {timestamp}')
                elif line.startswith('Updated By:'):
                    updated_lines.append(f'Updated By: {updated_by}')
                else:
                    updated_lines.append(line)

            meta_path.write_text('\n'.join(updated_lines), encoding="utf-8")
            print(f"Saved PROJECT_META.md for {project_name} (by {updated_by})")
            return True

        except Exception as e:
            print(f"Error saving project meta: {e}")
            return False

    def create_default_meta(self, project_name: str) -> str:
        """Create default PROJECT_META.md structure for a project.

        Returns:
            The created content
        """
        if project_name == "Default":
            return ""

        timestamp = datetime.now().isoformat()
        content = DEFAULT_PROJECT_META_TEMPLATE.format(
            project_name=project_name,
            timestamp=timestamp
        )

        meta_path = self.get_meta_path(project_name)
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        meta_path.write_text(content, encoding="utf-8")

        print(f"Created default PROJECT_META.md for {project_name}")
        return content

    def ensure_project_meta(self, project_name: str) -> str:
        """Ensure PROJECT_META.md exists, create if not.

        Returns:
            Content of the file (existing or newly created)
        """
        if project_name == "Default":
            return ""

        content = self.read_project_meta(project_name)
        if not content:
            content = self.create_default_meta(project_name)
        return content

    def get_all_agent_metas(self, project_name: str) -> Dict[str, str]:
        """Read all agent context files for a project.

        Returns:
            Dict of {agent_mode: content}
        """
        if project_name == "Default":
            return {}

        agents_dir = self.projects_dir / project_name / "agents"
        if not agents_dir.exists():
            return {}

        agent_metas = {}
        for meta_file in agents_dir.glob("*_context.md"):
            agent_name = meta_file.stem.replace("_context", "").capitalize()
            try:
                content = meta_file.read_text(encoding="utf-8")
                if content.strip():
                    agent_metas[agent_name] = content
            except Exception as e:
                print(f"Error reading {meta_file}: {e}")

        return agent_metas

    def get_last_update_info(self, project_name: str) -> Dict[str, str]:
        """Get last update timestamp and source from PROJECT_META.md.

        Returns:
            Dict with 'timestamp' and 'updated_by' keys
        """
        content = self.read_project_meta(project_name)
        if not content:
            return {"timestamp": "", "updated_by": ""}

        info = {"timestamp": "", "updated_by": ""}
        for line in content.split('\n'):
            if line.startswith('Last Updated:'):
                info["timestamp"] = line.replace('Last Updated:', '').strip()
            elif line.startswith('Updated By:'):
                info["updated_by"] = line.replace('Updated By:', '').strip()

        return info

    def truncate_for_context(self, content: str, max_chars: int = 2000) -> str:
        """Truncate PROJECT_META.md for injection into agent context.

        Prioritizes: Vision & Goals, Current Roadmap, Export Queue

        Args:
            content: Full PROJECT_META.md content
            max_chars: Maximum characters to include

        Returns:
            Truncated content with priority sections
        """
        if len(content) <= max_chars:
            return content

        # Priority sections to keep
        priority_sections = [
            "## Vision & Goals",
            "## Current Roadmap",
            "## Export Queue"
        ]

        lines = content.split('\n')
        result_lines = []
        current_chars = 0
        in_priority_section = False
        current_section = ""

        for line in lines:
            # Check if entering a section
            if line.startswith('## '):
                current_section = line
                in_priority_section = any(ps in line for ps in priority_sections)

            # Always include header lines
            if line.startswith('# Project:') or line.startswith('Last Updated:') or line.startswith('Updated By:'):
                result_lines.append(line)
                current_chars += len(line) + 1
                continue

            # Include priority section content
            if in_priority_section:
                if current_chars + len(line) + 1 > max_chars:
                    result_lines.append("... (truncated)")
                    break
                result_lines.append(line)
                current_chars += len(line) + 1

        return '\n'.join(result_lines)

    def extract_export_queue(self, project_name: str) -> List[str]:
        """Extract items from the Export Queue section.

        Returns:
            List of export queue items
        """
        content = self.read_project_meta(project_name)
        if not content:
            return []

        items = []
        in_export_section = False

        for line in content.split('\n'):
            if '## Export Queue' in line:
                in_export_section = True
                continue
            elif line.startswith('## ') and in_export_section:
                break
            elif in_export_section and line.strip().startswith('-') and line.strip() != '-':
                item = line.strip().lstrip('- ').strip()
                if item:
                    items.append(item)

        return items
