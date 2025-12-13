#!/bin/bash

# Multi-Model AI Development Assistant
# Quick Setup Script for macOS (Apple Silicon M4 Max)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_error "$1 is not installed"
        return 1
    fi
}

# Main setup
print_header "Multi-Model AI Development Assistant Setup"

# Check system
print_header "Checking System Requirements"

# Check for macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS. Please modify for your OS."
    exit 1
fi

# Check for Apple Silicon
if [[ $(uname -m) != "arm64" ]]; then
    print_warning "This system is optimized for Apple Silicon (M1/M2/M3/M4)"
fi

# Check Python
if check_command python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python version: $PYTHON_VERSION"
else
    print_error "Python 3.10+ is required"
    echo "Install with: brew install python@3.10"
    exit 1
fi

# Check and install Homebrew if needed
print_header "Checking Package Managers"
if ! check_command brew; then
    print_warning "Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Ollama
print_header "Setting up Ollama"
if ! check_command ollama; then
    print_warning "Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
    print_success "Ollama installed"
else
    print_success "Ollama is already installed"
fi

# Start Ollama service
print_header "Starting Ollama Service"
if pgrep -x "ollama" > /dev/null; then
    print_success "Ollama service is running"
else
    print_warning "Starting Ollama service..."
    ollama serve &
    sleep 5
    print_success "Ollama service started"
fi

# Pull required models
print_header "Downloading AI Models (this may take a while)"

# Default models (can be changed later in Model Setup tab)
models=("deepseek-r1:32b" "qwen2.5:32b")
for model in "${models[@]}"; do
    echo -e "\n${YELLOW}Pulling $model...${NC}"
    if ollama list | grep -q "$model"; then
        print_success "$model already available"
    else
        ollama pull $model
        print_success "$model downloaded"
    fi
done

# Create virtual environment
print_header "Setting up Python Environment"

if [ -d "venv" ]; then
    print_warning "Virtual environment already exists"
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
pip install --upgrade pip -q
print_success "pip upgraded"

# Install requirements
print_header "Installing Python Dependencies"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt -q
    print_success "Dependencies installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Create necessary directories
print_header "Creating Project Structure"

directories=(
    "src/core"
    "src/ui"
    "src/integrations"
    "src/monitoring"
    "scripts"
    "tests"
    "logs"
    "config"
    "chroma_db"
    "projects"
    "faust_documentation"
    "juce_documentation" 
    "python_documentation"
    "models/cached"
)

for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        print_success "Created $dir"
    else
        print_success "$dir already exists"
    fi
done

# Initialize ChromaDB
print_header "Initializing ChromaDB"
cat > init_chromadb.py << 'EOF'
import chromadb
from chromadb.config import Settings

# Initialize ChromaDB
client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(
        anonymized_telemetry=False,
        allow_reset=True
    )
)

# Create collections
collections = [
    "faust_docs",
    "juce_docs",
    "python_docs",
    "cpp_docs",
    "project_context"
]

for collection_name in collections:
    try:
        client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"✓ Created collection: {collection_name}")
    except:
        print(f"✓ Collection exists: {collection_name}")

print("\n✓ ChromaDB initialized successfully")
EOF

python init_chromadb.py
rm init_chromadb.py

# Create model config file (if not exists)
print_header "Creating Model Configuration"
if [ ! -f "model_config.json" ]; then
    cat > model_config.json << 'EOF'
{
  "reasoning_model": {
    "model_id": "deepseek-r1:32b",
    "backend": "ollama",
    "display_name": "DeepSeek-R1:32B (Reasoning)"
  },
  "fast_model": {
    "model_id": "qwen2.5:32b",
    "backend": "ollama",
    "display_name": "Qwen2.5:32B (Fast)"
  }
}
EOF
    print_success "Model configuration created (model_config.json)"
else
    print_success "Model configuration already exists"
fi

# Download sample documentation
print_header "Downloading Sample Documentation"

# FAUST sample
if [ ! -f "faust_documentation/basics.md" ]; then
    cat > faust_documentation/basics.md << 'EOF'
# FAUST Basics

FAUST (Functional Audio Stream) is a functional programming language for sound synthesis and audio processing.

## Basic Syntax
```faust
// Simple sine oscillator
process = os.osc(440);

// Volume control
process = os.osc(440) * hslider("volume", 0.5, 0, 1, 0.01);
```
EOF
    print_success "Created sample FAUST documentation"
fi

# Create run script
print_header "Creating Run Script"
cat > run.sh << 'EOF'
#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve &
    sleep 5
fi

# Run Streamlit app
echo "Starting Multi-Model AI Assistant..."
echo "Opening browser at http://localhost:8501"
streamlit run main.py
EOF

chmod +x run.sh
print_success "Run script created"

# Final message
print_header "Setup Complete! 🎉"

echo -e "${GREEN}Multi-Model AI Development Assistant is ready!${NC}\n"
echo "To start the application:"
echo -e "  ${BLUE}./run.sh${NC}"
echo ""
echo "Or manually:"
echo -e "  ${BLUE}source venv/bin/activate${NC}"
echo -e "  ${BLUE}streamlit run main.py${NC}"
echo ""
echo "Access the application at:"
echo -e "  ${BLUE}http://localhost:8501${NC}"
echo ""
print_warning "Note: First run may be slow as models are loaded into memory"

# Offer to start now
echo ""
read -p "Would you like to start the application now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ./run.sh
fi