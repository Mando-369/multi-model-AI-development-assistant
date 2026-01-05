"""
Parse FAUST library files and extract function definitions.
Outputs faust_bible.json with all valid functions, args, and I/O counts.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any


def extract_prefix(content: str) -> Optional[str]:
    """Extract library prefix from header comment."""
    # Pattern: "Its official prefix is `xx`"
    match = re.search(r"official prefix is `(\w+)`", content)
    if match:
        return match.group(1)
    return None


def parse_usage_signature(usage_block: str) -> Dict[str, Any]:
    """Parse the Usage code block to extract args and I/O."""
    result = {"args": [], "inputs": 0, "outputs": 1}

    # Find the signature line in the code block
    # Patterns like: _ : func(a,b) : _
    #                func(a,b,c) : _
    #                _ : func : _
    #                _, _ : func : _, _

    lines = usage_block.strip().split('\n')
    for line in lines:
        # Strip comment prefixes: //, *, etc
        line = re.sub(r'^[\s/*]+', '', line).strip()
        if not line:
            continue

        # Skip lines that are clearly not signatures
        if line.startswith('#') or line.startswith('Where') or '=' in line:
            continue

        # Pattern: [inputs :] funcname(args) [: outputs]
        # Examples: ar(at,rt,t) : _           → 0 in, 1 out
        #           _ : zero(z) : _           → 1 in, 1 out
        #           _, _ : cross : _, _       → 2 in, 2 out

        # Find function call pattern (name with 2+ letters, optional args)
        func_match = re.search(r'\b([a-zA-Z][a-zA-Z0-9_]+)\s*(\([^)]*\))?', line)
        if not func_match:
            continue

        func_name = func_match.group(1)
        func_pos = func_match.start()

        # Split by function position
        before = line[:func_pos]
        after = line[func_match.end():]

        # Count underscores (each _ is a signal)
        result["inputs"] = before.count('_')
        out_count = after.count('_')
        result["outputs"] = out_count if out_count > 0 else 1

        # Extract args
        if func_match.group(2):
            args_str = func_match.group(2).strip('()')
            if args_str.strip():
                result["args"] = [a.strip() for a in args_str.split(',')]

        break

    return result


def parse_where_block(block: str) -> Dict[str, str]:
    """Extract parameter descriptions from Where: block."""
    param_docs = {}

    # Find Where: section
    where_match = re.search(r'Where:\s*\n(.*?)(?=\n\s*\n|#### |//[-]+)', block, re.DOTALL)
    if not where_match:
        return param_docs

    where_text = where_match.group(1)

    # Parse each parameter line: * `param`: description
    for line in where_text.split('\n'):
        line = line.strip().lstrip('/*').strip()
        param_match = re.match(r'\*?\s*`(\w+)`\s*:\s*(.+)', line)
        if param_match:
            param_name = param_match.group(1)
            param_desc = param_match.group(2).strip()
            param_docs[param_name] = param_desc

    return param_docs


def parse_test_block(block: str) -> str:
    """Extract example code from #### Test block."""
    # Find Test section with code block
    test_match = re.search(r'#### Test.*?```\s*\n(.*?)```', block, re.DOTALL)
    if test_match:
        example = test_match.group(1).strip()
        # Clean up comment prefixes
        lines = []
        for line in example.split('\n'):
            # Remove leading // but preserve content
            clean = re.sub(r'^[\s/]*', '', line)
            if clean:
                lines.append(clean)
        return '\n'.join(lines)
    return ""


