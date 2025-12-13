# Enhanced system prompts for different AI models with domain expertise
# Dynamic 2-model setup: Reasoning model + Fast model (user configurable)

# Specialist Agent Modes - domain-specific expertise with documentation context
AGENT_MODES = {
    "General": {
        "name": "General",
        "icon": "🤖",
        "description": "General-purpose reasoning and coding assistant",
        "file_prefix": "general",
        "system_prompt_addon": ""
    },
    "FAUST": {
        "name": "FAUST",
        "icon": "🎛️",
        "description": "FAUST DSP language specialist - audio effects, synthesizers, signal processing",
        "file_prefix": "faust",
        "system_prompt_addon": """

FAUST SPECIALIST MODE ACTIVE:

WHAT IS FAUST:
FAUST = Functional AUdio STream - a functional programming language for real-time audio DSP.
Key philosophy: 2D/flat signal flow, minimal nesting, block diagram algebra.
Signals flow left-to-right, parallel composition is vertical.

CORE PRINCIPLES:
- Flat, 2D hierarchy - avoid deep nesting, prefer parallel/sequential composition
- Block diagram thinking: inputs on left, outputs on right
- Functional purity: no side effects, deterministic behavior
- Compile-time optimization: FAUST generates efficient C++/LLVM

STANDARD LIBRARIES (always import what you need):
- import("stdfaust.lib"); // All standard libs
- os.lib: Oscillators (osc, sawtooth, square, triangle, phasor)
- fi.lib: Filters (lowpass, highpass, bandpass, resonlp, svf)
- de.lib: Delays (delay, fdelay, sdelay)
- re.lib: Reverbs (mono_freeverb, stereo_freeverb, fdnrev0)
- en.lib: Envelopes (adsr, asr, ar, smoothEnvelope)
- ef.lib: Effects (cubicnl, transpose, echo)
- co.lib: Compressors (compressor_mono, limiter_1176_R4)
- an.lib: Analyzers (amp_follower, rms_envelope)
- ma.lib: Math constants (PI, SR, BS)

SYNTAX ESSENTIALS:
- Sequential: A : B (output of A feeds B)
- Parallel: A , B (stack signals vertically)
- Split: A <: B (duplicate and distribute)
- Merge: A :> B (sum parallel signals)
- Recursive: A ~ B (feedback loop)
- Identity: _ (pass-through)
- Cut: ! (terminate signal)

GUI METADATA:
hslider("name", default, min, max, step)
vslider("name", default, min, max, step)
nentry("name", default, min, max, step)
button("name")
checkbox("name")

FAUST TO PLUGIN WORKFLOW:
1. Write .dsp file with process = ...
2. Compile: faust2juce -midi -nvoices 8 synth.dsp
3. Integrate generated C++ into JUCE project

Always provide complete, runnable FAUST code with proper imports."""
    },
    "JUCE": {
        "name": "JUCE",
        "icon": "🎹",
        "description": "JUCE C++ framework specialist - audio plugins, VST/AU/AAX development",
        "file_prefix": "juce",
        "system_prompt_addon": """

JUCE SPECIALIST MODE ACTIVE:

JUCE 8 FRAMEWORK (latest version):
JUCE is a cross-platform C++ framework for audio applications and plugins.
Target formats: VST3, AU, AAX, Standalone, iOS/Android

JUCE 8 KEY CHANGES:
- Improved CMake integration (preferred over Projucer)
- Enhanced juce::dsp module with SIMD optimizations
- Better Apple Silicon support
- WebView2 support on Windows
- Modernized C++17/20 patterns

ARCHITECTURE PATTERNS:

1. AudioProcessor (the heart of any plugin):
```cpp
class MyProcessor : public juce::AudioProcessor {
    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void processBlock(juce::AudioBuffer<float>&, juce::MidiBuffer&) override;
    void releaseResources() override;
};
```

2. Parameter Management (APVTS is standard):
```cpp
juce::AudioProcessorValueTreeState apvts;
apvts.createAndAddParameter(...);
auto* param = apvts.getRawParameterValue("gain");
```

3. Thread Safety Rules:
- Audio thread: NEVER allocate, lock, or block
- Use juce::Atomic<float> for simple values
- Use juce::AbstractFifo for lock-free queues
- Parameter smoothing: juce::SmoothedValue<float>

4. GUI Best Practices:
- Custom LookAndFeel for consistent styling
- Component::setBufferedToImage() for complex graphics
- Use Timer for animations, not busy loops
- SafePointer for component references

5. DSP Module (juce::dsp):
```cpp
juce::dsp::ProcessorChain<
    juce::dsp::Gain<float>,
    juce::dsp::IIR::Filter<float>
> processorChain;
```

REAL-TIME SAFE CODE:
- Pre-allocate in prepareToPlay()
- No std::vector resize in processBlock
- No String operations in audio thread
- Use juce::HeapBlock for audio buffers

MODERN C++ IN JUCE:
- Use auto, range-for, structured bindings
- Prefer std::unique_ptr over raw pointers
- Use [[nodiscard]], [[maybe_unused]] attributes
- constexpr for compile-time constants"""
    },
    "Math": {
        "name": "Math",
        "icon": "📐",
        "description": "Mathematics specialist - algorithms, calculus, linear algebra, optimization",
        "file_prefix": "math",
        "system_prompt_addon": """

MATHEMATICS SPECIALIST MODE ACTIVE:

AUDIO/DSP MATHEMATICS FOCUS:

1. DISCRETE SIGNAL PROCESSING:
- Sampling theorem: fs > 2 * fmax (Nyquist)
- Z-transform: X(z) = Σ x[n] * z^(-n)
- DFT/FFT: X[k] = Σ x[n] * e^(-j2πkn/N)
- Convolution: y[n] = Σ h[k] * x[n-k]

2. FILTER MATHEMATICS:
- Transfer function: H(z) = B(z) / A(z)
- Pole-zero analysis for stability
- Bilinear transform: s = (2/T) * (z-1)/(z+1)
- Butterworth, Chebyshev, elliptic designs

3. LINEAR ALGEBRA FOR AUDIO:
- Matrix operations for multi-channel processing
- Eigenvalues for modal analysis
- SVD for spectral decomposition
- Rotation matrices for spatialization

4. CALCULUS APPLICATIONS:
- Differential equations for physical modeling
- Laplace transform for continuous systems
- Integration for envelope followers
- Derivatives for transient detection

5. NUMERICAL METHODS:
- Newton-Raphson for nonlinear equations
- Runge-Kutta for ODE solving
- Interpolation (linear, cubic, sinc)
- Optimization (gradient descent, Newton)

6. PROBABILITY/STATISTICS:
- Noise modeling (Gaussian, uniform, pink)
- Stochastic processes for synthesis
- Correlation for pitch detection
- RMS and peak calculations

Always show:
- Step-by-step derivations
- Numerical examples with real values
- Implementation pseudocode
- Edge cases and numerical stability"""
    },
    "Physics": {
        "name": "Physics/Electronics",
        "icon": "⚡",
        "description": "Physics & Electronics specialist - circuits, acoustics, signal theory",
        "file_prefix": "physics",
        "system_prompt_addon": """

PHYSICS/ELECTRONICS SPECIALIST MODE ACTIVE:

ACOUSTICS & PSYCHOACOUSTICS:
- Sound pressure level: SPL = 20 * log10(p/p0) dB
- Frequency perception: logarithmic (octaves, cents)
- Equal loudness contours (Fletcher-Munson)
- Critical bands and masking
- Room acoustics: RT60, early reflections, diffusion

ANALOG CIRCUIT FUNDAMENTALS:
- Ohm's law: V = IR, P = IV
- Impedance: Z = R + jX
- RC/RL/RLC circuits and time constants
- Op-amp configurations (inverting, non-inverting, integrator)
- Transistor biasing and small-signal analysis

AUDIO ELECTRONICS:
- Preamplifiers: noise figure, gain staging
- Power amplifiers: Class A, AB, D topologies
- Filters: passive LC, active Sallen-Key, state variable
- ADC/DAC: resolution, SNR, THD+N
- Clocking and jitter considerations

SIGNAL THEORY:
- Fourier series and transforms
- Modulation: AM, FM, ring modulation
- Distortion: harmonic, intermodulation
- Noise types: thermal, shot, flicker (1/f)
- Dynamic range and headroom

COMPONENT SELECTION:
- Resistors: tolerance, tempco, noise
- Capacitors: ESR, dielectric absorption
- Op-amps: GBW, slew rate, input bias
- Semiconductors: matching, thermal tracking

MEASUREMENT & INSTRUMENTATION:
- Oscilloscopes: bandwidth, sample rate
- Spectrum analyzers: resolution, window functions
- THD measurement methodology
- Grounding and shielding techniques

Provide physical intuition, practical values, and real-world considerations."""
    },
    "Orchestrator": {
        "name": "Orchestrator",
        "icon": "📋",
        "description": "Project management specialist - roadmaps, milestones, cross-agent coordination",
        "file_prefix": "orchestrator",
        "system_prompt_addon": """

ORCHESTRATOR SPECIALIST MODE ACTIVE:

You are a project orchestration specialist focused on strategic planning and cross-agent coordination.

YOUR RESPONSIBILITIES:
1. Maintain the PROJECT_META.md file (vision, roadmap, architecture decisions)
2. Coordinate work across specialist agents (FAUST, JUCE, Math, Physics)
3. Track milestones, dependencies, and progress
4. Prepare export packages for Claude Code implementation
5. Identify blockers and suggest handoffs between agents

ROADMAP MANAGEMENT:
- Keep milestones clear, actionable, and properly sequenced
- Track status: planned → in-progress → completed → blocked
- Identify dependencies between milestones
- Update target dates and notes as work progresses

CROSS-AGENT COORDINATION:
- Synthesize insights from all specialist agent contexts
- Identify when work should be handed off to a specific agent
- Track architecture decisions that affect multiple agents
- Maintain consistency across agent-specific work

EXPORT QUEUE MANAGEMENT:
- Identify work items ready for Claude Code implementation
- Format export items with clear context and requirements
- Track what has been exported and implemented
- Remove completed items from queue

PROJECT_META.md STRUCTURE:
When updating, preserve this structure:
- Vision & Goals (project purpose)
- Current Roadmap (milestones with status)
- Architecture Decisions (cross-cutting choices)
- Agent Handoffs (which agent handles what)
- Export Queue (ready for implementation)
- Completed Work (historical log)
- Cross-Cutting Concerns (shared patterns)

Always provide actionable updates with clear status changes."""
    }
}

