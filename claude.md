# Local AI Coding Assistant

## Tech Stack
- **Ollama** - Local model backend (configurable models via Model Setup tab)
- **Reasoning Model** - Deep reasoning, planning, architecture (default: deepseek-r1:32b)
- **Fast Model** - Summarization, titles, quick tasks (default: qwen2.5:32b)
- **ChromaDB** - Knowledge base with FAUST/JUCE documentation
- **Streamlit** - Web interface
- **faust-mcp** - FAUST analysis (:8765) and realtime audio (:8000)
- **node-web-audio-api** - WebAudio backend for realtime playback

## Architecture (v2.3)

### Project Meta System
Strategic planning with PROJECT_META.md per project:
- Vision & Goals
- Roadmap with milestones
- Architecture decisions
- Export queue for Claude Code

### Specialist Agent Modes
| Mode | Focus |
|------|-------|
| Orchestrator | Project management, roadmaps, cross-agent coordination |
| General | General-purpose reasoning |
| FAUST | DSP language, signal flow, block diagrams |
| JUCE | C++ audio framework, VST/AU plugins |
| Math | DSP algorithms, filter design |
| Physics | Circuits, acoustics, electronics |

### Context Hierarchy
All agents see: `Agent Prompt → PROJECT_META.md → Agent Meta → Last Exchange → Question`

### Hybrid Workflow
1. Define vision & roadmap in **Project Meta** tab
2. Work with specialist agents in **AI Chat**
3. Sync progress back using **Orchestrator**
4. Export items to **Claude Code** for implementation

## FAUST Integration

### Buttons
| Button | Function | Server |
|--------|----------|--------|
| ✓ Syntax | WASM validation | :8000 realtime (fallback: local CLI) |
| 🎛️ Analyze | Compile + metrics | :8765 analysis |
| ▶️ Run | Live playback | :8000 realtime |

### Test Input (for Effects)
Effects (DSPs with inputs) need test signals. Options:
- **none** - No input (for generators like oscillators)
- **sine** - Configurable frequency sine wave
- **noise** - White noise
- **file** - Audio file (local or HTTP URL)

File input modes:
- **Local File** (recommended) - Drag & drop, works immediately
- **HTTP URL** - For remote files, requires `python -m http.server 8080` in audio folder

Safety check warns when running effects with "none" selected.

### Key Files
- `src/core/faust_mcp_client.py` - Analysis server client
- `src/core/faust_realtime_client.py` - Realtime server client
- `src/ui/editor_ui.py` - Editor with FAUST buttons & test input UI

## Key Files
- `main.py` - Streamlit entry point
- `model_config.json` - Model role configuration (Reasoning/Fast)
- `src/core/multi_model_system.py` - Model orchestration & context injection
- `src/core/model_backends.py` - Backend abstraction (Ollama, HuggingFace stub)
- `src/core/model_config.py` - Model configuration manager
- `src/core/project_meta_manager.py` - PROJECT_META.md operations
- `src/core/prompts.py` - System prompts & agent modes
- `src/ui/model_setup_ui.py` - Model Setup tab
- `src/ui/project_meta_ui.py` - Project Meta tab
- `src/ui/ui_components.py` - UI components
- `src/ui/editor_ui.py` - Code editor with FAUST integration
- `src/ui/file_browser.py` - File browser with URL persistence

## Rules
- Always test before returning
- Use descriptive variable names
- Prefer functional programming patterns
- Keep signal flow flat (FAUST philosophy)
