# Multi-Model AI Development Assistant

**A local, offline AI reasoning assistant for FAUST/JUCE audio DSP development with real-time audio preview**

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30%2B-FF4B4B)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20(Apple%20Silicon)-silver)](https://www.apple.com/)

---

## Quick Setup (New Users)

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/Mando-369/multi-model-AI-development-assistant.git
cd multi-model-AI-development-assistant

# Run the setup script (installs everything)
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Install Ollama and pull AI models
- Create Python virtual environment
- Install all dependencies
- Clone and build faust-mcp (FAUST analysis & realtime audio)
- Install Rust (for native audio bindings)
- Build node-web-audio-api (WebAudio backend)

### Option 2: Manual Setup

See [Manual Installation](#installation) below.

---

## Starting the Assistant

After setup, start all services with:

```bash
./start_assistant.sh
```

This starts:
| Service | URL | Purpose |
|---------|-----|---------|
| Streamlit App | http://localhost:8501 | Main UI |
| FAUST Analysis | http://localhost:8765/sse | Offline audio analysis |
| FAUST Realtime | http://localhost:8000/sse | Live audio playback |
| FAUST UI | http://localhost:8787 | Parameter sliders |
| Ollama API | http://localhost:11434 | AI models |

Press `Ctrl+C` to stop all services.

---

## FAUST Integration

The assistant includes deep FAUST integration via [faust-mcp](https://github.com/sletz/faust-mcp):

| Button | Function | Server |
|--------|----------|--------|
| **✓ Syntax** | Fast syntax validation | :8000 (WASM) or local CLI fallback |
| **🎛️ Analyze** | Compile + audio metrics | :8765 (offline) |
| **▶️ Run** | Compile + live playback | :8000 (realtime) |

When a DSP is running, click the link to open the **Parameter UI** at http://localhost:8787 for real-time slider control.

### Test Input for Effects

Effects (DSPs with audio inputs) need test signals. The **Test Input** panel provides:

| Input Source | Description |
|--------------|-------------|
| **none** | No input - for generators (oscillators, synths) |
| **sine** | Sine wave with configurable frequency |
| **noise** | White noise |
| **file** | Audio file (local or URL) |

A safety check warns when running effects with "none" selected.

#### File Input Options

**Local File (recommended):**
- Select "Local File" mode
- Drag & drop audio file (wav, mp3, ogg, flac, aiff)
- Works immediately, no setup needed

**HTTP URL (advanced):**
- Select "HTTP URL" mode
- Enter URL like `http://localhost:8080/myfile.wav`
- Requires running an HTTP server to serve files:
  ```bash
  # Start server in folder with audio files
  cd /path/to/audio/files
  python -m http.server 8080

  # Now files are available at http://localhost:8080/filename.wav
  ```
- Useful for remote files or integration with other systems

**Note**: Syntax checking uses the realtime server's WASM compiler by default. Local Faust CLI is only used as fallback when the realtime server isn't running.

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

**Ollama Cloud Models**: With Ollama v0.12+, you can also select cloud-hosted models like `cloud/glm-4.6` or `cloud/qwen3-coder:480b` for access to larger models that won't fit locally. These work seamlessly with the same API.

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
- **macOS** with Apple Silicon (M1/M2/M3/M4)
- **32GB+ RAM** (64GB recommended for 32B models)
- **Python 3.10+**
- **Node.js 18+** (for realtime audio)
- **Git** (for cloning repos)

### Optional (installed automatically by setup.sh)
- **Rust** - Required for building node-web-audio-api
- **Faust compiler** - Optional fallback for syntax checking when realtime server not running (`brew install faust`)

### AI Models
- **Ollama** - Local model server (also supports [cloud models](https://ollama.com/blog/cloud-models))
- `deepseek-r1:32b` - Primary reasoning model (local)
- `qwen2.5:32b` - Fast summarization (local)

#### Ollama Cloud Models (Optional)
With Ollama v0.12+, you can also use cloud-hosted models for larger models that won't fit locally:
- `cloud/glm-4.6` - GLM-4.6 (cloud)
- `cloud/qwen3-coder:480b` - Qwen3 Coder 480B (cloud)

Cloud models work seamlessly with the same API. Free tier available with usage limits. See [Ollama Cloud](https://ollama.com/cloud) for details.

## Installation

### Automated (Recommended)

```bash
git clone https://github.com/Mando-369/multi-model-AI-development-assistant.git
cd multi-model-AI-development-assistant
./setup.sh
```

### Manual Installation

#### 1. Clone and Setup Python
```bash
git clone https://github.com/Mando-369/multi-model-AI-development-assistant.git
cd multi-model-AI-development-assistant
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Install Ollama and Models
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
ollama pull deepseek-r1:32b
ollama pull qwen2.5:32b
```

#### 3. Setup faust-mcp (FAUST Integration)
```bash
mkdir -p ../tools
git clone https://github.com/sletz/faust-mcp.git ../tools/faust-mcp
cd ../tools/faust-mcp
git submodule update --init external/node-web-audio-api
```

#### 4. Install Rust and Build WebAudio (for Realtime)
```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"

# Build node-web-audio-api
cd external/node-web-audio-api
npm install
npm run build
```

#### 5. Install Faust Compiler (Optional)
```bash
brew install faust
```

## Usage

### Starting All Services (Recommended)
```bash
cd ..  # Parent directory
./start_assistant.sh
```

### Starting Streamlit Only
```bash
source venv/bin/activate
streamlit run main.py
# Access at http://localhost:8501
# Note: FAUST Analyze/Run buttons won't work without faust-mcp servers
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

### Current (v2.3)
- [x] **FAUST Realtime Audio** - Compile and play FAUST code live via WebAudio
- [x] **Three FAUST Buttons** - Syntax check, Analyze, Run/Stop
- [x] **faust-mcp Integration** - Full integration with faust-mcp server
- [x] **Parameter UI** - Real-time parameter control via faust-ui
- [x] **Unified Launcher** - start_assistant.sh starts all services
- [x] **URL State Persistence** - Browse folder and open file persist across reloads

### Completed (v2.2)
- [x] Dynamic Model Selection - Choose any Ollama model for Reasoning/Fast roles
- [x] Model Setup Tab - UI for model configuration
- [x] Backend Abstraction - Prepared for HuggingFace/Transformers support

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
- [ ] **Embedded Parameter Sliders** - Control FAUST params directly in UI
- [ ] **HuggingFace Backend** - GLM-4.6V and other Transformers models via MPS
- [ ] **IDE Integration** - Cline/Continue.dev integration
- [ ] **Voice input** - Whisper integration for hands-free queries

## Troubleshooting

### Ollama Connection Error
```bash
ollama serve    # Ensure Ollama is running
ollama list     # Check available models
```

### FAUST Servers Not Starting
```bash
# Check if ports are in use
lsof -i:8765 -i:8000 -i:8787

# Check server logs
cat ../tools/faust-mcp/server.log
cat ../tools/faust-mcp/realtime_server.log

# Rebuild node-web-audio-api if needed
cd ../tools/faust-mcp/external/node-web-audio-api
npm run build
```

### Syntax Check Not Working
```bash
# Install Faust compiler
brew install faust

# Verify installation
faust --version
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
