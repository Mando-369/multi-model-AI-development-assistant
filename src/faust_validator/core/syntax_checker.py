"""
Check FAUST code syntax against the bible.
Catches unknown functions, wrong arg counts, etc.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class SyntaxError:
    """A syntax error found in FAUST code."""
    line: int
    column: int
    message: str
    suggestion: str
    severity: str = "error"  # error, warning


class SyntaxChecker:
    """Check FAUST code against the function bible."""

    def __init__(self, bible_path: Optional[Path] = None):
        if bible_path is None:
            bible_path = Path(__file__).parent.parent / "static" / "faust_bible.json"

        with open(bible_path) as f:
            self.bible = json.load(f)

        self.functions = self.bible.get("functions", {})

        # Build prefix -> functions map
        self.by_prefix: Dict[str, List[str]] = {}
        for full_name, info in self.functions.items():
            prefix = info.get("prefix", "")
            if prefix not in self.by_prefix:
                self.by_prefix[prefix] = []
            self.by_prefix[prefix].append(info.get("name", ""))

        # Known library prefixes
        self.known_prefixes = set(self.by_prefix.keys())

    def check(self, code: str) -> List[SyntaxError]:
        """Check FAUST code for syntax issues."""
        errors = []
        lines = code.split('\n')

        for line_num, line in enumerate(lines, 1):
            # Skip comments
            stripped = line.strip()
            if stripped.startswith('//') or stripped.startswith('/*'):
                continue

            # Check for function calls with prefix: prefix.func(args)
            # Pattern: word.word(
            func_calls = re.finditer(r'\b(\w+)\.(\w+)\s*\(', line)
            for match in func_calls:
                prefix = match.group(1)
                func_name = match.group(2)
                full_name = f"{prefix}.{func_name}"
                col = match.start() + 1

                # Check if prefix is known
                if prefix not in self.known_prefixes:
                    # Might be a variable access, not a library call
                    # Only warn if it looks like a library prefix (2-3 chars)
                    if len(prefix) <= 3:
                        errors.append(SyntaxError(
                            line=line_num,
                            column=col,
                            message=f"Unknown library prefix '{prefix}'",
                            suggestion=f"Known prefixes: {', '.join(sorted(self.known_prefixes)[:10])}...",
                            severity="warning"
                        ))
                    continue

                # Check if function exists
                if full_name not in self.functions:
                    # Find similar functions
                    similar = self._find_similar(prefix, func_name)
                    suggestion = f"Did you mean: {', '.join(similar)}" if similar else "Check faustlibraries documentation"
                    errors.append(SyntaxError(
                        line=line_num,
                        column=col,
                        message=f"Unknown function '{full_name}'",
                        suggestion=suggestion,
                        severity="error"
                    ))
                    continue

                # Check arg count (if we can parse it)
                func_info = self.functions[full_name]
                expected_args = func_info.get("arg_count", 0)
                if expected_args > 0:
                    # Try to count args in the call
                    actual_args = self._count_args(line, match.end())
                    if actual_args is not None and actual_args != expected_args:
                        errors.append(SyntaxError(
                            line=line_num,
                            column=col,
                            message=f"'{full_name}' expects {expected_args} args, got {actual_args}",
                            suggestion=f"Args: {', '.join(func_info.get('args', []))}",
                            severity="error"
                        ))

            # Check for recursive definition trap
            # Pattern: name = name.something
            assign_match = re.match(r'(\w+)\s*=\s*(\w+)\.', stripped)
            if assign_match:
                var_name = assign_match.group(1)
                ref_name = assign_match.group(2)
                if var_name == ref_name:
                    errors.append(SyntaxError(
                        line=line_num,
                        column=1,
                        message=f"Recursive definition: '{var_name}' references itself",
                        suggestion=f"Rename variable to avoid conflict. Use '{var_name[:3]}' or similar.",
                        severity="error"
                    ))

            # Check for string assignment (not in declare)
            if '=' in line and '"' in line and not stripped.startswith('declare'):
                # Check if string is being assigned to a variable
                string_assign = re.search(r'(\w+)\s*=\s*"[^"]*"', stripped)
                if string_assign:
                    errors.append(SyntaxError(
                        line=line_num,
                        column=string_assign.start() + 1,
                        message="String assigned to variable (invalid in FAUST)",
                        suggestion="Use 'declare name \"value\";' for metadata strings",
                        severity="error"
                    ))

        return errors

    def _find_similar(self, prefix: str, func_name: str) -> List[str]:
        """Find similar function names in the same library."""
        if prefix not in self.by_prefix:
            return []

        funcs = self.by_prefix[prefix]
        # Simple similarity: starts with same letters
        similar = [f"{prefix}.{f}" for f in funcs if f.startswith(func_name[:3])]
        return similar[:5]

    def _count_args(self, line: str, start_pos: int) -> Optional[int]:
        """Count arguments in a function call starting at start_pos."""
        # Find matching parenthesis and count commas
        depth = 1
        pos = start_pos
        commas = 0

        while pos < len(line) and depth > 0:
            char = line[pos]
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            elif char == ',' and depth == 1:
                commas += 1
            pos += 1

        if depth == 0:
            # Check if empty args
            content = line[start_pos:pos-1].strip()
            if not content:
                return 0
            return commas + 1

        return None  # Couldn't parse


def check_syntax(code: str) -> List[SyntaxError]:
    """Convenience function to check FAUST syntax."""
    checker = SyntaxChecker()
    return checker.check(code)