def parse_function_block(block: str, default_prefix: str) -> Optional[Dict[str, Any]]:
    """Parse a single function documentation block."""

    # Extract function name from header
    # Pattern: //-----------------------`(prefix.)funcname`--------------------------
    header_match = re.search(r"`\((\w+)\.\)(\w+)`", block)
    if not header_match:
        # Try without prefix: `funcname`
        header_match = re.search(r"`(\w+)`", block)
        if header_match:
            prefix = default_prefix
            name = header_match.group(1)
        else:
            return None
    else:
        prefix = header_match.group(1)
        name = header_match.group(2)

    # Extract description (first paragraph after header)
    lines = block.split('\n')
    description_lines = []
    in_description = False
    for line in lines:
        line = line.strip()
        if line.startswith('//') and not line.startswith('//--') and not line.startswith('//=='):
            text = line.lstrip('/').strip()
            if text and not text.startswith('#'):
                if '#### Usage' in line:
                    break
                description_lines.append(text)
                in_description = True
            elif in_description and not text:
                break

    description = ' '.join(description_lines[:3])  # First 3 lines max

    # Extract Usage block
    usage_match = re.search(r'#### Usage.*?```\s*\n(.*?)```', block, re.DOTALL)
    signature_info = {"args": [], "inputs": 0, "outputs": 1}
    if usage_match:
        signature_info = parse_usage_signature(usage_match.group(1))

    # If no args from usage, try to get from function definition
    if not signature_info["args"]:
        # Pattern: funcname(arg1, arg2) = or funcname(arg1, arg2) :
        def_match = re.search(rf'{name}\s*\(([^)]*)\)\s*[=:]', block)
        if def_match:
            args_str = def_match.group(1)
            if args_str.strip():
                signature_info["args"] = [a.strip() for a in args_str.split(',')]

    # Extract parameter documentation from Where: block
    param_docs = parse_where_block(block)

    # Extract example from #### Test block
    example = parse_test_block(block)

    return {
        "prefix": prefix,
        "name": name,
        "full_name": f"{prefix}.{name}",
        "args": signature_info["args"],
        "arg_count": len(signature_info["args"]),
        "inputs": signature_info["inputs"],
        "outputs": signature_info["outputs"],
        "description": description[:200] if description else "",
        "param_docs": param_docs,
        "example": example[:500] if example else ""  # Limit example size
    }


def parse_lib_file(filepath: Path) -> Dict[str, Dict[str, Any]]:
    """Parse a single .lib file and extract all functions."""
    content = filepath.read_text(encoding='utf-8', errors='replace')

    # Get default prefix for this library
    default_prefix = extract_prefix(content) or filepath.stem[:2]

    functions = {}

    # Split by function doc blocks
    # Pattern: //-----...`(prefix.)name`-----
    blocks = re.split(r'(//[-]+`.*?`[-]+)', content)

    current_header = None
    for i, block in enumerate(blocks):
        if re.match(r'//[-]+`.*?`[-]+', block):
            current_header = block
        elif current_header:
            full_block = current_header + block
            func_info = parse_function_block(full_block, default_prefix)
            if func_info:
                functions[func_info["full_name"]] = func_info
            current_header = None

    return functions


def build_bible(libs_dir: Path) -> Dict[str, Any]:
    """Parse all .lib files and build the complete bible."""
    bible = {
        "version": "1.0",
        "source": str(libs_dir),
        "libraries": {},
        "functions": {}
    }

    lib_files = sorted(libs_dir.glob("*.lib"))

    for lib_file in lib_files:
        lib_name = lib_file.stem
        prefix = None

        # Parse the file
        try:
            content = lib_file.read_text(encoding='utf-8', errors='replace')
            prefix = extract_prefix(content)
            functions = parse_lib_file(lib_file)

            # Add to bible
            bible["libraries"][lib_name] = {
                "file": lib_file.name,
                "prefix": prefix,
                "function_count": len(functions)
            }

            bible["functions"].update(functions)

            print(f"✓ {lib_file.name}: {len(functions)} functions (prefix: {prefix})")

        except Exception as e:
            print(f"✗ {lib_file.name}: Error - {e}")

    return bible


def main():
    """Main entry point."""
    import sys

    # Default paths
    libs_dir = Path("/Users/thomasmandolini/Dev/Local Coding Assistant/faustlibraries")
    output_file = Path(__file__).parent.parent / "static" / "faust_bible.json"

    if len(sys.argv) > 1:
        libs_dir = Path(sys.argv[1])

    if not libs_dir.exists():
        print(f"Error: {libs_dir} not found")
        sys.exit(1)

    print(f"Parsing FAUST libraries from: {libs_dir}")
    print("-" * 60)

    bible = build_bible(libs_dir)

    print("-" * 60)
    print(f"Total libraries: {len(bible['libraries'])}")
    print(f"Total functions: {len(bible['functions'])}")

    # Save
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(bible, f, indent=2)

    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()
