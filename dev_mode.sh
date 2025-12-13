#!/bin/bash

echo "🔧 Launching Development Mode with Claude Code"
echo "=============================================="

# Use script directory as project path
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Check if Claude Code is initialized
if [ ! -f "CLAUDE.md" ] && [ ! -f "claude.md" ]; then
    echo "Initializing Claude Code..."
    claude init
fi

# Show current model configuration
echo ""
echo "📦 Current Model Configuration:"
if [ -f "model_config.json" ]; then
    cat model_config.json
else
    echo "  (using defaults - deepseek-r1:32b + qwen2.5:32b)"
fi

# Launch Claude Code for development
echo ""
echo "Starting Claude Code development assistant..."
echo ""
echo "Useful commands:"
echo "  - Check model config: cat model_config.json"
echo "  - Test components: ./test_components.sh models"
echo "  - Run app: streamlit run main.py"
echo ""

claude
