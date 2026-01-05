"""
Extract all FAUST library documentation into a single markdown file.
This file can be loaded into ChromaDB for semantic search.
"""

import re
from pathlib import Path
from typing import List, Tuple


def extract_function_docs(content: str, lib_name: str) -> List[Tuple[str, str]]:
    """Extract all function documentation blocks from a library file.

    Returns list of (function_name, full_documentation) tuples.
    """
    docs = []

    # Split by function doc headers
    # Pattern: //-----...`(prefix.)name`-----
    blocks = re.split(r'(//[-=]+`[^`]+`[-=]+)', content)

    current_header = None
    for block in blocks:
        if re.match(r'//[-=]+`[^`]+`[-=]+', block):
            current_header = block
        elif current_header:
            # Extract function name from header
            name_match = re.search(r'`\((\w+)\.\)(\w+)`', current_header)
            if not name_match:
                name_match = re.search(r'`(\w+)`', current_header)
                if name_match:
                    func_name = name_match.group(1)
                else:
                    current_header = None
                    continue
            else:
                func_name = f"{name_match.group(1)}.{name_match.group(2)}"

            # Extract documentation (comments until first non-comment code)
            doc_lines = [current_header]
            for line in block.split('\n'):
                stripped = line.strip()
                # Stop at actual code (function definition)
                if stripped and not stripped.startswith('//') and not stripped.startswith('declare'):
                    if '=' in stripped or stripped.startswith('with'):
                        break
                doc_lines.append(line)

            full_doc = '\n'.join(doc_lines).strip()
            if full_doc:
                docs.append((func_name, full_doc))

            current_header = None

    return docs


def extract_library_header(content: str) -> str:
    """Extract the library header documentation."""
    lines = []
    for line in content.split('\n')[:50]:  # First 50 lines
        if line.strip().startswith('//'):
            lines.append(line)
        elif line.strip() and not line.strip().startswith('declare'):
            break
    return '\n'.join(lines)


def generate_docs_markdown(libs_dir: Path) -> str:
    """Generate complete markdown documentation from all libraries."""

    md_lines = [
        "# FAUST Libraries Documentation",
        "",
        "Complete reference for all FAUST standard library functions.",
        "Use this for understanding function behavior, examples, and best practices.",
        "",
        "---",
        ""
    ]

    lib_files = sorted(libs_dir.glob("*.lib"))

    for lib_file in lib_files:
        lib_name = lib_file.stem

        try:
            content = lib_file.read_text(encoding='utf-8', errors='replace')

            # Extract library prefix
            prefix_match = re.search(r"official prefix is `(\w+)`", content)
            prefix = prefix_match.group(1) if prefix_match else lib_name[:2]

            # Get library header
            header = extract_library_header(content)

            # Extract all function docs
            func_docs = extract_function_docs(content, lib_name)

            if not func_docs and not header:
                continue

            # Add library section
            md_lines.append(f"# {lib_name}.lib")
            md_lines.append(f"**Prefix:** `{prefix}`")
            md_lines.append("")

            # Clean up header (remove // prefixes)
            if header:
                clean_header = '\n'.join(
                    line.lstrip('/').strip()
                    for line in header.split('\n')
                    if line.strip().startswith('//')
                )
                md_lines.append(clean_header)
                md_lines.append("")

            # Add each function
            for func_name, doc in func_docs:
                md_lines.append(f"## {func_name}")
                md_lines.append("")

                # Clean up doc (convert // comments to plain text, preserve ``` blocks)
                in_code_block = False
                for line in doc.split('\n'):
                    stripped = line.strip()

                    if '```' in stripped:
                        in_code_block = not in_code_block
                        # Extract just the ``` part
                        if in_code_block:
                            md_lines.append("```faust")
                        else:
                            md_lines.append("```")
                        continue

                    if in_code_block:
                        # Inside code block - remove comment prefixes
                        clean = re.sub(r'^[\s/]*', '', line)
                        md_lines.append(clean)
                    else:
                        # Regular text - remove // prefix
                        if stripped.startswith('//'):
                            text = stripped.lstrip('/').strip()
                            # Skip divider lines
                            if text and not re.match(r'^[-=]+$', text):
                                md_lines.append(text)

                md_lines.append("")
                md_lines.append("---")
                md_lines.append("")

            print(f"✓ {lib_file.name}: {len(func_docs)} functions")

        except Exception as e:
            print(f"✗ {lib_file.name}: {e}")

    return '\n'.join(md_lines)


def main():
    """Main entry point."""
    import sys

    libs_dir = Path("/Users/thomasmandolini/Dev/Local Coding Assistant/faustlibraries")
    output_file = Path(__file__).parent.parent / "static" / "faust_docs.md"

    if len(sys.argv) > 1:
        libs_dir = Path(sys.argv[1])

    if not libs_dir.exists():
        print(f"Error: {libs_dir} not found")
        sys.exit(1)

    print(f"Extracting FAUST documentation from: {libs_dir}")
    print("-" * 60)

    markdown = generate_docs_markdown(libs_dir)

    print("-" * 60)

    # Save
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(markdown, encoding='utf-8')

    # Stats
    line_count = len(markdown.split('\n'))
    size_kb = len(markdown.encode('utf-8')) / 1024

    print(f"Generated: {output_file}")
    print(f"Size: {size_kb:.1f} KB / {line_count} lines")


if __name__ == "__main__":
    main()
