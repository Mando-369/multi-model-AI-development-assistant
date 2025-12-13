# Local AI Coding Assistant

**A local, offline AI reasoning assistant for FAUST/JUCE audio DSP development**

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30%2B-FF4B4B)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20(M4%20Max)-silver)](https://www.apple.com/)

## Quick Start

```bash
source venv/bin/activate
streamlit run main.py
# Access at http://localhost:8501
```

---

## Overview

A **local, offline AI assistant** for deep reasoning and complex problem-solving. Designed to work alongside your preferred coding tools (Claude Code, GitHub Codex, Cursor, etc.) - you get local reasoning power with configurable models, then copy/export the results to your implementation tool of choice.

### Why This Approach?

| This Assistant (Offline) | Your Coding Tool (Online) |
|--------------------------|---------------------------|
| Deep reasoning & planning | Code implementation |
| Complex problem decomposition | File editing & refactoring |
| Architecture decisions | Git operations |
| Algorithm design | Testing & debugging |
| Math/physics calculations | Project management |

**The Hybrid Workflow**: Use DeepSeek locally for heavy thinking, export the reasoning to Claude Code/Codex for implementation. Best of both worlds - privacy for reasoning, power for coding.

## Key Features

- **Project Meta System**: Strategic planning with PROJECT_META.md per project
- **Orchestrator Agent**: Cross-agent coordination, roadmaps, milestones
- **2-Model System**: Configurable Reasoning + Fast models (select any Ollama model)
- **Specialist Agent Modes**: FAUST, JUCE, Math, Physics/Electronics
- **Context Hierarchy**: All agents see project overview + their specialist context
- **Export Queue**: Items ready for Claude Code implementation
- **Knowledge Base**: FAUST/JUCE documentation with ChromaDB vector search
- **100% Local**: Runs entirely on your machine via Ollama

## Models

Models are **configurable** via the **⚙️ Model Setup** tab. Select any installed Ollama model for each role:

| Role | Purpose | Default |
|------|---------|---------|
| **Reasoning** | Deep reasoning, planning, architecture | `deepseek-r1:32b` |
| **Fast** | Summarization, titles, quick tasks | `qwen2.5:32b` |

Change models anytime - configuration persists in `model_config.json`.

## Specialist Modes

| Mode | Icon | Focus |
|------|------|-------|
| Orchestrator | 📋 | Project management, roadmaps, cross-agent coordination |
| General | 🤖 | General-purpose reasoning |
| FAUST | 🎛️ | DSP language, signal flow, libraries |
| JUCE | 🎹 | C++ framework, audio plugins, VST/AU |
| Math | 📐 | DSP math, filters, algorithms |
| Physics | ⚡ | Circuits, acoustics, electronics |

## Requirements

### System Requirements
- **macOS** with Apple Silicon (M4 Max recommended)
- **64GB+ RAM** (32B models run well on 64GB)
- **Python 3.10+**

### Model Requirements
- **Ollama** installed and running
- Models:
  - `deepseek-r1:32b` - Primary reasoning model
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
ollama pull deepseek-r1:32b
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

1. **Create a named project** (Project Meta not available for Default)
2. **Define vision & roadmap** in Project Meta tab
3. **Work with specialist agents** (FAUST, JUCE, etc.) in AI Chat
4. **Sync progress** back to Project Meta using Orchestrator
5. **Export refined items** to Claude Code for implementation

### Interface Tabs

| Tab | Description |
|-----|-------------|
| **📋 Project Meta** | Strategic planning, roadmap, Orchestrator chat |
| **💬 AI Chat** | Main conversation with specialist modes |
| **📝 Code Editor** | File browser and syntax-highlighted editor |
| **📚 Knowledge Base** | Upload and manage documentation |
| **🖥️ System Monitor** | System status dashboard |
| **⚙️ Model Setup** | Configure which Ollama models to use |

## Project Structure

```
multi-model-AI-development-assistant/
├── main.py                    # Streamlit entry point
├── model_config.json          # Model role configuration
├── src/
│   ├── core/
│   │   ├── multi_model_system.py    # Model orchestration & context injection
│   │   ├── model_backends.py        # Backend abstraction (Ollama, HuggingFace)
│   │   ├── model_config.py          # Model configuration manager
│   │   ├── project_meta_manager.py  # PROJECT_META.md operations
│   │   ├── prompts.py               # System prompts & agent modes
│   │   ├── project_manager.py       # Project management
│   │   └── context_enhancer.py      # RAG context enhancement
│   └── ui/
│       ├── project_meta_ui.py       # Project Meta tab
│       ├── model_setup_ui.py        # Model Setup tab
│       ├── ui_components.py         # UI components
│       ├── editor_ui.py             # Code editor
│       └── file_browser.py          # File browser
├── chroma_db/                 # Vector database
├── projects/                  # User projects & saved sessions
│   └── {project}/
│       ├── PROJECT_META.md          # Strategic planning document
│       └── agents/                  # Per-agent context files
└── requirements.txt
```

## Saved Sessions

Sessions are saved to `projects/{project}/reasoning/` with filenames like:
- `faust_20241204_143052.md` - FAUST mode session
- `juce_20241204_150312.md` - JUCE mode session
- `physics_20241204_161523.md` - Physics mode session

Easy to identify which specialist mode was used!

## Roadmap

### Current (v2.2)
- [x] **Dynamic Model Selection** - Choose any Ollama model for Reasoning/Fast roles
- [x] **Model Setup Tab** - UI for model configuration
- [x] **Backend Abstraction** - Prepared for HuggingFace/Transformers support

### Completed (v2.1)
- [x] Project Meta System with PROJECT_META.md per project
- [x] Orchestrator agent mode (roadmaps, cross-agent coordination)
- [x] Context hierarchy (all agents see project overview)
- [x] Sync from Agents feature (merge/replace options)
- [x] Export Queue for Claude Code implementation

### Completed (v2.0)
- [x] 2-model simplified architecture
- [x] Specialist agent modes (FAUST/JUCE/Math/Physics)
- [x] Export buttons (Copy/Save/Format)
- [x] Summarization tools
- [x] Persistent tab navigation

### Future
- [ ] **HuggingFace Backend** - GLM-4.6V and other Transformers models via MPS
- [ ] **IDE Integration** - Cline/Continue.dev integration when model chaining is supported
- [ ] **MCP Server** - Expose ChromaDB knowledge base to external tools
- [ ] **Voice input** - Whisper integration for hands-free queries

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

## License

MIT License - see [LICENSE](LICENSE) file.

## Acknowledgments

- [Ollama](https://ollama.ai/) for local model serving
- [Streamlit](https://streamlit.io/) for the web interface
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [FAUST](https://faust.grame.fr/) and [JUCE](https://juce.com/) communities

---

**Built for audio DSP developers who value privacy and local-first tooling.**
