# Local AI Coding Assistant

## Tech Stack
- **DeepSeek-R1:32B** - Deep reasoning, planning, architecture decisions
- **Qwen2.5:32B** - Fast summarization, titles, quick tasks
- **ChromaDB** - Knowledge base with FAUST/JUCE documentation
- **Streamlit** - Web interface

## Architecture (v2.1)

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

## Key Files
- `main.py` - Streamlit entry point
- `src/core/multi_model_system.py` - Model orchestration & context injection
- `src/core/project_meta_manager.py` - PROJECT_META.md operations
- `src/core/prompts.py` - System prompts & agent modes
- `src/ui/project_meta_ui.py` - Project Meta tab
- `src/ui/ui_components.py` - UI components

## Rules
- Always test before returning
- Use descriptive variable names
- Prefer functional programming patterns
- Keep signal flow flat (FAUST philosophy)
