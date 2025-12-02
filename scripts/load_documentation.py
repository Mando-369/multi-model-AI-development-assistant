#!/usr/bin/env python3
"""
Load all documentation files into ChromaDB vector store.

Usage:
    python scripts/load_documentation.py          # Load docs (skip existing)
    python scripts/load_documentation.py --reset  # Clear DB and reload all
    python scripts/load_documentation.py --update # Update only modified files
    python scripts/load_documentation.py --status # Show current DB status
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime
import hashlib
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


# Metadata file to track loaded documents
METADATA_FILE = project_root / "chroma_db" / ".doc_metadata.json"


def get_file_hash(file_path: Path) -> str:
    """Get MD5 hash of file content"""
    return hashlib.md5(file_path.read_bytes()).hexdigest()


def load_metadata() -> dict:
    """Load document metadata from file"""
    if METADATA_FILE.exists():
        return json.loads(METADATA_FILE.read_text())
    return {"files": {}, "last_updated": None}


def save_metadata(metadata: dict):
    """Save document metadata to file"""
    METADATA_FILE.parent.mkdir(exist_ok=True)
    metadata["last_updated"] = datetime.now().isoformat()
    METADATA_FILE.write_text(json.dumps(metadata, indent=2))


def init_components():
    """Initialize embeddings and vectorstore"""
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    chroma_path = project_root / "chroma_db"
    chroma_path.mkdir(exist_ok=True)

    vectorstore = Chroma(
        persist_directory=str(chroma_path),
        embedding_function=embeddings
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    return vectorstore, text_splitter, embeddings


def get_db_status():
    """Get current database status"""
    print("=" * 60)
    print("ChromaDB Knowledge Base Status")
    print("=" * 60)

    try:
        vectorstore, _, _ = init_components()
        collection = vectorstore._collection
        count = collection.count()

        print(f"\nTotal chunks in database: {count}")

        metadata = load_metadata()
        if metadata["files"]:
            print(f"\nLoaded documentation sources:")

            # Group by category
            by_category = {}
            for path, info in metadata["files"].items():
                cat = info.get("category", "unknown")
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(info)

            for category, files in by_category.items():
                total_chunks = sum(f.get("chunks", 0) for f in files)
                print(f"  {category}: {len(files)} files, {total_chunks} chunks")

            if metadata.get("last_updated"):
                print(f"\nLast updated: {metadata['last_updated']}")
        else:
            print("\nNo metadata found. Run with --reset to rebuild.")

    except Exception as e:
        print(f"\nError accessing database: {e}")

    print("=" * 60)


def reset_database():
    """Clear the database completely"""
    import shutil

    chroma_path = project_root / "chroma_db"

    if chroma_path.exists():
        print("Removing existing database...")
        shutil.rmtree(chroma_path)
        print("Database cleared.")

    chroma_path.mkdir(exist_ok=True)


def load_documentation(reset: bool = False, update_only: bool = False):
    """Load all documentation into ChromaDB

    Args:
        reset: If True, clear database before loading
        update_only: If True, only load modified files
    """
    print("=" * 60)
    print("Documentation Loader for Multi-Model AI Assistant")
    print("=" * 60)

    if reset:
        print("\n[0/5] Resetting database...")
        reset_database()

    # Load existing metadata
    metadata = load_metadata() if not reset else {"files": {}, "last_updated": None}

    print("\n[1/5] Initializing embeddings model...")
    vectorstore, text_splitter, _ = init_components()
    print("      Embeddings initialized.")

    print(f"\n[2/5] Connected to ChromaDB")

    # Documentation directories
    doc_dirs = {
        "faust_documentation": "FAUST DSP",
        "juce_documentation": "JUCE Framework",
        "python_documentation": "Python",
    }

    print("\n[3/5] Scanning documentation files...")

    total_docs = 0
    total_chunks = 0
    skipped = 0
    updated = 0

    for doc_dir, doc_type in doc_dirs.items():
        doc_path = project_root / doc_dir

        if not doc_path.exists():
            print(f"      Skipping {doc_dir} (not found)")
            continue

        txt_files = list(doc_path.glob("*.txt"))

        if not txt_files:
            print(f"      Skipping {doc_dir} (no .txt files)")
            continue

        print(f"\n      Processing {doc_type} ({len(txt_files)} files)...")

        for txt_file in txt_files:
            file_key = str(txt_file.relative_to(project_root))
            current_hash = get_file_hash(txt_file)

            # Check if file needs updating
            existing = metadata["files"].get(file_key, {})
            if update_only and existing.get("hash") == current_hash:
                skipped += 1
                continue

            try:
                content = txt_file.read_text(encoding="utf-8")

                doc = Document(
                    page_content=content,
                    metadata={
                        "source": str(txt_file),
                        "filename": txt_file.name,
                        "doc_type": doc_type,
                        "category": doc_dir,
                        "loaded_at": datetime.now().isoformat(),
                    }
                )

                chunks = text_splitter.split_documents([doc])
                vectorstore.add_documents(chunks)

                # Update metadata
                metadata["files"][file_key] = {
                    "hash": current_hash,
                    "chunks": len(chunks),
                    "category": doc_dir,
                    "doc_type": doc_type,
                    "loaded_at": datetime.now().isoformat(),
                }

                total_docs += 1
                total_chunks += len(chunks)

                if existing:
                    updated += 1
                    print(f"         Updated: {txt_file.name} ({len(chunks)} chunks)")
                else:
                    print(f"         Added: {txt_file.name} ({len(chunks)} chunks)")

            except Exception as e:
                print(f"         Error: {txt_file.name}: {e}")

    print("\n[4/5] Saving metadata...")
    save_metadata(metadata)

    print("\n[5/5] Verifying...")
    try:
        collection = vectorstore._collection
        final_count = collection.count()
        print(f"      Total chunks in ChromaDB: {final_count}")
    except Exception as e:
        print(f"      Could not verify: {e}")

    print("\n" + "=" * 60)
    print(f"COMPLETE:")
    print(f"  - Added: {total_docs - updated} new files")
    print(f"  - Updated: {updated} files")
    print(f"  - Skipped: {skipped} unchanged files")
    print(f"  - Total chunks: {total_chunks}")
    print("=" * 60)

    return total_docs, total_chunks


def main():
    parser = argparse.ArgumentParser(
        description="Load documentation into ChromaDB knowledge base",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/load_documentation.py          # First-time load
  python scripts/load_documentation.py --reset  # Clear and reload all
  python scripts/load_documentation.py --update # Update modified files only
  python scripts/load_documentation.py --status # Check current status
        """
    )

    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear database and reload all documentation"
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Only load new or modified files"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current database status"
    )

    args = parser.parse_args()

    if args.status:
        get_db_status()
    elif args.reset:
        load_documentation(reset=True, update_only=False)
    elif args.update:
        load_documentation(reset=False, update_only=True)
    else:
        # Default: load all, skip existing
        load_documentation(reset=False, update_only=True)


if __name__ == "__main__":
    main()
