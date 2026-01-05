"""
FAUST Validator - Validate FAUST code before compilation.

Usage:
    from faust_validator import validate, translate_error

    # Validate code before compiling
    result = validate(code)
    if not result.valid:
        print(result.format_for_llm())

    # Translate compiler error to actionable message
    translated = translate_error("ERROR : endless evaluation cycle of 4 steps")
    print(translated.fix)
"""

from .validator import (
    validate,
    translate_error,
    FAUSTValidator,
    ValidationResult,
)

from .core.syntax_checker import SyntaxChecker
from .core.error_translator import ErrorTranslator, TranslatedError

__all__ = [
    "validate",
    "translate_error",
    "FAUSTValidator",
    "ValidationResult",
    "SyntaxChecker",
    "ErrorTranslator",
    "TranslatedError",
]
