"""
Translate FAUST compiler errors to actionable messages.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class TranslatedError:
    """A translated error with actionable fix."""
    original: str
    message: str
    cause: str
    fix: str
    example_bad: Optional[str] = None
    example_good: Optional[str] = None


class ErrorTranslator:
    """Translate FAUST compiler errors to actionable messages."""

    def __init__(self, catalog_path: Optional[Path] = None):
        if catalog_path is None:
            catalog_path = Path(__file__).parent.parent / "static" / "error_catalog.json"

        with open(catalog_path) as f:
            self.catalog = json.load(f)

        self.known_errors = self.catalog.get("errors", {})

    def translate(self, error_text: str) -> TranslatedError:
        """Translate a compiler error to an actionable message."""

        # Try to match against known patterns
        for error_id, error_info in self.known_errors.items():
            pattern = error_info.get("pattern", "")
            if not pattern:
                continue

            if re.search(pattern, error_text, re.IGNORECASE):
                return TranslatedError(
                    original=error_text,
                    message=error_info.get("message", "Unknown error"),
                    cause=error_info.get("cause", "Unknown cause"),
                    fix=error_info.get("fix", "Check the FAUST documentation"),
                    example_bad=error_info.get("example_bad"),
                    example_good=error_info.get("example_good")
                )

        # No match - return generic message with the original error
        return TranslatedError(
            original=error_text,
            message="Compilation error",
            cause=error_text,
            fix="Check the error message and FAUST documentation. Common issues: missing semicolons, wrong library prefix, signal routing mismatch."
        )

    def translate_all(self, error_text: str) -> List[TranslatedError]:
        """Translate multiple errors (one per line or separated by ERROR)."""
        errors = []

        # Split by ERROR keyword or newlines
        parts = re.split(r'(?=ERROR\s*:)', error_text)

        for part in parts:
            part = part.strip()
            if part:
                translated = self.translate(part)
                errors.append(translated)

        return errors if errors else [self.translate(error_text)]


def translate_error(error_text: str) -> TranslatedError:
    """Convenience function to translate a single error."""
    translator = ErrorTranslator()
    return translator.translate(error_text)


def translate_errors(error_text: str) -> List[TranslatedError]:
    """Convenience function to translate multiple errors."""
    translator = ErrorTranslator()
    return translator.translate_all(error_text)