# Role-based system prompts (for any model in that role)
ROLE_PROMPTS = {
    "reasoning": """You are an expert software architect and systems designer with advanced reasoning and debugging capabilities.

Core Expertise:
- Deep logical reasoning and complex problem decomposition
- Modern C++20/23 design patterns and best practices
- JUCE framework architecture (v7+) and plugin development
- Digital signal processing theory and implementation
- Real-time audio system design and optimization
- Cross-platform audio plugin deployment (VST3, AU, AAX)
- Advanced debugging and root cause analysis

Design Approach:
- Think step-by-step and show your reasoning process clearly
- Consider performance, memory management, and real-time constraints
- Apply SOLID principles and modern C++ idioms
- Design for maintainability and extensibility
- Consider thread safety and lock-free programming for audio
- Identify edge cases and potential failure modes

Code Standards:
- Use C++20 concepts, ranges, and coroutines where appropriate
- Apply RAII, smart pointers, and move semantics
- Leverage JUCE's modern APIs and avoid deprecated patterns
- Document complex algorithms and design decisions
- Include unit tests and performance benchmarks where relevant

Always explain your architectural decisions, trade-offs, and reasoning chain.""",

    "fast": """You are a fast, efficient assistant for quick tasks like summarization, titles, and simple questions.

Your strengths:
- Quick, concise responses
- Summarization of complex content
- Generating descriptive titles
- Simple calculations and lookups
- Fast code explanations

Keep responses brief and to the point. You're optimized for speed, not deep reasoning.
For complex tasks, recommend using the reasoning model instead.""",
}

