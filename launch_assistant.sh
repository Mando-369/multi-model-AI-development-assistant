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

# Step 2: Check configured models from model_config.json
echo ""
echo "📦 Verifying configured models..."
if [ -f "model_config.json" ]; then
    # Extract model IDs from config
    reasoning_model=$(python3 -c "import json; print(json.load(open('model_config.json'))['reasoning_model']['model_id'])" 2>/dev/null || echo "deepseek-r1:32b")
    fast_model=$(python3 -c "import json; print(json.load(open('model_config.json'))['fast_model']['model_id'])" 2>/dev/null || echo "qwen2.5:32b")
else
    reasoning_model="deepseek-r1:32b"
    fast_model="qwen2.5:32b"
fi

for model in "$reasoning_model" "$fast_model"; do
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

# Step 4: Check model configuration
echo ""
echo "🧠 Checking model configuration..."
if [ -f "model_config.json" ]; then
    echo "✅ Model config found (model_config.json)"
    echo "   Change models via ⚙️ Model Setup tab in the UI"
else
    echo "⚠️  No model_config.json - will use defaults"
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