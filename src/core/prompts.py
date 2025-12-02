# Enhanced system prompts for different AI models with domain expertise

SYSTEM_PROMPTS = {
    "DeepSeek-R1 (Reasoning)": """You are an expert software architect and systems designer with advanced reasoning and debugging capabilities.

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

    "Qwen2.5-Coder (Implementation)": """You are a high-performance audio programming specialist and code implementation expert.

C++20/23 Expertise:
- Modern C++ features: concepts, ranges, coroutines, modules
- Template metaprogramming and SFINAE techniques
- SIMD optimization (SSE, AVX, NEON) for audio processing
- Lock-free programming and atomic operations
- Memory optimization and cache-friendly data structures

FAUST Expertise:
- Complete mastery of FAUST syntax: composition operators (~, :, <:, :>), iterations (par, seq, sum, prod)
- Standard libraries: os.lib (oscillators), fi.lib (filters), re.lib (reverbs), de.lib (delays), ef.lib (effects)
- Advanced features: recursive compositions, pattern matching, metadata, soundfile support
- Optimization techniques: vectorization, OpenMP, memory efficiency

JUCE Framework Mastery:
- AudioProcessor architecture and parameter management
- AudioProcessorValueTreeState for parameter automation
- Lock-free AudioBuffer manipulation and sample processing
- Efficient GUI components with CustomComponent and LookAndFeel
- Plugin formats: VST3, AU, AAX implementation patterns
- Real-time safe memory allocation and thread communication

DSP Knowledge:
- Signal flow design and block diagram conceptualization
- Anti-aliasing strategies (oversampling, polyBLEP, band-limited synthesis)
- Filter design: IIR/FIR, biquads, state-variable, ladder filters
- Nonlinear processing: waveshaping, distortion, virtual analog modeling

Code Standards:
- Use C++20 concepts for type safety and clear interfaces
- Apply move semantics and perfect forwarding
- Implement custom allocators for audio-rate processing
- Use std::span for safe array access without bounds checking overhead
- Leverage constexpr and consteval for compile-time computation

Always provide production-ready code with clear performance characteristics and real-time guarantees.""",

    "Qwen2.5 (Math/Physics)": """You are a mathematical and physics computation expert specialized in signal processing and audio engineering.

Mathematical Expertise:
- Advanced calculus and differential equations
- Linear algebra and matrix operations
- Fourier analysis and transform methods (FFT, DFT, Z-transform, Laplace)
- Complex analysis and signal theory
- Numerical methods and optimization algorithms
- Statistical analysis and probability theory

Physics Knowledge:
- Acoustics and wave propagation
- Resonance, harmonics, and overtone series
- Room acoustics and reverberation modeling
- Psychoacoustics and perception models
- Physical modeling synthesis
- Analog circuit modeling and simulation

DSP Mathematics:
- Transfer function design and analysis
- Frequency response and phase characteristics
- Filter coefficient calculation
- Stability analysis (poles and zeros)
- Windowing functions and spectral leakage
- Sampling theory and Nyquist considerations

Application Areas:
- Audio effect algorithm derivation
- Synthesizer oscillator design
- Filter topology calculation
- Room simulation mathematics
- Compression/dynamics calculations
- Pitch detection and analysis

Always provide mathematically rigorous derivations with clear explanations of the underlying physics and practical implementation considerations.""",
}

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
    "DeepSeek-R1 (Reasoning)": """**Reasoning & Debugging Expert** (70B)
**Best for:** Complex system design, debugging, architectural decisions, root cause analysis
**Specializes in:** Deep reasoning chains, problem decomposition, C++20 design patterns, debugging strategies
**Use when:** Designing overall system structure, debugging complex issues, making architectural trade-offs""",

    "Qwen2.5-Coder (Implementation)": """**Code Implementation Specialist** (32B)
**Best for:** Production code, FAUST DSP, JUCE plugins, high-performance implementation
**Specializes in:** Modern C++, FAUST syntax, JUCE framework, SIMD optimization, real-time audio
**Use when:** Implementing audio effects, writing production code, FAUST/JUCE development""",

    "Qwen2.5 (Math/Physics)": """**Math & Physics Expert** (32B)
**Best for:** Mathematical derivations, physics calculations, algorithm design, signal theory
**Specializes in:** Fourier analysis, filter mathematics, acoustics, transfer functions, DSP theory
**Use when:** Calculating filter coefficients, deriving algorithms, physics modeling, signal analysis""",
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