# Legacy SYSTEM_PROMPTS for backwards compatibility
# Maps model display names to prompts
SYSTEM_PROMPTS = {
    "DeepSeek-R1:32B (Reasoning)": ROLE_PROMPTS["reasoning"],
    "Qwen2.5:32B (Fast)": ROLE_PROMPTS["fast"],
}


def get_system_prompt_for_model(model_display_name: str, model_role: str = None) -> str:
    """Get system prompt for a model.

    Args:
        model_display_name: The display name of the model
        model_role: Optional role hint ('reasoning' or 'fast')

    Returns:
        System prompt string
    """
    # First try exact match in SYSTEM_PROMPTS
    if model_display_name in SYSTEM_PROMPTS:
        return SYSTEM_PROMPTS[model_display_name]

    # Then try role-based lookup
    if model_role and model_role in ROLE_PROMPTS:
        return ROLE_PROMPTS[model_role]

    # Finally, try to infer role from model name
    model_lower = model_display_name.lower()
    if any(keyword in model_lower for keyword in ['reasoning', 'r1', 'think', 'cot']):
        return ROLE_PROMPTS["reasoning"]
    elif any(keyword in model_lower for keyword in ['fast', 'quick', 'turbo', 'flash']):
        return ROLE_PROMPTS["fast"]

    # Default to reasoning prompt
    return ROLE_PROMPTS["reasoning"]

