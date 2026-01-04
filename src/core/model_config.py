"""
Model Configuration Manager

Handles user model selections and persists configuration.
"""

import json
from pathlib import Path
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, asdict, field

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent


@dataclass
class ModelRole:
    """Configuration for a model role (reasoning, fast, etc.)."""
    model_id: str
    backend: str
    display_name: str


@dataclass
class ModelConfig:
    """Complete model configuration."""
    reasoning_model: ModelRole
    fast_model: ModelRole
    # Future: vision_model, embedding_model, etc.

    @classmethod
    def default(cls) -> 'ModelConfig':
        """Create default configuration (backwards compatible with v2.1)."""
        return cls(
            reasoning_model=ModelRole(
                model_id="deepseek-r1:32b",
                backend="ollama",
                display_name="DeepSeek-R1:32B (Reasoning)"
            ),
            fast_model=ModelRole(
                model_id="qwen2.5:32b",
                backend="ollama",
                display_name="Qwen2.5:32B (Fast)"
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "reasoning_model": asdict(self.reasoning_model),
            "fast_model": asdict(self.fast_model),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelConfig':
        """Create from dictionary."""
        return cls(
            reasoning_model=ModelRole(**data.get("reasoning_model", {})),
            fast_model=ModelRole(**data.get("fast_model", {})),
        )


class ModelConfigManager:
    """Manages model configuration persistence and access."""

    CONFIG_FILENAME = "model_config.json"

    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or PROJECT_ROOT
        self.config_path = self.config_dir / self.CONFIG_FILENAME
        self._config: Optional[ModelConfig] = None
        self._load_config()

    def _load_config(self):
        """Load configuration from file or create default."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                self._config = ModelConfig.from_dict(data)
                print(f"Loaded model config from {self.config_path}")
            except Exception as e:
                print(f"Error loading model config: {e}")
                self._config = ModelConfig.default()
        else:
            self._config = ModelConfig.default()
            self._save_config()

    def _save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config.to_dict(), f, indent=2)
            print(f"Saved model config to {self.config_path}")
        except Exception as e:
            print(f"Error saving model config: {e}")

    @property
    def config(self) -> ModelConfig:
        """Get current configuration."""
        if self._config is None:
            self._config = ModelConfig.default()
        return self._config

    def get_reasoning_model(self) -> ModelRole:
        """Get the reasoning model configuration."""
        return self.config.reasoning_model

    def get_fast_model(self) -> ModelRole:
        """Get the fast model configuration."""
        return self.config.fast_model

    def set_reasoning_model(self, model_id: str, backend: str, display_name: str):
        """Set the reasoning model."""
        self.config.reasoning_model = ModelRole(
            model_id=model_id,
            backend=backend,
            display_name=display_name
        )
        self._save_config()

    def set_fast_model(self, model_id: str, backend: str, display_name: str):
        """Set the fast model."""
        self.config.fast_model = ModelRole(
            model_id=model_id,
            backend=backend,
            display_name=display_name
        )
        self._save_config()

    def get_models_dict(self) -> Dict[str, str]:
        """Get models as display_name -> model_id dict (backwards compatible)."""
        return {
            self.config.reasoning_model.display_name: self.config.reasoning_model.model_id,
            self.config.fast_model.display_name: self.config.fast_model.model_id,
        }

    def get_model_id(self, display_name: str) -> Optional[str]:
        """Get model ID from display name."""
        if display_name == self.config.reasoning_model.display_name:
            return self.config.reasoning_model.model_id
        elif display_name == self.config.fast_model.display_name:
            return self.config.fast_model.model_id
        return None

    def get_display_names(self) -> List[str]:
        """Get list of model display names."""
        return [
            self.config.reasoning_model.display_name,
            self.config.fast_model.display_name,
        ]

    def get_reasoning_display_name(self) -> str:
        """Get reasoning model display name."""
        return self.config.reasoning_model.display_name

    def get_fast_display_name(self) -> str:
        """Get fast model display name."""
        return self.config.fast_model.display_name

    def reload(self):
        """Reload configuration from disk."""
        self._load_config()


# Singleton instance
_config_manager: Optional[ModelConfigManager] = None


def get_model_config() -> ModelConfigManager:
    """Get the global model configuration manager."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ModelConfigManager()
    return _config_manager


def reload_model_config():
    """Force reload of model configuration."""
    global _config_manager
    if _config_manager is not None:
        _config_manager.reload()
    else:
        _config_manager = ModelConfigManager()
