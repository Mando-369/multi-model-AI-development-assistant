# Project: GRAME FAUST JA Hysteresis Library
Last Updated: 2025-12-13T08:45:13.171575
Updated By: manual

## Vision & Goals
- Implement the Jiles-Atherton (JA) magnetic hysteresis model in FAUST for tape saturation simulation.
- Develop a reusable `jahysteresis.lib` library with configurable physics parameters.

## Current Roadmap

| Milestone | Status | Target | Notes |
|-----------|--------|--------|-------|
| Define project scope | planned | - | Initial requirements gathering and scoping phase |
| Identify idiomatic FAUST patterns for variable iteration counts based on runtime accumulator state. | planned | - | Research and establish best practices for variable iteration counts in FAUST |
| Implement a reusable Jiles-Atherton hysteresis module (`jahysteresis.lib`). | planned | - | Develop reusable Jiles-Atherton hysteresis module |

## Architecture Decisions

| Decision | Date | Rationale | Status |
|----------|------|-----------|--------|
| Use FAUST for DSP implementation | - | Leverages FAUST's strengths in real-time audio processing | active |
| Implement C++ wrapper using JUCE framework | - | Provides cross-platform plugin deployment capabilities | planned |

## Agent Handoffs

- **FAUST**:  
  - Develop core JA hysteresis model implementation  
  - Optimize for CPU load with LUT trade-offs  

- **JUCE**:  
  - Design plugin architecture for real-time audio processing  
  - Implement C++ wrapper around FAUST-generated code  

- **Math**:  
  - Derive and validate Jiles-Atherton model equations  
  - Establish parameter mappings for physical realism  

- **Physics**:  
  - Model magnetic tape saturation behavior  
  - Translate physical characteristics into DSP parameters  

## Export Queue (Ready for Claude Code)

| Item | Description | Dependencies |
|------|-------------|--------------|
| JA Hysteresis Core Implementation | FAUST implementation of Jiles-Atherton model | - |
| Reusable jahysteresis.lib Library | Optimized FAUST library with configurable parameters | JA Hysteresis Core |

## Completed Work
- None yet

## Cross-Cutting Concerns

- **Variable iteration pattern**: Address difference between C++ fractional substep accumulation and FAUST's fixed unrolled chains
- **CPU load optimization**: Balance between LUT trade-offs and fixed bias parameter handling
- **Phase continuity**: Ensure consistent behavior across variable iteration counts