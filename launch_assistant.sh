#!/bin/bash

echo "Launching Multi-Model AI Development Assistant on M4 Max"
echo "=================================================="

# Step 1: Check and start Ollama service
echo "🔧 Checking Ollama service..."
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve &
    sleep 3  # Give it time to start
else
    echo "✅ Ollama service already running"
fi

# Step 2: Pull/verify models (don't run them - just ensure they're available)
echo ""
echo "📦 Verifying models..."
models=("deepseek-r1:70b" "qwen2.5-coder:32b" "qwen2.5:32b" "nomic-embed-text")
for model in "${models[@]}"; do
    if ollama list | grep -q "$model"; then
        echo "✅ $model ready"
    else
        echo "📥 Pulling $model..."
        ollama pull "$model"
    fi
done

# Step 3: Check Python environment
echo ""
echo "🐍 Checking Python environment..."
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Step 4: Check HRM availability
echo ""
echo "🧠 Checking HRM module..."
if [ -d "lib/hrm" ]; then
    echo "✅ HRM found - MPS acceleration available on M4 Max"
    export PYTORCH_ENABLE_MPS_FALLBACK=1
else
    echo "⚠️  HRM not found - running without hierarchical reasoning"
fi

# Step 5: Check ChromaDB databases
echo ""
echo "💾 Checking knowledge bases..."
if [ -d "chroma_db" ]; then
    size=$(du -sh chroma_db | cut -f1)
    echo "✅ Main ChromaDB found (${size})"
fi
if [ -d "knowledge_db" ]; then
    size=$(du -sh knowledge_db | cut -f1)
    echo "✅ Knowledge DB found (${size})"
fi

# Step 6: Set environment variables
echo ""
echo "⚙️  Setting environment..."
export TOKENIZERS_PARALLELISM=false  # Prevent warning
export PYTHONUNBUFFERED=1  # Real-time output

# Step 7: Launch the actual Streamlit app
echo ""
echo "🌐 Launching Streamlit interface..."
echo "=================================================="
echo ""

# Run Streamlit (this is your actual app!)
streamlit run main.py \
    --server.port 8501 \
    --server.address localhost \
    --server.maxUploadSize 200 \
    --theme.base dark

# Note: The script will stay running with Streamlit
# Press Ctrl+C to stop