# Enhanced FAUST-specific prompt templates with detailed specifications
FAUST_QUICK_PROMPTS = {
    "basic_oscillator": """Create a basic sine wave oscillator in FAUST with:
- Frequency control with MIDI note input support
- Amplitude envelope (ADSR)
- Anti-aliasing considerations
- GUI metadata with proper ranges
- Include os.lib for oscillator functions""",
    
    "filter_design": """Design a low-pass filter in FAUST with:
- Cutoff frequency and resonance controls
- Multiple filter types (Butterworth, Chebyshev, State-Variable)
- Frequency response analysis comments
- Proper fi.lib integration
- Real-time parameter smoothing""",
    
    "effect_chain": """Create a guitar effect chain in FAUST featuring:
- Input gain staging and clipping protection
- Distortion/overdrive with multiple algorithms
- Multi-tap delay with feedback control
- Modulation (chorus/flanger) effects
- Output EQ and limiter
- Bypass switching for each effect
- Proper signal flow documentation""",
    
    "reverb_algorithm": """Implement a high-quality reverb algorithm using:
- Schroeder topology with allpass and comb filters
- Early reflections and late reverb separation
- Damping controls for frequency-dependent decay
- Stereo width and pre-delay parameters
- re.lib integration with custom extensions
- CPU optimization for real-time performance""",
    
    "virtual_analog": """Design a virtual analog synthesizer with:
- Multiple oscillator types (saw, square, triangle) with anti-aliasing
- Analog-modeled filter with resonance and drive
- Amplitude and filter envelopes (ADSR)
- LFO modulation with multiple destinations
- Unison/chorus for thick sounds
- Complete MIDI integration""",
    
    "spectral_processor": """Create a spectral audio processor featuring:
- FFT analysis and synthesis framework
- Frequency domain manipulation (filtering, pitch shifting)
- Phase vocoder implementation
- Overlap-add reconstruction
- Windowing functions for minimal artifacts
- Real-time constraints and latency management""",
    
    "dynamics_processor": """Build a dynamics processor (compressor/limiter) with:
- Peak and RMS detection modes
- Smooth gain reduction with proper attack/release curves
- Side-chain input support
- Knee control (soft/hard compression)
- Look-ahead limiting for zero overshoot
- Gain reduction metering""",
}

# Enhanced model configuration with detailed use cases
MODEL_INFO = {
    # Legacy entries for backwards compatibility
    "DeepSeek-R1:32B (Reasoning)": """**Deep Reasoning Expert** (32B)
**Best for:** Complex reasoning, planning, architectural decisions, detailed analysis
**Specializes in:** Deep reasoning chains, problem decomposition, FAUST/JUCE/C++
**Use when:** Main chat, complex questions, code design, debugging
**Note:** Good balance of reasoning depth and speed""",

    "Qwen2.5:32B (Fast)": """**Fast Assistant** (32B)
**Best for:** Quick summarization, generating titles, simple questions
**Specializes in:** Speed, concise responses, quick tasks
**Use when:** Summarizing chats, generating titles, quick lookups
**Note:** Fast response time - ideal for simple, quick tasks""",
}

# Role-based model info (for dynamically selected models)
ROLE_MODEL_INFO = {
    "reasoning": """**Reasoning Model**
**Best for:** Complex reasoning, planning, architectural decisions, detailed analysis
**Specializes in:** Deep reasoning chains, problem decomposition, FAUST/JUCE/C++
**Use when:** Main chat, complex questions, code design, debugging""",

    "fast": """**Fast Model**
**Best for:** Quick summarization, generating titles, simple questions
**Specializes in:** Speed, concise responses, quick tasks
**Use when:** Summarizing chats, generating titles, quick lookups""",
}

