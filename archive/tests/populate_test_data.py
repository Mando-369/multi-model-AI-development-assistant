#!/usr/bin/env python3
"""
Populate ChromaDB with test data for validation
"""

import sys
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

def create_test_documents():
    """Create sample documents for testing"""
    return [
        Document(
            page_content="""
FAUST Oscillator Library (os.osc)

The os.osc function creates a sinusoidal oscillator:
- Syntax: os.osc(freq)
- freq: frequency in Hz
- Returns: sinusoidal signal between -1 and 1

Example:
process = os.osc(440);

Related functions:
- os.oscsin: sine oscillator
- os.osccos: cosine oscillator
- os.phasor: phasor generator
            """,
            metadata={"type": "faust", "category": "oscillator", "function": "os.osc"}
        ),
        Document(
            page_content="""
FAUST Filter Library (fi.lowpass)

The fi.lowpass function implements a first-order lowpass filter:
- Syntax: fi.lowpass(order, fc)
- order: filter order (1, 2, 3, etc.)
- fc: cutoff frequency in Hz
- Returns: filtered signal

Example:
process = _ : fi.lowpass(1, 1000);

The function uses a butterworth response by default.
            """,
            metadata={"type": "faust", "category": "filter", "function": "fi.lowpass"}
        ),
        Document(
            page_content="""
FAUST State Variable Filter (fi.svf)

The fi.svf implements a state variable filter topology:
- Syntax: fi.svf.lp(freq, Q), fi.svf.hp(freq, Q), fi.svf.bp(freq, Q)
- freq: center frequency
- Q: quality factor (resonance)
- Returns: lowpass, highpass, or bandpass output

Example:
resonantFilter = fi.svf.lp(hslider("freq", 1000, 20, 20000, 1), hslider("Q", 1, 0.1, 10, 0.1));
process = _ : resonantFilter;
            """,
            metadata={"type": "faust", "category": "filter", "function": "fi.svf"}
        ),
        Document(
            page_content="""
FAUST Reverb Library (re.freeverb)

Freeverb implementation in FAUST:
- Syntax: re.mono_freeverb(fb1, fb2, damp, spread)
- fb1, fb2: feedback parameters
- damp: damping factor
- spread: stereo spread

Example:
verb = re.mono_freeverb(0.5, 0.5, 0.5, 1);
process = _ <: _, verb :> _;

For stereo: re.stereo_freeverb
            """,
            metadata={"type": "faust", "category": "reverb", "function": "re.freeverb"}
        ),
        Document(
            page_content="""
JUCE AudioProcessor Class

The AudioProcessor is the base class for audio processing:

class MyProcessor : public AudioProcessor {
public:
    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void processBlock(AudioBuffer<float>& buffer, MidiBuffer& midiMessages) override;
    void releaseResources() override;
    
    // Parameter management
    AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override { return true; }
};

Key methods:
- prepareToPlay(): Initialize processing
- processBlock(): Main audio callback
- releaseResources(): Cleanup
            """,
            metadata={"type": "juce", "category": "processor", "class": "AudioProcessor"}
        ),
        Document(
            page_content="""
JUCE AudioProcessorValueTreeState

Manages plugin parameters with undo/redo support:

AudioProcessorValueTreeState parameters;

// In constructor:
parameters(*this, nullptr, "Parameters", {
    std::make_unique<AudioParameterFloat>("gain", "Gain", 0.0f, 1.0f, 0.5f),
    std::make_unique<AudioParameterFloat>("freq", "Frequency", 20.0f, 20000.0f, 1000.0f)
})

// Access parameters:
float gain = *parameters.getRawParameterValue("gain");
parameters.addParameterListener("gain", this);
            """,
            metadata={"type": "juce", "category": "parameters", "class": "AudioProcessorValueTreeState"}
        ),
        Document(
            page_content="""
JUCE Component and GUI

Base class for all GUI components:

class MyEditor : public AudioProcessorEditor, public Slider::Listener {
private:
    Slider gainSlider;
    Label gainLabel;
    
public:
    MyEditor() {
        addAndMakeVisible(gainSlider);
        addAndMakeVisible(gainLabel);
        
        gainSlider.addListener(this);
        gainSlider.setRange(0.0, 1.0, 0.01);
    }
    
    void sliderValueChanged(Slider* slider) override {
        // Handle slider changes
    }
};
            """,
            metadata={"type": "juce", "category": "gui", "class": "Component"}
        ),
        Document(
            page_content="""
JUCE DSP Module (dsp::IIR::Filter)

High-performance IIR filtering:

dsp::IIR::Filter<float> filter;

// Setup in prepareToPlay:
auto coeffs = dsp::IIR::Coefficients<float>::makeLowPass(sampleRate, 1000.0f);
filter.coefficients = coeffs;

// In processBlock:
dsp::AudioBlock<float> block(buffer);
dsp::ProcessContextReplacing<float> context(block);
filter.process(context);

Available types: makeLowPass, makeHighPass, makeBandPass, makeNotch
            """,
            metadata={"type": "juce", "category": "dsp", "class": "dsp::IIR::Filter"}
        ),
        Document(
            page_content="""
Real-time Audio Programming Best Practices

Key principles for low-latency audio:

1. Avoid memory allocation in audio callbacks
2. Use lock-free data structures
3. Minimize branching in hot paths  
4. Use SIMD when possible
5. Profile and optimize critical sections

Memory management:
- Pre-allocate all buffers
- Use memory pools
- Avoid new/delete in processBlock

Threading:
- Audio thread is high priority
- Use atomic variables for thread communication
- Avoid locks in audio callback
            """,
            metadata={"type": "general", "category": "best_practices", "topic": "real_time_audio"}
        ),
        Document(
            page_content="""
FAUST to JUCE Integration Workflow

Steps to integrate FAUST DSP in JUCE:

1. Compile FAUST to C++:
   faust -a minimal.cpp mydsp.dsp -o mydsp.cpp

2. Include generated files in JUCE project

3. Create wrapper in AudioProcessor:
   class FaustProcessor : public AudioProcessor {
       mydsp faustDSP;
       UI* interface;
   };

4. Initialize in prepareToPlay:
   faustDSP.init(sampleRate);
   faustDSP.buildUserInterface(interface);

5. Process in processBlock:
   faustDSP.compute(numSamples, inputs, outputs);
            """,
            metadata={"type": "integration", "category": "workflow", "topic": "faust_juce"}
        )
    ]

def populate_chromadb():
    """Populate ChromaDB with test documents"""
    print("🚀 Populating ChromaDB with test data...")
    
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    
    # Initialize vectorstore
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    
    # Create test documents
    documents = create_test_documents()
    
    print(f"📚 Adding {len(documents)} test documents...")
    
    # Add documents to vectorstore
    vectorstore.add_documents(documents)
    
    print("✅ Test data population complete!")
    
    # Verify by doing a test search
    test_results = vectorstore.similarity_search("FAUST oscillator", k=3)
    print(f"🔍 Verification: Found {len(test_results)} documents for 'FAUST oscillator'")
    
    for i, doc in enumerate(test_results):
        preview = doc.page_content[:100].replace('\n', ' ').strip()
        print(f"  {i+1}. {preview}...")
    
    return vectorstore

if __name__ == "__main__":
    populate_chromadb()