"""
Model Backend Abstraction Layer

Provides a unified interface for different LLM backends (Ollama, HuggingFace, etc.)
"""

import subprocess
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ModelInfo:
    """Information about an available model."""
    id: str
    name: str
    size: str
    backend: str
    modified: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


class ModelBackend(ABC):
    """Abstract base class for model backends."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Backend identifier name."""
        pass

    @abstractmethod
    def list_models(self) -> List[ModelInfo]:
        """List all available models for this backend."""
        pass

    @abstractmethod
    def check_availability(self, model_id: str) -> bool:
        """Check if a specific model is available."""
        pass

    @abstractmethod
    def generate(self, prompt: str, model_id: str, **kwargs) -> str:
        """Generate a response from the model."""
        pass

    @abstractmethod
    def get_llm_instance(self, model_id: str, **kwargs) -> Any:
        """Get a langchain-compatible LLM instance."""
        pass


class OllamaBackend(ModelBackend):
    """Ollama backend implementation."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self._model_cache: Dict[str, Any] = {}

    @property
    def name(self) -> str:
        return "ollama"

    def list_models(self) -> List[ModelInfo]:
        """List all models available in Ollama."""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                print(f"Ollama list error: {result.stderr}")
                return []

            models = []
            lines = result.stdout.strip().split('\n')

            # Skip header line
            for line in lines[1:]:
                if not line.strip():
                    continue

                parts = line.split()
                if len(parts) >= 2:
                    model_id = parts[0]
                    # Parse size (e.g., "19 GB" or "19GB")
                    size_parts = []
                    modified = ""

                    # Find size and modified info
                    for i, part in enumerate(parts[1:], 1):
                        if part.endswith('GB') or part.endswith('MB') or part == 'GB' or part == 'MB':
                            if parts[i-1].replace('.', '').isdigit():
                                size_parts = [parts[i-1], part] if part in ['GB', 'MB'] else [part]
                            else:
                                size_parts = [part]

                    size = ' '.join(size_parts) if size_parts else "Unknown"

                    # Create display name from model ID
                    display_name = self._format_model_name(model_id)

                    models.append(ModelInfo(
                        id=model_id,
                        name=display_name,
                        size=size,
                        backend="ollama",
                        modified=modified
                    ))

            return models

        except subprocess.TimeoutExpired:
            print("Ollama list timed out")
            return []
        except FileNotFoundError:
            print("Ollama not found. Is it installed?")
            return []
        except Exception as e:
            print(f"Error listing Ollama models: {e}")
            return []

    def _format_model_name(self, model_id: str) -> str:
        """Format model ID into a display name."""
        # Remove :latest suffix
        name = model_id.replace(':latest', '')

        # Common formatting
        name = name.replace('-', ' ').replace('_', ' ')

        # Capitalize appropriately
        words = name.split()
        formatted = []
        for word in words:
            # Keep version numbers lowercase
            if word.replace('.', '').replace('b', '').replace('q', '').isdigit():
                formatted.append(word.upper() if 'b' in word.lower() else word)
            else:
                formatted.append(word.capitalize())

        return ' '.join(formatted)

    def check_availability(self, model_id: str) -> bool:
        """Check if a model is available in Ollama."""
        try:
            from langchain_community.llms import Ollama
            llm = Ollama(model=model_id)
            llm.invoke("test")
            return True
        except Exception:
            return False

    def generate(self, prompt: str, model_id: str, **kwargs) -> str:
        """Generate response using Ollama."""
        llm = self.get_llm_instance(model_id, **kwargs)
        if llm:
            return llm.invoke(prompt)
        return "Error: Could not get model instance"

    def get_llm_instance(self, model_id: str, temperature: float = 0.7, system: str = "", **kwargs) -> Any:
        """Get a cached Ollama LLM instance."""
        cache_key = f"{model_id}_{temperature}_{hash(system)}"

        if cache_key not in self._model_cache:
            try:
                from langchain_community.llms import Ollama
                self._model_cache[cache_key] = Ollama(
                    model=model_id,
                    temperature=temperature,
                    system=system,
                )
            except Exception as e:
                print(f"Error creating Ollama instance for {model_id}: {e}")
                return None

        return self._model_cache.get(cache_key)

    def clear_cache(self):
        """Clear the model instance cache."""
        self._model_cache.clear()


class HuggingFaceBackend(ModelBackend):
    """HuggingFace Transformers backend (Phase 2 - stub)."""

    def __init__(self, device: str = "mps"):
        self.device = device
        self._model_cache: Dict[str, Any] = {}

    @property
    def name(self) -> str:
        return "huggingface"

    def list_models(self) -> List[ModelInfo]:
        """List available HuggingFace models (manual configuration)."""
        # Phase 2: Would return manually configured models
        # For now, return a placeholder list
        return [
            ModelInfo(
                id="THUDM/glm-4.6v-flash",
                name="GLM-4.6V Flash (Vision)",
                size="~18GB",
                backend="huggingface",
                details={"vision": True, "requires_gpu": True}
            )
        ]

    def check_availability(self, model_id: str) -> bool:
        """Check if HuggingFace model can be loaded."""
        # Phase 2 implementation
        return False

    def generate(self, prompt: str, model_id: str, **kwargs) -> str:
        """Generate using HuggingFace Transformers."""
        # Phase 2 implementation
        return "HuggingFace backend not yet implemented"

    def get_llm_instance(self, model_id: str, **kwargs) -> Any:
        """Get HuggingFace model instance."""
        # Phase 2 implementation
        return None


class BackendManager:
    """Manages multiple model backends."""

    def __init__(self):
        self.backends: Dict[str, ModelBackend] = {}
        self._register_default_backends()

    def _register_default_backends(self):
        """Register default backends."""
        self.register_backend(OllamaBackend())
        # Phase 2: self.register_backend(HuggingFaceBackend())

    def register_backend(self, backend: ModelBackend):
        """Register a new backend."""
        self.backends[backend.name] = backend

    def get_backend(self, name: str) -> Optional[ModelBackend]:
        """Get a backend by name."""
        return self.backends.get(name)

    def list_all_models(self) -> Dict[str, List[ModelInfo]]:
        """List models from all backends."""
        all_models = {}
        for name, backend in self.backends.items():
            all_models[name] = backend.list_models()
        return all_models

    def get_available_backends(self) -> List[str]:
        """Get list of available backend names."""
        return list(self.backends.keys())


# Singleton instance
_backend_manager: Optional[BackendManager] = None


def get_backend_manager() -> BackendManager:
    """Get the global backend manager instance."""
    global _backend_manager
    if _backend_manager is None:
        _backend_manager = BackendManager()
    return _backend_manager