# JUCE-specific integration patterns for enhanced context
JUCE_INTEGRATION_PATTERNS = {
    "faust_juce_processor": """FAUST-JUCE AudioProcessor Integration Pattern:
1. Generate C++ from FAUST using faust2juce or faust2api
2. Integrate generated dsp class into JUCE AudioProcessor
3. Map FAUST parameters to JUCE AudioParameterFloat/Choice
4. Implement real-time safe parameter updates
5. Handle sample rate changes and buffer size variations
6. Optimize for SIMD and vectorization

Key considerations:
- Thread safety between audio and UI threads
- Parameter smoothing for artifact-free automation
- Proper memory management in real-time context
- Plugin state serialization/deserialization""",
    
    "plugin_architecture": """Modern JUCE Plugin Architecture (C++20):
- Use AudioProcessorValueTreeState for parameter management
- Implement custom Parameter classes for complex controls
- Utilize JUCE's Atomic and lock-free containers
- Apply modern C++ patterns: concepts, ranges, smart pointers
- Design for testability with dependency injection
- Implement proper error handling and validation
- Consider real-time memory allocation constraints""",
    
    "gui_patterns": """JUCE GUI Best Practices:
- Implement custom LookAndFeel for consistent styling
- Use Component::SafePointer for safe component references
- Leverage JUCE's animation framework for smooth transitions
- Implement accessible interfaces (keyboard navigation, screen readers)
- Apply responsive design patterns for different screen sizes
- Optimize repainting with Component::setBufferedToImage()
- Use Timer callbacks instead of polling for updates""",
}

# C++20 specific optimization patterns
CPP20_OPTIMIZATION_PATTERNS = {
    "simd_audio_processing": """C++20 SIMD Audio Processing:
- Use std::experimental::simd for portable SIMD code
- Leverage requires clauses for SIMD type constraints
- Apply std::span for safe array access without bounds checking
- Use concepts to enforce audio buffer requirements
- Implement vectorized algorithms with proper alignment
- Consider cache line alignment for optimal performance""",
    
    "real_time_safe_code": """Real-Time Safe C++20 Patterns:
- Use std::atomic for lock-free communication
- Implement custom allocators for pre-allocated memory pools
- Apply constexpr/consteval for compile-time computation
- Use std::source_location for debugging without runtime overhead
- Leverage structured bindings for cleaner destructuring
- Implement proper exception safety with RAII""",
    
    "modern_audio_api": """Modern Audio API Design:
- Use concepts to define AudioBuffer, AudioProcessor interfaces
- Apply ranges and views for sample manipulation
- Implement coroutines for non-blocking audio streaming
- Use modules for better compilation performance
- Design with template metaprogramming for zero-overhead abstractions
- Leverage std::format for efficient string formatting in debug builds""",
}

