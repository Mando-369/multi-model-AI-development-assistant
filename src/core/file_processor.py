import pytesseract
from PIL import Image
from pathlib import Path
from datetime import datetime
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


class FileProcessor:
    def __init__(self, vectorstore, text_splitter):
        self.vectorstore = vectorstore
        self.text_splitter = text_splitter
        self.supported_extensions = [
            ".pdf",
            ".txt",
            ".md",
            ".py",
            ".cpp",
            ".h",
            ".c",
            ".dsp",
            ".lib",
            ".hpp",
            ".cc",
            ".jpg",
            ".jpeg",
            ".png",
            ".bmp",
            ".tiff",
        ]

    def process_file(self, file_path):
        """Process files with enhanced metadata including folder structure"""
        file_path = Path(file_path)
        file_ext = file_path.suffix.lower()

        try:
            # Determine file category from folder structure
            relative_path = (
                file_path.relative_to(Path("./uploads"))
                if str(file_path).startswith("./uploads")
                else file_path
            )

            folder_category = (
                str(relative_path.parent)
                if str(relative_path.parent) != "."
                else "root"
            )

            if file_ext == ".pdf":
                loader = PyPDFLoader(str(file_path))
                documents = loader.load()
            elif file_ext in [
                ".txt",
                ".md",
                ".py",
                ".cpp",
                ".h",
                ".c",
                ".dsp",
                ".lib",
                ".hpp",
                ".cc",
            ]:
                loader = TextLoader(str(file_path))
                documents = loader.load()
            elif file_ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
                image = Image.open(file_path)
                ocr_text = pytesseract.image_to_string(image)
                documents = [
                    Document(
                        page_content=ocr_text,
                        metadata={
                            "source": str(file_path),
                            "type": "image_ocr",
                            "category": folder_category,
                            "file_name": file_path.name,
                        },
                    )
                ]
            else:
                return f"Unsupported file type: {file_ext}"

            # Add enhanced metadata to all documents
            for doc in documents:
                if hasattr(doc, "metadata"):
                    doc.metadata.update(
                        {
                            "category": folder_category,
                            "file_name": file_path.name,
                            "file_type": file_ext,
                            "processed_date": datetime.now().isoformat(),
                        }
                    )

            # Process and store
            splits = self.text_splitter.split_documents(documents)
            self.vectorstore.add_documents(splits)
            return f"Processed {len(splits)} chunks from {folder_category}/{file_path.name}"

        except Exception as e:
            return f"Error processing {file_path}: {e}"

    def scan_uploads_recursive(self):
        """Scan uploads folder and all subfolders recursively"""
        uploads_dir = Path("./uploads")
        if not uploads_dir.exists():
            return "❌ No uploads folder found"

        processed_files = []

        # Walk through all directories and subdirectories
        for file_path in uploads_dir.rglob("*"):
            if (
                file_path.is_file()
                and file_path.suffix.lower() in self.supported_extensions
            ):
                try:
                    relative_path = file_path.relative_to(uploads_dir)
                    result = self.process_file(str(file_path))
                    processed_files.append(
                        {
                            "file": str(relative_path),
                            "result": result,
                            "category": (
                                str(relative_path.parent)
                                if str(relative_path.parent) != "."
                                else "root"
                            ),
                        }
                    )
                except Exception as e:
                    # Handle case where relative_path might not be set
                    try:
                        relative_path = file_path.relative_to(uploads_dir)
                        file_str = str(relative_path)
                    except:
                        file_str = str(file_path.name)

                    processed_files.append(
                        {
                            "file": file_str,
                            "result": f"Error: {e}",
                            "category": "error",
                        }
                    )

        # Organize results by category
        categories = {}
        for item in processed_files:
            category = item["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(item)

        # Format response
        summary = f"📁 Processed {len(processed_files)} files from subfolders:\n\n"
        for category, files in categories.items():
            summary += f"📂 **{category}/**: {len(files)} files\n"
            for file_info in files[:3]:  # Show first 3 files per category
                summary += f" ✅ {file_info['file']}\n"
            if len(files) > 3:
                summary += f" ... and {len(files) - 3} more files\n"
            summary += "\n"

        return summary

    def load_faust_libraries(self):
        """Load FAUST .lib files directly from faustlibraries submodule.

        This provides deep semantic search for all FAUST functions,
        examples, and library documentation from the source files.
        """
        import re

        # Path to faustlibraries submodule
        libs_dir = Path(__file__).parent.parent.parent / "faust_documentation" / "faustlibraries"

        if not libs_dir.exists():
            return "❌ faustlibraries not found. Run: git submodule update --init"

        # Library prefix mapping
        LIB_PREFIXES = {
            "aanl.lib": "aa",
            "analyzers.lib": "an",
            "basics.lib": "ba",
            "compressors.lib": "co",
            "delays.lib": "de",
            "demos.lib": "dm",
            "dx7.lib": "dx",
            "envelopes.lib": "en",
            "fds.lib": "fd",
            "filters.lib": "fi",
            "hoa.lib": "ho",
            "instruments.lib": "in",
            "interpolators.lib": "it",
            "maths.lib": "ma",
            "mi.lib": "mi",
            "misceffects.lib": "ef",
            "noises.lib": "no",
            "oscillators.lib": "os",
            "phaflangers.lib": "pf",
            "physmodels.lib": "pm",
            "quantizers.lib": "qu",
            "reducemaps.lib": "rm",
            "reverbs.lib": "re",
            "routes.lib": "ro",
            "signals.lib": "si",
            "soundfiles.lib": "sf",
            "spats.lib": "sp",
            "stdfaust.lib": "sf",
            "synths.lib": "sy",
            "tonestacks.lib": "ts",
            "tubes.lib": "tu",
            "vaeffects.lib": "ve",
            "version.lib": "vl",
            "wdmodels.lib": "wd",
            "webaudio.lib": "wa",
        }

        documents = []
        total_size = 0

        for lib_file in libs_dir.glob("*.lib"):
            try:
                content = lib_file.read_text(encoding='utf-8')
                total_size += len(content)

                lib_name = lib_file.name
                prefix = LIB_PREFIXES.get(lib_name, lib_name.replace('.lib', ''))

                # Split by function documentation blocks (//--------)
                # Each block typically documents one function
                blocks = re.split(r'\n(?=//[-=]{20,})', content)

                for block in blocks:
                    if not block.strip() or len(block.strip()) < 50:
                        continue

                    # Try to extract function name from block
                    func_match = re.search(r'\((\w+)\.\)(\w+)', block)
                    if func_match:
                        func_name = f"{func_match.group(1)}.{func_match.group(2)}"
                    else:
                        # Fallback: look for function definition
                        def_match = re.search(r'^(\w+)\s*[=(]', block, re.MULTILINE)
                        func_name = f"{prefix}.{def_match.group(1)}" if def_match else lib_name

                    doc = Document(
                        page_content=block.strip(),
                        metadata={
                            "source": f"faustlibraries/{lib_name}",
                            "function": func_name,
                            "library": prefix,
                            "type": "faust_library_source",
                            "category": "faust",
                        }
                    )
                    documents.append(doc)

            except Exception as e:
                print(f"⚠️ Error reading {lib_file.name}: {e}")
                continue

        if not documents:
            return "❌ No library content found"

        # Split large chunks
        splits = self.text_splitter.split_documents(documents)

        # Add to vectorstore
        self.vectorstore.add_documents(splits)

        return f"""✅ FAUST Libraries Loaded!

📊 Stats:
- Library files: {len(list(libs_dir.glob('*.lib')))}
- Documentation blocks: {len(documents)}
- Chunks indexed: {len(splits)}
- Total size: {total_size // 1024} KB

Source: faust_documentation/faustlibraries/ (git submodule)"""

    def get_folder_stats(self):
        """Get statistics about uploaded files by folder"""
        uploads_dir = Path("./uploads")
        if not uploads_dir.exists():
            return {}

        stats = {}

        for file_path in uploads_dir.rglob("*"):
            if (
                file_path.is_file()
                and file_path.suffix.lower() in self.supported_extensions
            ):
                relative_path = file_path.relative_to(uploads_dir)
                folder = (
                    str(relative_path.parent)
                    if str(relative_path.parent) != "."
                    else "root"
                )

                if folder not in stats:
                    stats[folder] = 0
                stats[folder] += 1

        return stats
