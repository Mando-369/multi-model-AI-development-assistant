# Local AI Coding Assistant

**A local, offline AI reasoning assistant for FAUST/JUCE audio DSP development**

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30%2B-FF4B4B)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20(M4%20Max)-silver)](https://www.apple.com/)

## Overview

A **local, offline AI assistant** for deep reasoning and complex problem-solving. Designed to work alongside your preferred coding tools (Claude Code, GitHub Codex, Cursor, etc.) - you get the reasoning power of DeepSeek-R1:70B running locally, then copy/export the results to your implementation tool of choice.

### Why This Approach?

| This Assistant (Offline) | Your Coding Tool (Online) |
|--------------------------|---------------------------|
| Deep reasoning & planning | Code implementation |
| Complex problem decomposition | File editing & refactoring |
| Architecture decisions | Git operations |
| Algorithm design | Testing & debugging |
| Math/physics calculations | Project management |

**The Hybrid Workflow**: Use DeepSeek locally for heavy thinking, export the reasoning to Claude Code/Codex for implementation. Best of both worlds - privacy for reasoning, power for coding.

### What Changed (HRM Removal)

We removed the **Hierarchical Reasoning Model (HRM)** integration. After investigation, HRM turned out to be designed for puzzle-solving (Sudoku, mazes, logic puzzles) rather than code understanding. The "intelligent routing" was actually just regex pattern matching with no real reasoning capability.

**New simplified approach**: 2 models with clear purposes, no fake "AI routing".

## Key Features

- **2-Model System**: DeepSeek-R1:70B (reasoning) + Qwen2.5:32B (fast tasks)
- **Specialist Agent Modes**: FAUST, JUCE, Math, Physics/Electronics
- **Export Buttons**: Copy, Save to Project, Format for Claude
- **Summarization Tools**: Generate titles, quick summaries using Qwen
- **Knowledge Base**: FAUST/JUCE documentation with ChromaDB vector search
- **Integrated Code Editor**: Syntax highlighting, AI-powered editing with diff view
- **100% Local**: Runs entirely on your machine via Ollama

## Models

| Model | Purpose | When to Use |
|-------|---------|-------------|
| **DeepSeek-R1:70B** | Deep reasoning, planning, architecture | Complex questions, debugging, design decisions |
| **Qwen2.5:32B** | Fast summarization, titles | Quick tasks, generating titles, simple lookups |

## Specialist Modes

| Mode | Icon | Focus |
|------|------|-------|
| General | 🤖 | General-purpose reasoning |
| FAUST | 🎛️ | DSP language, signal flow, libraries |
| JUCE | 🎹 | C++ framework, audio plugins, VST/AU |
| Math | 📐 | DSP math, filters, algorithms |
| Physics | ⚡ | Circuits, acoustics, electronics |

## Requirements

### System Requirements
- **macOS** with Apple Silicon (M4 Max recommended)
- **64GB+ RAM** (128GB recommended for 70B model)
- **Python 3.10+**

### Model Requirements
- **Ollama** installed and running
- Models:
  - `deepseek-r1:70b` - Primary reasoning model
  - `qwen2.5:32b` - Fast summarization

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
ollama pull deepseek-r1:70b
ollama pull qwen2.5:32b
```

### 3. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Load Documentation (Optional)
```bash
python scripts/load_documentation.py
```

## Usage

### Starting the System
```bash
source venv/bin/activate
streamlit run main.py
# Access at http://localhost:8501
```

### Workflow Example

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
├── archive/                   # Archived HRM integration (removed)
├── chroma_db/                 # Vector database
├── projects/                  # User projects & saved sessions
└── requirements.txt
```

## Saved Sessions

Sessions are saved to `projects/{project}/reasoning/` with filenames like:
- `faust_20241204_143052.md` - FAUST mode session
- `juce_20241204_150312.md` - JUCE mode session
- `physics_20241204_161523.md` - Physics mode session

Easy to identify which specialist mode was used!

## Roadmap

### Current (v2.0)
- [x] 2-model simplified architecture
- [x] Specialist agent modes (FAUST/JUCE/Math/Physics)
- [x] Export buttons (Copy/Save/Format)
- [x] Summarization tools using Qwen
- [x] Persistent tab navigation

### Future
- [ ] **IDE Integration** - Cline/Continue.dev integration when model chaining is supported
- [ ] **MCP Server** - Expose ChromaDB knowledge base to external tools
- [ ] **Voice input** - Whisper integration for hands-free queries
- [ ] **WebAssembly FAUST** - In-browser DSP testing

## Troubleshooting

### Ollama Connection Error
```bash
ollama serve    # Ensure Ollama is running
ollama list     # Check available models
```

### Memory Issues
```bash
# Use smaller model variants
ollama pull deepseek-r1:32b  # Instead of 70b
```

### Reset Knowledge Base
```bash
rm -rf chroma_db/
python scripts/load_documentation.py
```

## License

MIT License - see [LICENSE](LICENSE) file.

## Acknowledgments

- [Ollama](https://ollama.ai/) for local model serving
- [Streamlit](https://streamlit.io/) for the web interface
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [FAUST](https://faust.grame.fr/) and [JUCE](https://juce.com/) communities

---

**Built for audio DSP developers who value privacy and local-first tooling.**
