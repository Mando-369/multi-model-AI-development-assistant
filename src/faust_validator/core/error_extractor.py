"""
Extract error patterns from FAUST compiler source code.
Outputs error_catalog.json with patterns and actionable fixes.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any


# Manual catalog of known errors with actionable fixes
# These are the most common errors users encounter
KNOWN_ERRORS = {
    "endless_evaluation_cycle": {
        "pattern": r"endless evaluation cycle of (\d+) steps",
        "message": "Endless evaluation cycle detected",
        "cause": "A variable references itself, creating infinite recursion. Usually happens when a variable name matches a library prefix (e.g., 'envelope = envelope.adsr(...)' tries to access 'envelope' before it's defined).",
        "fix": "Rename the variable to avoid conflict with library names. Use short names like 'env' instead of 'envelope', 'lpf' instead of 'filter', 'dly' instead of 'delay'.",
        "example_bad": "envelope = envelope.adsr(0.1, 0.1, 0.8, 0.2, gate);",
        "example_good": "env = en.adsr(0.1, 0.1, 0.8, 0.2, gate);"
    },
    "stack_overflow": {
        "pattern": r"stack overflow in eval",
        "message": "Stack overflow during evaluation",
        "cause": "Deep recursion or infinite loop in signal definition.",
        "fix": "Check for circular references in your signal definitions. Ensure feedback loops use the ~ operator correctly.",
        "example_bad": "x = x + 1;",
        "example_good": "x = _ ~ +(1);  // proper feedback"
    },
    "sequential_composition_mismatch": {
        "pattern": r"sequential composition.*outputs.*inputs",
        "message": "Sequential composition (:) input/output mismatch",
        "cause": "The output count of the left expression doesn't match the input count of the right expression.",
        "fix": "Check signal counts. Use <: to split signals or :> to merge them. Example: stereo signal into mono filter needs :> first.",
        "example_bad": "stereo_osc : mono_filter  // 2 outputs -> 1 input",
        "example_good": "stereo_osc :> mono_filter  // merge to mono first"
    },
    "split_composition_mismatch": {
        "pattern": r"split composition.*outputs.*inputs",
        "message": "Split composition (<:) error",
        "cause": "Output count must be a multiple of input count in split composition.",
        "fix": "Ensure the right side has N copies of the destination, where N = outputs/inputs.",
        "example_bad": "mono <: stereo_effect  // 1 -> 2 inputs doesn't work",
        "example_good": "mono <: (_, _) : stereo_effect  // duplicate first"
    },
    "merge_composition_mismatch": {
        "pattern": r"merge composition.*outputs.*inputs",
        "message": "Merge composition (:>) error",
        "cause": "Input count must be a multiple of output count in merge composition.",
        "fix": "The left side signals are summed in groups to produce fewer outputs.",
        "example_bad": "stereo :> (_, _, _)  // 2 -> 3 doesn't work",
        "example_good": "stereo :> _  // 2 -> 1 (summed to mono)"
    },
    "recursive_composition_mismatch": {
        "pattern": r"recursive composition.*outputs.*inputs",
        "message": "Recursive composition (~) error",
        "cause": "In A~B, outputs of A must be >= inputs of B, and inputs of A must be >= outputs of B.",
        "fix": "Check that the feedback path has compatible signal counts.",
        "example_bad": "_ ~ (_, _)  // 1 output can't feed 2 inputs",
        "example_good": "_ ~ _  // 1 output feeds 1 input"
    },
    "undefined_symbol": {
        "pattern": r"undefined symbol\s*['\"]?(\w+)['\"]?",
        "message": "Undefined symbol",
        "cause": "Reference to a variable or function that doesn't exist.",
        "fix": "Check spelling. Ensure library is imported. Use correct prefix (e.g., 'fi.lowpass' not 'filter.lowpass').",
        "example_bad": "process = lowpass(2, 1000);",
        "example_good": "process = fi.lowpass(2, 1000);"
    },
    "incompatible_types": {
        "pattern": r"incompatible types.*and",
        "message": "Incompatible signal types",
        "cause": "Trying to combine signals of different types (e.g., int and float).",
        "fix": "Ensure consistent types. Use float() or int() to convert.",
        "example_bad": "process = 1 + 0.5;  // int + float",
        "example_good": "process = 1.0 + 0.5;  // float + float"
    },
    "division_by_zero": {
        "pattern": r"division by (0|zero)",
        "message": "Division by zero",
        "cause": "Dividing by a value that can be zero at runtime.",
        "fix": "Use ba.if or max() to prevent division by zero. Note: ba.if evaluates both branches!",
        "example_bad": "process = x / y;",
        "example_good": "process = x / max(0.0001, y);"
    },
    "string_assignment": {
        "pattern": r"unexpected STRING",
        "message": "Unexpected string literal",
        "cause": "Strings can only be used in declare statements and UI labels, not as variable values.",
        "fix": "Use 'declare' for metadata strings. Variables must hold signal expressions.",
        "example_bad": "title = \"My Synth\";",
        "example_good": "declare name \"My Synth\";"
    },
    "file_not_found": {
        "pattern": r"can't open.*file",
        "message": "File not found",
        "cause": "The compiler can't find the referenced file (library or include).",
        "fix": "Check the file path. Ensure faustlibraries is installed. Use import(\"stdfaust.lib\") for standard libs.",
        "example_bad": "import(\"mylib.lib\");  // file doesn't exist",
        "example_good": "import(\"stdfaust.lib\");  // standard library"
    },
    "invalid_delay": {
        "pattern": r"invalid delay parameter",
        "message": "Invalid delay parameter",
        "cause": "Delay value is negative or exceeds maximum.",
        "fix": "Ensure delay is positive and within max bounds. Use max(0, d) to clamp.",
        "example_bad": "process = _ : @(-100);",
        "example_good": "process = _ : @(max(0, d));"
    },
    "too_big_delay": {
        "pattern": r"too big delay value",
        "message": "Delay value too large",
        "cause": "Delay exceeds the maximum allowed (usually 2^24 samples).",
        "fix": "Reduce delay or use de.delay() with explicit max size.",
        "example_bad": "process = _ : @(100000000);",
        "example_good": "process = _ : de.delay(48000, d);  // explicit max"
    },
    "unknown_function": {
        "pattern": r"unknown function.*['\"](\w+)['\"]",
        "message": "Unknown function",
        "cause": "Calling a function that doesn't exist in the imported libraries.",
        "fix": "Check function name and library prefix. See faustlibraries documentation.",
        "example_bad": "process = filters.lowpass(2, 1000);",
        "example_good": "process = fi.lowpass(2, 1000);"
    },
    "wrong_number_of_arguments": {
        "pattern": r"wrong number of (arguments|parameters)",
        "message": "Wrong number of arguments",
        "cause": "Function called with incorrect number of parameters.",
        "fix": "Check the function signature in documentation.",
        "example_bad": "process = fi.lowpass(1000);  // missing order",
        "example_good": "process = fi.lowpass(2, 1000);  // order, freq"
    },
    "ba_if_strict_evaluation": {
        "pattern": r"",  # No specific error - runtime issue
        "message": "ba.if strict evaluation trap",
        "cause": "ba.if evaluates BOTH branches, so division by zero in either branch will fail even if not selected.",
        "fix": "Use select2() for conditional selection, or ensure both branches are safe.",
        "example_bad": "ba.if(x > 0, 1/x, 0)  // 1/x evaluated even when x=0",
        "example_good": "select2(x > 0, 0, 1/max(0.0001, x))"
    }
}


def extract_errors_from_compiler(compiler_dir: Path) -> List[Dict[str, Any]]:
    """Scan compiler source for additional error patterns."""
    extracted = []

    cpp_files = list(compiler_dir.rglob("*.cpp"))

    for cpp_file in cpp_files:
        try:
            content = cpp_file.read_text(encoding='utf-8', errors='replace')

            # Find error strings
            # Pattern: "ERROR : <message>"
            errors = re.findall(r'"(ERROR\s*:?\s*[^"]{10,100})"', content)

            for error_msg in errors:
                # Clean up and deduplicate
                clean_msg = error_msg.strip()
                if clean_msg and clean_msg not in [e.get("raw") for e in extracted]:
                    extracted.append({
                        "raw": clean_msg,
                        "source": str(cpp_file.relative_to(compiler_dir))
                    })

        except Exception as e:
            print(f"Error reading {cpp_file}: {e}")

    return extracted


def build_catalog(compiler_dir: Path) -> Dict[str, Any]:
    """Build the complete error catalog."""
    catalog = {
        "version": "1.0",
        "source": str(compiler_dir),
        "errors": KNOWN_ERRORS,
        "raw_errors": []
    }

    # Extract additional errors from source
    raw_errors = extract_errors_from_compiler(compiler_dir)
    catalog["raw_errors"] = raw_errors

    print(f"Known errors with fixes: {len(KNOWN_ERRORS)}")
    print(f"Raw errors extracted: {len(raw_errors)}")

    return catalog


def main():
    """Main entry point."""
    import sys

    compiler_dir = Path("/Users/thomasmandolini/Dev/Local Coding Assistant/faust/compiler")
    output_file = Path(__file__).parent.parent / "static" / "error_catalog.json"

    if len(sys.argv) > 1:
        compiler_dir = Path(sys.argv[1])

    if not compiler_dir.exists():
        print(f"Error: {compiler_dir} not found")
        sys.exit(1)

    print(f"Extracting errors from: {compiler_dir}")
    print("-" * 60)

    catalog = build_catalog(compiler_dir)

    # Save
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(catalog, f, indent=2)

    print("-" * 60)
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()
