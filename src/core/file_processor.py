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

    def load_faust_documentation(self):
        """Load comprehensive FAUST documentation"""
        faust_docs_dir = Path("./faust_documentation")
        if not faust_docs_dir.exists():
            return "❌ No FAUST documentation found. Run download_faust_docs_complete.py first."

        processed_count = 0
        library_count = 0
        manual_count = 0

        for doc_file in faust_docs_dir.glob("*.txt"):
            try:
                with open(doc_file, "r", encoding="utf-8") as f:
                    first_lines = f.read(500)

                if "faustlibraries.grame.fr" in first_lines:
                    library_count += 1
                    doc_type = "🔧 Library"
                else:
                    manual_count += 1
                    doc_type = "📚 Manual"

                result = self.process_file(str(doc_file))
                processed_count += 1
                print(f"✅ {doc_type}: {doc_file.name}")

            except Exception as e:
                print(f"❌ Error processing {doc_file}: {e}")

        return f"""🎵 FAUST Documentation Loaded Successfully!

📊 Processed {processed_count} files:
🔧 Library docs: {library_count} files
📚 Manual docs: {manual_count} files

Your models now have access to:
- Complete FAUST library reference
- Language syntax and primitives
- DSP algorithms and examples
- Physical modeling techniques"""

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
