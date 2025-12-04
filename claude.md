# Local AI Coding Assistant

## Tech Stack
- **DeepSeek-R1:70B** - Deep reasoning, planning, architecture decisions
- **Qwen2.5:32B** - Fast summarization, titles, quick tasks
- **ChromaDB** - Knowledge base with FAUST/JUCE documentation
- **Streamlit** - Web interface

## Architecture (v2.0)

### Simplified 2-Model System
Removed HRM (Hierarchical Reasoning Model) integration - it was designed for puzzle-solving (Sudoku, mazes), not code understanding. The "intelligent routing" was just regex pattern matching.

**New approach**: Direct model selection with specialist agent modes.

### Specialist Agent Modes
| Mode | Focus |
|------|-------|
| General | General-purpose reasoning |
| FAUST | DSP language, signal flow, block diagrams |
| JUCE | C++ audio framework, VST/AU plugins |
| Math | DSP algorithms, filter design |
| Physics | Circuits, acoustics, electronics |

### Hybrid Workflow
This is a **local, offline assistant** for deep reasoning. Use it alongside:
- Claude Code
- GitHub Codex
- Cursor
- Any implementation tool

**Workflow**: DeepSeek reasons locally → Export results → Implement with your preferred tool.

## Key Files
- `main.py` - Streamlit entry point
- `src/core/multi_model_system.py` - Model orchestration
- `src/core/prompts.py` - System prompts & agent modes
- `src/ui/ui_components.py` - UI components
- `src/ui/editor_ui.py` - Code editor

## Future Roadmap
- IDE integration (Cline/Continue.dev) when model chaining is supported
- MCP server for ChromaDB knowledge base
- Voice input with Whisper

## Rules
- Always test before returning
- Use descriptive variable names
- Prefer functional programming patterns
- Keep signal flow flat (FAUST philosophy)
