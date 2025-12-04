#!/usr/bin/env python3
"""
Basic import tests for CI/CD pipeline.
Tests that all modules can be imported without errors.
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_core_imports():
    """Test core module imports"""
    from src.core.prompts import SYSTEM_PROMPTS, AGENT_MODES
    assert "General" in AGENT_MODES
    assert "FAUST" in AGENT_MODES
    assert "JUCE" in AGENT_MODES
    assert "Math" in AGENT_MODES
    assert "Physics" in AGENT_MODES


def test_agent_modes_structure():
    """Test agent modes have required fields"""
    from src.core.prompts import AGENT_MODES

    required_fields = ["name", "icon", "description", "file_prefix", "system_prompt_addon"]

    for mode_name, mode_config in AGENT_MODES.items():
        for field in required_fields:
            assert field in mode_config, f"{mode_name} missing field: {field}"


def test_project_structure():
    """Test required directories exist"""
    project_root = Path(__file__).parent.parent

    required_dirs = ["src", "src/core", "src/ui"]
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        assert dir_path.exists(), f"Missing directory: {dir_name}"


def test_main_files_exist():
    """Test main application files exist"""
    project_root = Path(__file__).parent.parent

    required_files = [
        "main.py",
        "src/core/multi_model_system.py",
        "src/core/prompts.py",
        "src/ui/ui_components.py",
        "src/ui/editor_ui.py",
    ]

    for file_name in required_files:
        file_path = project_root / file_name
        assert file_path.exists(), f"Missing file: {file_name}"


if __name__ == "__main__":
    test_core_imports()
    test_agent_modes_structure()
    test_project_structure()
    test_main_files_exist()
    print("All tests passed!")
