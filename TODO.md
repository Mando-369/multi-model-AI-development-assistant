# Local AI Coding Assistant - Status

## Completed (v2.0)

### Architecture Changes
- [x] Removed HRM (was for puzzles, not code understanding)
- [x] Simplified to 2-model system (DeepSeek + Qwen)
- [x] Removed "intelligent routing" - direct model selection

### Export & Summarization
- [x] Copy Response button
- [x] Save to Project button (with agent mode prefix in filename)
- [x] Format for Claude button
- [x] Generate Title (uses Qwen)
- [x] Quick Summary (uses Qwen)

### Specialist Agent Modes
- [x] General mode
- [x] FAUST mode (with documentation)
- [x] JUCE mode (JUCE 8 best practices)
- [x] Math mode (DSP algorithms)
- [x] Physics mode (electronics/circuits)

### UI Improvements
- [x] Persistent tab navigation (radio buttons + session state)
- [x] File browser visual separation (bordered containers)
- [x] AI assistant text area height (350px)

### Documentation
- [x] Updated README.md
- [x] Updated CLAUDE.md
- [x] Updated TODO.md
- [x] Updated SETUP_GUIDE.md

---

## Completed (v2.1) - Project Meta Feature

### Project Meta System
- [x] Orchestrator agent mode (project management specialist)
- [x] PROJECT_META.md per project (vision, roadmap, decisions)
- [x] Project Meta tab with viewer/editor (first tab position)
- [x] Orchestrator chat interface in Project Meta tab
- [x] Inject PROJECT_META.md into all agent contexts
- [x] Sync from Agents feature (merge/replace options)
- [x] Quick action buttons (Generate Summary, Export to Claude)

### Context Hierarchy (All Agents)
```
Agent System Prompt → PROJECT_META.md → Agent Meta → Last Exchange → Question
```

### Files Created/Modified
- `src/core/project_meta_manager.py` (new)
- `src/ui/project_meta_ui.py` (new)
- `src/core/prompts.py` (added Orchestrator)
- `src/core/multi_model_system.py` (context injection)
- `main.py` (Project Meta as first tab)

---

## Current Model Configuration

| Model | Purpose |
|-------|---------|
| DeepSeek-R1:32B | Reasoning, planning, architecture |
| Qwen2.5:32B | Summarization, titles, fast tasks |

---

## In Progress (v2.2) - Dynamic Model Selection

### Phase 1: Ollama Dynamic Selection
- [ ] Model backend abstraction (`src/core/model_backends.py`)
- [ ] Model configuration manager (`src/core/model_config.py`)
- [ ] Ollama backend with `ollama list` discovery
- [ ] Model Setup tab (6th tab)
- [ ] User-assignable "Reasoning" and "Fast" model roles
- [ ] Config persistence in `model_config.json`
- [ ] Update all files referencing hardcoded models

### Phase 2: HuggingFace Backend (Future)
- [ ] HuggingFace Transformers backend
- [ ] MPS acceleration for Apple Silicon
- [ ] GLM-4.6V-Flash support (vision + text)
- [ ] Image input in chat UI

### Architecture

```
┌─────────────────────────────────────────────┐
│           Model Configuration Tab           │
├─────────────────────────────────────────────┤
│  Backend: [Ollama ▼]                        │
│                                             │
│  Reasoning Model: [scan & select ▼]         │
│  Fast Model:      [scan & select ▼]         │
│                                             │
│  [Scan Available] [Test Connection] [Save]  │
└─────────────────────────────────────────────┘
```

**Backend Abstraction:**
```python
class ModelBackend(ABC):
    def list_models(self) -> List[str]
    def generate(self, prompt: str, model_id: str) -> str
    def check_availability(self, model_id: str) -> bool

class OllamaBackend(ModelBackend): ...
class HuggingFaceBackend(ModelBackend): ...  # Phase 2
```

**Files to Update:**
- `src/core/multi_model_system.py` - use config instead of hardcoded
- `src/ui/ui_components.py` - model dropdown from config
- `src/ui/project_meta_ui.py` - model references
- `src/ui/system_monitor.py` - model status display
- `main.py` - add Model Setup tab

---

## Future Roadmap

### IDE Integration (Waiting)
- [ ] Cline/Continue.dev integration when model chaining is supported
- [ ] Automatic DeepSeek → Claude handoff

### Optional Enhancements
- [ ] MCP server for ChromaDB knowledge base
- [ ] Voice input with Whisper
- [ ] WebAssembly FAUST in-browser testing

---

## Hybrid Workflow

```
Streamlit (Local)              Your Coding Tool
┌────────────────────┐         ┌─────────────────────┐
│ DeepSeek-R1:32B    │  Copy   │ Claude Code         │
│ └─ Reasoning       │ ──────► │ Cursor              │
│                    │  Save   │ Codex               │
│ Qwen2.5:32B        │         │ Any IDE             │
│ └─ Summarize       │         │                     │
└────────────────────┘         └─────────────────────┘
```

**Rule**: DeepSeek for thinking, Qwen for summarizing, external tool for implementing.

---

*Updated: December 2024 - v2.1*
