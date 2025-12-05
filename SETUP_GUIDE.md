# Local AI Coding Assistant - Setup Guide

## Overview

A local, offline AI reasoning assistant for FAUST/JUCE audio DSP development. Use alongside your preferred coding tools (Claude Code, Cursor, Codex).

**Key Features:**
- **DeepSeek-R1:32B** - Deep reasoning, planning, architecture decisions
- **Qwen2.5:32B** - Fast summarization, titles, quick tasks
- **Specialist Agent Modes** - FAUST, JUCE, Math, Physics/Electronics
- **Export Buttons** - Copy, Save, Format for Claude
- **Integrated Code Editor** with syntax highlighting
- **ChromaDB Knowledge Base** with FAUST/JUCE documentation

## Prerequisites

1. **Python 3.10+** installed
2. **Ollama** installed ([Download here](https://ollama.ai/))
3. **System Requirements**:
   - macOS with Apple Silicon (M4 Max recommended)
   - 64GB+ RAM (32B models run well on 64GB)
   - 200GB+ storage for models

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Mando-369/multi-model-AI-development-assistant.git
cd multi-model-AI-development-assistant
```

### 2. Install Ollama and Models
```bash
# Install Ollama (macOS)
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull required models
ollama pull deepseek-r1:32b    # Primary reasoning
ollama pull qwen2.5:32b        # Fast summarization

# Verify installation
ollama list
```

### 3. Create Virtual Environment
```bash
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Load Documentation (Optional)
```bash
python scripts/load_documentation.py
```

### 6. Start the Application
```bash
streamlit run main.py
# Access at http://localhost:8501
```

## Usage

### Specialist Agent Modes

| Mode | Icon | Focus |
|------|------|-------|
| General | 🤖 | General-purpose reasoning |
| FAUST | 🎛️ | DSP language, signal flow, block diagrams |
| JUCE | 🎹 | C++ audio framework, VST/AU plugins |
| Math | 📐 | DSP algorithms, filter design |
| Physics | ⚡ | Circuits, acoustics, electronics |

### Hybrid Workflow

1. **Select Specialist Mode** (FAUST, JUCE, Math, etc.)
2. **Ask DeepSeek** your complex question
3. **Wait for reasoning** (slower but thorough)
4. **Export the result**:
   - 📋 **Copy Response** → Paste into Claude Code
   - 💾 **Save to Project** → Creates timestamped .md file
   - 📤 **Format for Claude** → Ready-to-paste format

### Interface Tabs

| Tab | Description |
|-----|-------------|
| **💬 AI Chat** | Main conversation with specialist modes |
| **📝 Code Editor** | File browser and syntax-highlighted editor |
| **📚 Knowledge Base** | Upload and manage documentation |
| **🖥️ System Monitor** | System status dashboard |

## Configuration

### Model Configuration

Models are defined in `src/core/multi_model_system.py`:

```python
self.models = {
    "DeepSeek-R1:32B (Reasoning)": "deepseek-r1:32b",
    "Qwen2.5:32B (Fast)": "qwen2.5:32b",
}
```

### Specialist Modes

Agent modes are defined in `src/core/prompts.py`:

```python
AGENT_MODES = {
    "General": {...},
    "FAUST": {...},
    "JUCE": {...},
    "Math": {...},
    "Physics": {...},
}
```

### File Filtering Patterns

**Default Include:**
- `*.py`, `*.cpp`, `*.h`, `*.hpp`
- `*.dsp`, `*.lib`, `*.fst` (FAUST)
- `*.txt`, `*.md`, `*.json`

**Default Exclude:**
- `__pycache__`, `*.pyc`
- `.git`, `node_modules`
- `*.exe`, `*.dll`

## Troubleshooting

### Ollama Connection Error
```bash
ollama serve    # Ensure Ollama is running
ollama list     # Check available models
```

### Memory Issues
```bash
# Use smaller model variants
ollama pull deepseek-r1:14b  # Use smaller variant if needed
```

### Reset Knowledge Base
```bash
rm -rf chroma_db/
python scripts/load_documentation.py
```

### Model Loading Issues
```bash
# Re-pull the missing model
ollama pull <model-name>

# Restart Ollama service
ollama serve
```

## Project Structure

```
multi-model-AI-development-assistant/
├── main.py                    # Streamlit entry point
├── src/
│   ├── core/
│   │   ├── multi_model_system.py    # Model orchestration
│   │   ├── prompts.py               # System prompts & agent modes
│   │   ├── project_manager.py       # Project management
│   │   └── context_enhancer.py      # RAG context enhancement
│   └── ui/
│       ├── ui_components.py         # UI components
│       ├── editor_ui.py             # Code editor
│       └── file_browser.py          # File browser
├── chroma_db/                 # Vector database
├── projects/                  # User projects & saved sessions
└── requirements.txt
```

## Saved Sessions

Sessions are saved to `projects/{project}/reasoning/` with filenames like:
- `faust_20241204_143052.md` - FAUST mode session
- `juce_20241204_150312.md` - JUCE mode session
- `physics_20241204_161523.md` - Physics mode session

## Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [FAUST Documentation](https://faustdoc.grame.fr/)
- [JUCE Documentation](https://juce.com/learn/documentation)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

*Updated: December 2024 - v2.0*
