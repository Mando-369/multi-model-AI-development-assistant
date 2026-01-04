# Project: Multi-Model AI Code Assistant
Last Updated: 2026-01-02
Updated By: Claude Code

## Vision & Goals
A local, offline AI reasoning assistant for FAUST/JUCE audio DSP development with real-time audio preview. Combines deep reasoning with specialist agents and live audio playback.

## How To Use

### Starting
```bash
./start_assistant.sh
```
Opens: Streamlit (8501), FAUST Analysis (8765), FAUST Realtime (8000), Parameter UI (8787)

### Workflow
1. **Browse files** - Select folder, open .dsp files in editor
2. **Edit code** - Syntax-highlighted editor with AI suggestions
3. **Test FAUST**:
   - **Syntax** - Quick WASM validation
   - **Analyze** - Full compile + metrics (offline)
   - **Run** - Live audio playback
4. **For effects** - Use Test Input panel (sine/noise/file)
5. **Tweak params** - Open Parameter UI at :8787

### Test Input Options
| Source | Use Case |
|--------|----------|
| none | Generators (oscillators, synths) |
| sine | Test effects at specific frequency |
| noise | Test full spectrum response |
| file | Test with real audio |

#### File Input Modes
- **Local File** (recommended) - Drag & drop audio file, works immediately
- **HTTP URL** - Enter `http://localhost:8080/file.wav`, requires:
  ```bash
  cd /path/to/audio && python -m http.server 8080
  ```

### URL Persistence
- Browse folder saved to `?browse=...`
- Open file saved to `?file=...`
- Survives page reload

## Current Roadmap

| Milestone | Status | Notes |
|-----------|--------|-------|
| FAUST realtime integration | done | Live playback via WebAudio |
| Test input for effects | done | sine/noise/file sources |
| Safety check for effects | done | Warns on no input |
| File input via AudioBuffer | done | Bypasses broken faustwasm fetch |
| URL state persistence | done | Browse folder + open file |
| Embedded param sliders | planned | Control params in Streamlit UI |

## Architecture Decisions

| Decision | Date | Rationale | Status |
|----------|------|-----------|--------|
| Use AudioBufferSourceNode for file input | 2026-01-02 | Node.js fetch doesn't support file:// URLs, faustwasm soundfile broken | active |
| URL as source of truth for state | 2026-01-02 | Session state can be lost, URL persists | active |
| Always show Test Input expander | 2026-01-02 | Preserve file_uploader state across reruns | active |

## Agent Handoffs

- **FAUST**: DSP algorithms, signal processing code
- **JUCE**: Plugin architecture, C++ implementation
- **Math**: Algorithm derivations, filter design
- **Physics**: Circuit modeling, acoustics

## Export Queue (Ready for Claude Code)

- Embedded parameter sliders in Streamlit UI
- HuggingFace backend for GLM-4.6V

## Completed Work

- v2.3: FAUST realtime audio, test inputs, file playback, URL persistence
- v2.2: Dynamic model selection, Model Setup tab
- v2.1: Project Meta system, Orchestrator agent
- v2.0: 2-model architecture, specialist modes