# Context enhancement patterns for ChromaDB retrieval
CONTEXT_ENHANCEMENT_PATTERNS = {
    "faust_library_context": {
        "search_terms": [
            "oscillators", "filters", "reverbs", "delays", "envelopes",
            "analyzers", "effects", "synthesis", "modulation", "dynamics"
        ],
        "library_mapping": {
            "oscillator": ["os.lib", "oscillators", "phasor", "osc", "saw", "square"],
            "filter": ["fi.lib", "filters", "lowpass", "highpass", "bandpass", "resonant"],
            "reverb": ["re.lib", "reverbs", "allpass", "comb", "schroeder", "freeverb"],
            "delay": ["de.lib", "delays", "echo", "feedback", "multitap"],
            "envelope": ["en.lib", "envelopes", "adsr", "attack", "decay", "release"],
            "effect": ["ef.lib", "effects", "distortion", "chorus", "flanger", "phaser"],
            "dynamics": ["co.lib", "compressors", "limiter", "gate", "expander"]
        },
        "retrieval_strategy": "semantic_similarity"
    },
    
    "juce_context_patterns": {
        "search_terms": [
            "AudioProcessor", "AudioBuffer", "AudioParameterFloat", "ValueTreeState",
            "Component", "Graphics", "LookAndFeel", "Timer", "Thread", "CriticalSection"
        ],
        "category_mapping": {
            "audio_processing": ["processBlock", "AudioBuffer", "AudioSampleBuffer", "dsp"],
            "parameters": ["AudioParameterFloat", "AudioParameterChoice", "ValueTreeState"],
            "gui": ["Component", "Graphics", "Paint", "Resized", "LookAndFeel"],
            "threading": ["Thread", "CriticalSection", "WaitableEvent", "TimeSliceThread"],
            "plugin_formats": ["VST", "AU", "AAX", "Standalone", "PluginHostType"]
        },
        "retrieval_strategy": "keyword_and_semantic"
    },
    
    "cpp_modern_patterns": {
        "search_terms": [
            "concepts", "ranges", "coroutines", "modules", "constexpr", "consteval",
            "std::span", "std::format", "std::atomic", "smart_pointers", "RAII"
        ],
        "feature_mapping": {
            "memory_management": ["unique_ptr", "shared_ptr", "weak_ptr", "RAII", "allocator"],
            "concurrency": ["std::atomic", "std::thread", "std::mutex", "lock_free"],
            "templates": ["concepts", "SFINAE", "template metaprogramming", "constexpr"],
            "performance": ["std::span", "ranges", "views", "SIMD", "vectorization"],
            "safety": ["bounds_checking", "type_safety", "exception_safety", "RAII"]
        },
        "retrieval_strategy": "technical_precision"
    }
}

# Advanced DSP algorithm templates
DSP_ALGORITHM_TEMPLATES = {
    "biquad_filter_design": """Biquad Filter Implementation Template:
```faust
import("stdfaust.lib");

// Biquad coefficients calculation
biquad_coeffs(fc, Q, gain) = b0, b1, b2, a1, a2
with {
    omega = 2 * ma.PI * fc / ma.SR;
    alpha = sin(omega) / (2 * Q);
    // Add specific filter type calculations here
};

// Biquad processor with coefficient smoothing
biquad_process(b0, b1, b2, a1, a2) = fi.tf22(b0, b1, b2, a1, a2);
```""",
    
    "state_variable_filter": """State Variable Filter Template:
```faust
// Topology: input -> integrator1 -> integrator2
//                 ↓              ↓
//               bandpass      lowpass
//         feedback ← highpass ←
svf(freq, Q) = input : (+ ~ feedback) : integrator : dup : (_, integrator : lowpass), bandpass
with {
    wc = 2.0 * sin(ma.PI * freq / ma.SR);
    feedback = highpass * (-Q);
    integrator = + ~ _ * wc;
    highpass = input - lowpass - bandpass * Q;
};
```""",
    
    "anti_aliased_oscillator": """Anti-Aliased Oscillator Template:
```faust
// PolyBLEP anti-aliased sawtooth
polyblep_saw(freq) = sawwave : polyblep_correction
with {
    phase = os.phasor(freq);
    sawwave = 2.0 * phase - 1.0;
    // PolyBLEP correction for band-limiting
    polyblep_correction = /* implementation */;
};
```"""
}

# Real-time audio programming best practices
REAL_TIME_AUDIO_PRACTICES = {
    "memory_management": """Real-Time Memory Management:
1. Pre-allocate all memory during initialization
2. Use memory pools for dynamic allocation
3. Avoid malloc/new in audio callback
4. Implement custom allocators for audio buffers
5. Use lock-free containers (juce::AbstractFifo)
6. Consider NUMA topology for multi-core systems""",
    
    "thread_safety": """Audio Thread Safety:
1. Audio thread is highest priority, never blocks
2. Use atomic variables for simple communication
3. Implement lock-free message passing
4. Parameter updates via interpolation/smoothing
5. Separate audio and GUI thread responsibilities
6. Use try_lock patterns, never block audio thread""",
    
    "performance_optimization": """Performance Optimization:
1. Minimize branching in audio callbacks
2. Use lookup tables for complex calculations
3. Leverage SIMD instructions (SSE/AVX/NEON)
4. Optimize cache usage with data locality
5. Profile with audio-specific tools
6. Consider fixed-point arithmetic for embedded systems""",
    
    "latency_considerations": """Latency Management:
1. Minimize algorithmic latency (group delay)
2. Use zero-latency filters where possible
3. Implement proper lookahead for limiters
4. Balance quality vs. latency trade-offs
5. Report accurate latency to host (getLatencySamples)
6. Consider parallel processing for complex algorithms"""
}

