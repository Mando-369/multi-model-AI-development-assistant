#!/bin/bash

# Test components script for Multi-Model AI Development Assistant

case "$1" in
    "ollama")
        echo "Testing Ollama connection..."
        ollama list
        echo ""
        echo "Testing model response..."
        echo "Say hello" | ollama run deepseek-r1:32b --verbose 2>&1 | head -20
        ;;
    "chromadb")
        echo "Testing ChromaDB..."
        python -c "
import chromadb
client = chromadb.PersistentClient(path='./chroma_db')
collections = client.list_collections()
print(f'ChromaDB OK - {len(collections)} collections')
for c in collections:
    print(f'  - {c.name}')
"
        ;;
    "models")
        echo "Testing model configuration..."
        python -c "
from src.core.model_config import get_model_config
config = get_model_config()
print('Model Configuration:')
print(f'  Reasoning: {config.get_reasoning_model().display_name}')
print(f'            -> {config.get_reasoning_model().model_id}')
print(f'  Fast:      {config.get_fast_model().display_name}')
print(f'            -> {config.get_fast_model().model_id}')
"
        ;;
    "backends")
        echo "Testing model backends..."
        python -c "
from src.core.model_backends import get_backend_manager
bm = get_backend_manager()
print('Available backends:', list(bm.backends.keys()))
ollama = bm.get_backend('ollama')
if ollama:
    models = ollama.list_models()
    print(f'Ollama models found: {len(models)}')
    for m in models[:5]:
        print(f'  - {m.name} ({m.id})')
"
        ;;
    "streamlit")
        echo "Testing Streamlit..."
        streamlit run main.py --server.headless true &
        sleep 5
        curl -s http://localhost:8501 > /dev/null && echo "Streamlit OK" || echo "Streamlit FAILED"
        pkill -f "streamlit run"
        ;;
    *)
        echo "Usage: $0 {ollama|chromadb|models|backends|streamlit}"
        echo ""
        echo "  ollama    - Test Ollama connection and models"
        echo "  chromadb  - Test ChromaDB vector store"
        echo "  models    - Test model configuration"
        echo "  backends  - Test backend manager"
        echo "  streamlit - Test Streamlit app startup"
        ;;
esac
