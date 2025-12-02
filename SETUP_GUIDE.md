# Multi-Model AI Development Assistant

## Enhanced Features

- **HRM (Hierarchical Reasoning Model)** - The brain supervising all models, task decomposition and orchestration
- **DeepSeek-R1:70B** - Leading reasoning model for debugging and complex analysis
- **Qwen2.5-Coder:32B** - Best-in-class coding model for implementation
- **Qwen2.5:32B / Qwen2-Math** - Strongest model for math/physics computations
- **Integrated Code Editor** with syntax highlighting for 20+ languages
- **AI-Powered Code Editing** with change highlighting and diff view
- **Project-based organization** with separate chat histories
- **File browser** with include/exclude patterns
- **Direct file editing** - no copy-paste needed
- **Persistent knowledge base** using ChromaDB
- **FAUST/JUCE documentation integration** for audio DSP development  

## Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed ([Download here](https://ollama.ai/))
3. **GPU Requirements**:
   - NVIDIA GPU with CUDA 12.6+ (recommended for HRM training)
   - OR Apple Silicon M4 Max with MPS support (for inference)
   - Minimum 48GB VRAM for running all models simultaneously
4. **Tesseract OCR** for image processing (optional)

### Installing Tesseract (Optional)
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

## Installation Steps

### 1. Clone/Download the Project
```bash
git clone <your-repo-url>
cd multi-model-glm-assistant
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Ollama Models

#### Required Models
```bash
# Reasoning & debugging (70B - requires significant VRAM)
ollama pull deepseek-r1:70b

# Best coding model
ollama pull qwen2.5-coder:32b

# Math/physics specialist
ollama pull qwen2.5:32b

# Embedding model for knowledge base
ollama pull nomic-embed-text
```

#### Optional Models
```bash
# Math-specific variant
ollama pull qwen2-math

# Smaller alternatives for limited VRAM
ollama pull deepseek-r1:32b
ollama pull qwen2.5-coder:14b
```

#### Verify Installation
```bash
ollama list
```

### 5. Install HRM (Hierarchical Reasoning Model)

HRM acts as the orchestration brain, managing task decomposition and model routing.

```bash
# HRM is cloned to lib/hrm during setup
cd lib/hrm

# Install HRM dependencies
pip install -r requirements.txt

# For NVIDIA GPUs - Install FlashAttention
# Hopper GPUs (H100, etc.):
git clone git@github.com:Dao-AILab/flash-attention.git
cd flash-attention/hopper && python setup.py install

# Ampere or earlier GPUs:
pip install flash-attn
```

#### Download Pre-trained HRM Checkpoints
Available from HuggingFace:
- [ARC-AGI-2](https://huggingface.co/sapientinc/HRM-checkpoint-ARC-2)
- [Sudoku](https://huggingface.co/sapientinc/HRM-checkpoint-sudoku-extreme)
- [Maze](https://huggingface.co/sapientinc/HRM-checkpoint-maze-30x30-hard)

### 6. Create Required Directories
```bash
mkdir -p uploads projects knowledge_db faust_documentation
```

## Quick Start

### 1. Launch the Application
```bash
streamlit run main.py
```

### 2. First-Time Setup
1. **Check Model Status** - Use the "Check Model Availability" button in the sidebar
2. **Create a Project** - Click "➕ New Project" and create your first project
3. **Upload Documentation** - Go to Knowledge Base tab and upload your files

### 3. Start Coding!
1. **Switch to Code Editor tab**
2. **Create or open files** using the file browser
3. **Ask AI to modify your code** with specific instructions
4. **Review highlighted changes** in the diff viewer
5. **Accept or reject** AI suggestions
6. **Save directly** to your files

## Usage Examples

### Basic Code Editing Workflow

1. **Open a Python file** in the Code Editor tab
2. **Select your code** and ask AI: "Add docstrings to all functions"
3. **Review the changes** in the highlighted diff view:
   - 🟢 **Green lines** = AI additions
   - 🔴 **Red lines** = AI deletions  
   - 🔵 **Blue lines** = AI modifications
4. **Accept or reject** the changes
5. **Save directly** to your file

### FAUST DSP Development

1. **Create a new .dsp file** 
2. **Ask Code Llama**: "Create a stereo reverb effect with adjustable room size"
3. **Review the FAUST code** with syntax highlighting
4. **Iterate with AI** to refine the algorithm
5. **Save and test** your DSP code

### Project Organization

1. **Create specialized projects** for different codebases
2. **Set include/exclude patterns** to focus on relevant files
3. **Use project-specific chat history** for context
4. **Organize files** with the integrated file browser

## Configuration

### File Filtering Patterns

**Default Include Patterns:**
- `*.py` (Python files)
- `*.cpp`, `*.h`, `*.hpp` (C++ files)  
- `*.dsp`, `*.lib`, `*.fst` (FAUST files)
- `*.txt`, `*.md` (Documentation)
- `*.json` (Configuration files)

**Default Exclude Patterns:**
- `__pycache__`, `*.pyc` (Python cache)
- `.git` (Git repository data)
- `node_modules` (Node.js dependencies)
- `*.exe`, `*.dll` (Binaries)

### Editor Settings

- **Theme**: Monokai (dark theme optimized for code)
- **Font Size**: 14px (adjustable per project)
- **Tab Size**: 4 spaces
- **Language Detection**: Automatic based on file extension

## FAUST Integration

### Specialized Features for Audio DSP

1. **FAUST Documentation**: Load complete FAUST library documentation
2. **Code Llama Specialist**: Trained specifically for FAUST syntax and DSP concepts
3. **Quick Actions**: Pre-built prompts for common FAUST patterns:
   - Basic oscillators
   - Filter designs  
   - Effect chains
4. **Syntax Support**: Full highlighting for `.dsp` and `.lib` files

### Loading FAUST Documentation
```bash
# Run the documentation downloader
python download_faust_docs_complete.py
```

Then use the "📥 Load FAUST Docs" button in the Knowledge Base tab.

## Troubleshooting

### Model Loading Issues

**Problem**: "❌ Model Missing" errors  
**Solution**: 
```bash
# Re-pull the missing model
ollama pull <model-name>