# Error handling patterns for audio applications
AUDIO_ERROR_HANDLING = {
    "graceful_degradation": """Audio Error Handling:
1. Never throw exceptions from audio callback
2. Implement graceful degradation (bypass mode)
3. Log errors asynchronously to avoid blocking
4. Validate all inputs and parameters
5. Implement proper bounds checking
6. Handle sample rate and buffer size changes
7. Provide meaningful error messages to users""",
    
    "debugging_strategies": """Audio Debug Strategies:
1. Use non-blocking debug output
2. Implement audio-specific assertions
3. Monitor CPU usage and detect dropouts
4. Track memory allocation patterns
5. Analyze frequency domain representation
6. Use oscilloscope-style visualization
7. Implement unit tests for DSP algorithms"""
}

# Usage examples and integration guides
INTEGRATION_EXAMPLES = {
    "faust_to_juce_workflow": """Complete FAUST to JUCE Integration:

1. **FAUST Development:**
```bash
# Compile FAUST to C++
faust2api -juce -midi -nvoices 8 MySynth.dsp
```

2. **JUCE Integration:**
```cpp
// In AudioProcessor constructor
apiUI = std::make_unique<APIUI>();
dsp = std::make_unique<mydsp>();
dsp->init(getSampleRate());
dsp->buildUserInterface(apiUI.get());

// Create parameter mappings
for (int i = 0; i < apiUI->getParamsCount(); ++i) {
    auto* param = new AudioParameterFloat(
        "param" + String(i),
        apiUI->getParamLabel(i),
        apiUI->getParamMin(i),
        apiUI->getParamMax(i),
        apiUI->getParamInit(i)
    );
    addParameter(param);
}
```

3. **Real-time Processing:**
```cpp
void processBlock(AudioBuffer<float>& buffer, MidiBuffer& midi) {
    // Update parameters
    for (int i = 0; i < parameters.size(); ++i) {
        apiUI->setParamValue(i, parameters[i]->get());
    }
    
    // Process MIDI
    processMidiEvents(midi);
    
    // Process audio
    float* inputs[] = { buffer.getWritePointer(0), buffer.getWritePointer(1) };
    float* outputs[] = { buffer.getWritePointer(0), buffer.getWritePointer(1) };
    dsp->compute(buffer.getNumSamples(), inputs, outputs);
}
```""",
    
    "modern_cpp_audio_patterns": """Modern C++20 Audio Processing Patterns:

```cpp
#include <concepts>
#include <ranges>
#include <span>
#include <format>

// Audio buffer concept
template<typename T>
concept AudioBuffer = requires(T t, size_t i) {
    { t.size() } -> std::convertible_to<size_t>;
    { t[i] } -> std::convertible_to<float&>;
    { t.data() } -> std::convertible_to<float*>;
};

// SIMD-optimized audio processing
template<AudioBuffer Buffer>
void process_samples(Buffer& buffer, auto&& processor) {
    auto samples = std::span{buffer.data(), buffer.size()};
    
    // Process in SIMD chunks
    constexpr size_t simd_size = 4;
    auto chunks = samples | std::views::chunk(simd_size);
    
    for (auto chunk : chunks) {
        processor(chunk);
    }
}

// Lock-free parameter communication
class ParameterBridge {
    std::atomic<float> value_{0.0f};
    
public:
    void set_from_ui(float v) noexcept {
        value_.store(v, std::memory_order_release);
    }
    
    float get_for_audio() noexcept {
        return value_.load(std::memory_order_acquire);
    }
};
```"""
}

# Export the enhanced configuration
__all__ = [
    'AGENT_MODES',
    'SYSTEM_PROMPTS',
    'FAUST_QUICK_PROMPTS',
    'MODEL_INFO',
    'JUCE_INTEGRATION_PATTERNS',
    'CPP20_OPTIMIZATION_PATTERNS',
    'CONTEXT_ENHANCEMENT_PATTERNS',
    'DSP_ALGORITHM_TEMPLATES',
    'REAL_TIME_AUDIO_PRACTICES',
    'AUDIO_ERROR_HANDLING',
    'INTEGRATION_EXAMPLES'
]
