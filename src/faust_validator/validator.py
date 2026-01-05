"""
FAUST Validator - Main interface.
Validates FAUST code before compilation.
"""

import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

from .core.syntax_checker import SyntaxChecker, SyntaxError as SyntaxIssue
from .core.error_translator import ErrorTranslator, TranslatedError


@dataclass
class ValidationResult:
    """Result of validating FAUST code."""
    valid: bool
    errors: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[Dict[str, Any]] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "suggestions": self.suggestions
        }

    def format_for_llm(self) -> str:
        """Format validation result for feeding back to an LLM."""
        lines = []

        if self.valid:
            lines.append("✓ Code passed validation")
        else:
            lines.append("✗ Validation failed:")

        for err in self.errors:
            lines.append(f"\nERROR (line {err.get('line', '?')}): {err.get('message', 'Unknown')}")
            if err.get('suggestion'):
                lines.append(f"  FIX: {err['suggestion']}")
            if err.get('example_good'):
                lines.append(f"  CORRECT: {err['example_good']}")

        for warn in self.warnings:
            lines.append(f"\nWARNING (line {warn.get('line', '?')}): {warn.get('message', 'Unknown')}")
            if warn.get('suggestion'):
                lines.append(f"  SUGGESTION: {warn['suggestion']}")

        return '\n'.join(lines)


class FAUSTValidator:
    """Main FAUST validator combining all checks."""

    def __init__(self):
        self.syntax_checker = SyntaxChecker()
        self.error_translator = ErrorTranslator()

    def validate(self, code: str) -> ValidationResult:
        """Validate FAUST code before compilation.

        Args:
            code: FAUST source code

        Returns:
            ValidationResult with errors, warnings, and suggestions
        """
        errors = []
        warnings = []
        suggestions = []

        # 1. Basic syntax checks
        try:
            syntax_issues = self.syntax_checker.check(code)

            for issue in syntax_issues:
                item = {
                    "line": issue.line,
                    "column": issue.column,
                    "message": issue.message,
                    "suggestion": issue.suggestion
                }
                if issue.severity == "error":
                    errors.append(item)
                else:
                    warnings.append(item)

        except Exception as e:
            warnings.append({
                "line": 0,
                "message": f"Syntax check failed: {e}",
                "suggestion": "Code may still compile"
            })

        # 2. Check for common patterns that cause issues
        patterns_check = self._check_common_patterns(code)
        warnings.extend(patterns_check.get("warnings", []))
        suggestions.extend(patterns_check.get("suggestions", []))

        # 3. Check for missing import
        if "import(" not in code and "library(" not in code:
            if any(prefix + "." in code for prefix in ["os", "fi", "de", "en", "an", "ma", "ba", "no", "re", "ef"]):
                warnings.append({
                    "line": 1,
                    "message": "Using library functions but no import statement",
                    "suggestion": "Add: import(\"stdfaust.lib\");"
                })

        # 4. Check for process definition
        if "process" not in code:
            errors.append({
                "line": 0,
                "message": "No 'process' definition found",
                "suggestion": "FAUST requires: process = <your_signal_chain>;"
            })

        is_valid = len(errors) == 0

        return ValidationResult(
            valid=is_valid,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions
        )

    def translate_compiler_error(self, error_text: str) -> TranslatedError:
        """Translate a FAUST compiler error to actionable message."""
        return self.error_translator.translate(error_text)

    def _check_common_patterns(self, code: str) -> Dict[str, List[Dict]]:
        """Check for common problematic patterns."""
        warnings = []
        suggestions = []
        lines = code.split('\n')

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()

            # Check for division without protection
            if re.search(r'/\s*\w+\s*[;,)]', line) and "max(" not in line:
                # Looks like division by a variable without max protection
                if "/0" not in line and "/ 0" not in line:  # Not literal zero
                    suggestions.append(f"Line {line_num}: Consider protecting division with max(0.0001, divisor)")

            # Check for very large delay constants
            delay_match = re.search(r'@\s*\(\s*(\d+)\s*\)', line)
            if delay_match:
                delay_val = int(delay_match.group(1))
                if delay_val > 1000000:
                    warnings.append({
                        "line": line_num,
                        "message": f"Large delay value: {delay_val} samples",
                        "suggestion": "Consider using de.delay() with explicit max size"
                    })

        return {"warnings": warnings, "suggestions": suggestions}


# Convenience functions
def validate(code: str) -> ValidationResult:
    """Validate FAUST code."""
    validator = FAUSTValidator()
    return validator.validate(code)


def translate_error(error_text: str) -> TranslatedError:
    """Translate a compiler error to actionable message."""
    validator = FAUSTValidator()
    return validator.translate_compiler_error(error_text)