# Restart Ollama service
ollama serve
```

### Code Editor Not Loading

**Problem**: Blank editor or loading issues  
**Solution**:
1. Clear browser cache
2. Restart Streamlit: `Ctrl+C` then `streamlit run main.py`
3. Check console for JavaScript errors

### File Permission Errors

**Problem**: Cannot save files  
**Solution**:
```bash
# Fix permissions (Unix/Linux/macOS)
chmod -R 755 projects/
chmod -R 755 uploads/

# On Windows, run as administrator if needed
```

### Memory Issues with Large Models

**Problem**: System running slow or out of memory
**Solutions**:
1. **Use smaller model variants**:
   ```bash
   ollama pull deepseek-r1:32b      # Instead of 70b
   ollama pull qwen2.5-coder:14b    # Instead of 32b
   ```
2. **Load models sequentially** - Unload unused models with `ollama stop <model>`
3. **Increase system swap space**
4. **For Apple Silicon**: Ensure sufficient unified memory allocation

## System Requirements

### Minimum Requirements
- **RAM**: 64GB (for running 70B models)
- **VRAM**: 48GB+ (for all models loaded)
- **Storage**: 200GB free space (models + data)
- **CPU**: Modern multi-core processor
- **GPU**: Required - NVIDIA RTX 4090/A100 or Apple M4 Max

### Recommended Requirements
- **RAM**: 128GB
- **VRAM**: 80GB+ (for concurrent model loading)
- **GPU**: NVIDIA H100 or Apple M4 Max with 128GB unified memory
- **Storage**: NVMe SSD with 500GB+ free space

## Advanced Usage

### Custom Model Integration

Models are configured in `src/core/multi_model_system.py`:

```python
self.models = {
    "DeepSeek-R1 (Reasoning)": "deepseek-r1:70b",
    "Qwen2.5-Coder (Implementation)": "qwen2.5-coder:32b",
    "Qwen2.5 (Math/Physics)": "qwen2.5:32b",
    "Your Custom Model": "your-model-name"  # Add custom models here
}
```

### Model Routing

HRM automatically routes tasks to appropriate models:
- **Reasoning/debugging**: DeepSeek-R1:70B
- **Code implementation**: Qwen2.5-Coder:32B
- **Math/physics**: Qwen2.5:32B or Qwen2-Math
- **Task orchestration**: HRM

### Extending File Type Support

Modify `editor_ui.py` to add new language modes:

```python
language_map = {
    '.py': 'python',
    '.your_ext': 'your_language_mode',  # Add this
    # ... existing mappings
}
```

## Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Test your changes** thoroughly
4. **Submit a pull request**

## Additional Resources

- [HRM - Hierarchical Reasoning Model](https://github.com/sapientinc/HRM)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [FAUST Documentation](https://faustdoc.grame.fr/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)

## Reporting Issues

If you encounter problems:

1. **Check the console** for error messages
2. **Verify model installation** with `ollama list`
3. **Create an issue** with:
   - System information
   - Error messages
   - Steps to reproduce
   - Screenshots (if applicable)

---

The integrated code editor enables seamless iteration on projects with AI assistance while maintaining full control over the codebase.