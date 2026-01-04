"""
Context Enhancement Module for FAUST/JUCE Development
Provides intelligent ChromaDB retrieval with domain-specific search strategies
"""

import re
from typing import Any, List, Dict, Set, Tuple, Optional
from langchain_chroma import Chroma
from .prompts import CONTEXT_ENHANCEMENT_PATTERNS, DSP_ALGORITHM_TEMPLATES


class ContextEnhancer:
    """Enhanced context retrieval for FAUST/JUCE development"""
    
    def __init__(self, vectorstore: Chroma):
        self.vectorstore = vectorstore
        self.patterns = CONTEXT_ENHANCEMENT_PATTERNS
        self.templates = DSP_ALGORITHM_TEMPLATES
        
        # FAUST library function registry
        self.faust_functions = self._build_faust_function_registry()
        
        # JUCE class hierarchy mapping
        self.juce_hierarchy = self._build_juce_hierarchy()
        
    def _build_faust_function_registry(self) -> Dict[str, List[str]]:
        """Build registry of FAUST library functions"""
        return {
            "oscillators": [
                "os.osc", "os.oscsin", "os.osccos", "os.phasor", "os.saw", "os.square",
                "os.triangle", "os.sawtooth", "os.lf_saw", "os.lf_triangle", "os.lf_square",
                "os.impulse", "os.sawN", "os.squareN", "os.triangleN"
            ],
            "filters": [
                "fi.lowpass", "fi.highpass", "fi.bandpass", "fi.notch", "fi.peak",
                "fi.tf2", "fi.tf22", "fi.biquad", "fi.resonlp", "fi.resonhp",
                "fi.svf", "fi.ladder", "fi.moog_vcf", "fi.dcblocker", "fi.pole", "fi.zero"
            ],
            "reverbs": [
                "re.mono_freeverb", "re.stereo_freeverb", "re.jcrev", "re.satrev",
                "re.fdnrev0", "re.zita_rev1", "re.greyhole", "re.jpverb"
            ],
            "delays": [
                "de.delay", "de.fdelay", "de.sdelay", "de.fdelaylti", "de.fdelayltv",
                "de.multitap", "de.echo", "de.pingpong", "de.tapiir"
            ],
            "envelopes": [
                "en.adsr", "en.asr", "en.ar", "en.ahd", "en.adshr", 
                "en.smoothEnvelope", "en.exponentialDecay"
            ],
            "effects": [
                "ef.chorus", "ef.flanger", "ef.phaser", "ef.tremolo", "ef.vibrato",
                "ef.autopan", "ef.gate", "ef.compressor", "ef.limiter", "ef.dryWetMix"
            ],
            "dynamics": [
                "co.compressor_mono", "co.compressor_stereo", "co.limiter_1176",
                "co.peak_compression_gain_mono", "co.rms_compression_gain_mono"
            ]
        }
    
    def _build_juce_hierarchy(self) -> Dict[str, List[str]]:
        """Build JUCE class hierarchy for better context retrieval"""
        return {
            "audio_processing": [
                "AudioProcessor", "AudioProcessorGraph", "AudioProcessorPlayer",
                "AudioBuffer", "AudioSampleBuffer", "MidiBuffer", "MidiMessage"
            ],
            "parameters": [
                "AudioParameterFloat", "AudioParameterInt", "AudioParameterBool",
                "AudioParameterChoice", "AudioProcessorValueTreeState", "Parameter"
            ],
            "gui_components": [
                "Component", "Button", "Slider", "Label", "ComboBox", "TextEditor",
                "CustomComponent", "LookAndFeel", "Graphics", "Timer"
            ],
            "dsp_modules": [
                "dsp::ProcessorBase", "dsp::IIR::Filter", "dsp::FIR::Filter",
                "dsp::Oscillator", "dsp::DelayLine", "dsp::Reverb", "dsp::Compressor"
            ],
            "threading": [
                "Thread", "CriticalSection", "SpinLock", "WaitableEvent",
                "TimeSliceThread", "ThreadPool", "AsyncUpdater"
            ],
            "memory": [
                "MemoryBlock", "HeapBlock", "AudioBlock", "ProcessContext",
                "MemoryInputStream", "MemoryOutputStream"
            ]
        }
    
    def enhance_context_for_query(self, 
                                 query: str, 
                                 task_type: str = "general",
                                 max_docs: int = 8) -> Dict[str, Any]:
        """
        Enhance context retrieval based on query analysis and task type
        
        Args:
            query: User query to analyze
            task_type: Type of task (faust, juce, cpp, general)
            max_docs: Maximum number of documents to retrieve
            
        Returns:
            Enhanced context dictionary with documents and metadata
        """
        context = {
            "documents": [],
            "search_terms": [],
            "function_references": [],
            "algorithm_templates": [],
            "best_practices": [],
            "integration_patterns": []
        }
        
        # Analyze query for domain-specific patterns
        query_analysis = self._analyze_query(query, task_type)
        context.update(query_analysis)
        
        # Retrieve relevant documents using multiple strategies
        if task_type == "faust":
            context["documents"] = self._retrieve_faust_context(query, max_docs)
            context["function_references"] = self._extract_faust_functions(query)
            context["algorithm_templates"] = self._get_relevant_templates(query)
        elif task_type == "juce":
            context["documents"] = self._retrieve_juce_context(query, max_docs)
            context["function_references"] = self._extract_juce_classes(query)
        else:
            context["documents"] = self._retrieve_general_context(query, max_docs)
        
        # Add integration patterns if multiple domains detected
        if self._is_multi_domain_query(query):
            context["integration_patterns"] = self._get_integration_patterns(query)
        
        return context
    
    def _analyze_query(self, query: str, task_type: str) -> Dict[str, Any]:
        """Analyze query for domain-specific patterns"""
        query_lower = query.lower()
        
        analysis = {
            "complexity": self._estimate_complexity(query),
            "domain_keywords": [],
            "technical_terms": [],
            "library_references": []
        }
        
        # Extract domain-specific keywords
        if task_type == "faust" or "faust" in query_lower:
            analysis["domain_keywords"] = self._extract_faust_keywords(query)
            analysis["library_references"] = self._extract_library_references(query)
        elif task_type == "juce" or "juce" in query_lower:
            analysis["domain_keywords"] = self._extract_juce_keywords(query)
        
        # Extract technical terms
        analysis["technical_terms"] = self._extract_technical_terms(query)
        
        return analysis
    
    def _extract_faust_keywords(self, query: str) -> List[str]:
        """Extract FAUST-specific keywords from query"""
        faust_keywords = []
        query_lower = query.lower()
        
        # DSP algorithm keywords
        dsp_terms = [
            "oscillator", "filter", "reverb", "delay", "echo", "chorus", "flanger",
            "compressor", "limiter", "distortion", "envelope", "adsr", "lfo",
            "synthesis", "frequency", "amplitude", "resonance", "cutoff", "feedback"
        ]
        
        for term in dsp_terms:
            if term in query_lower:
                faust_keywords.append(term)
        
        # FAUST-specific syntax
        syntax_patterns = [
            r"process\s*=", r"import\([\"']", r"with\s*{", r"library\(", 
            r"~", r":", r"<:", r":>", r"\|", r",", r"\+"
        ]
        
        for pattern in syntax_patterns:
            if re.search(pattern, query):
                faust_keywords.append("faust_syntax")
                break
        
        return faust_keywords
    
    def _extract_juce_keywords(self, query: str) -> List[str]:
        """Extract JUCE-specific keywords from query"""
        juce_keywords = []
        query_lower = query.lower()
        
        # JUCE class names
        for category, classes in self.juce_hierarchy.items():
            for class_name in classes:
                if class_name.lower() in query_lower:
                    juce_keywords.append(class_name)
        
        # Plugin-specific terms
        plugin_terms = ["vst", "au", "aax", "plugin", "processor", "component"]
        for term in plugin_terms:
            if term in query_lower:
                juce_keywords.append(term)
        
        return juce_keywords
    
    def _extract_library_references(self, query: str) -> List[str]:
        """Extract FAUST library function references"""
        references = []
        
        # Look for library prefixes
        lib_patterns = [
            r"os\.", r"fi\.", r"re\.", r"de\.", r"en\.", r"ef\.", r"co\.",
            r"ma\.", r"ba\.", r"no\.", r"sy\.", r"ve\."
        ]
        
        for pattern in lib_patterns:
            matches = re.findall(pattern, query)
            references.extend(matches)
        
        # Look for specific function names
        for category, functions in self.faust_functions.items():
            for func in functions:
                if func in query:
                    references.append(func)
        
        return list(set(references))  # Remove duplicates
    
    def _extract_technical_terms(self, query: str) -> List[str]:
        """Extract general technical terms"""
        technical_terms = []
        query_lower = query.lower()
        
        # Audio processing terms
        audio_terms = [
            "sample rate", "buffer size", "latency", "real-time", "dsp",
            "signal processing", "frequency domain", "time domain", "fft",
            "convolution", "filtering", "modulation", "synthesis", "analysis"
        ]
        
        for term in audio_terms:
            if term in query_lower:
                technical_terms.append(term)
        
        # Programming terms
        prog_terms = [
            "class", "function", "method", "template", "algorithm", "optimization",
            "performance", "memory", "threading", "concurrency", "simd"
        ]
        
        for term in prog_terms:
            if term in query_lower:
                technical_terms.append(term)
        
        return technical_terms
    
    def _estimate_complexity(self, query: str) -> int:
        """Estimate query complexity on 1-10 scale"""
        complexity = 1
        query_lower = query.lower()
        
        complexity_indicators = {
            r'simple|basic|quick|easy': 2,
            r'example|demo|tutorial': 3,
            r'implement|create|build': 5,
            r'complex|advanced|sophisticated': 7,
            r'complete|full|entire|comprehensive': 8,
            r'system|framework|architecture|engine': 9,
            r'from scratch|ground up|production|enterprise': 10
        }
        
        for pattern, score in complexity_indicators.items():
            if re.search(pattern, query_lower):
                complexity = max(complexity, score)
        
        return min(10, complexity)
    
    def _retrieve_faust_context(self, query: str, max_docs: int) -> List:
        """Retrieve FAUST-specific context documents"""
        # Build enhanced search query
        search_terms = []
        
        # Add original query
        search_terms.append(query)
        
        # Add FAUST-specific terms
        faust_terms = ["faust", "dsp", "signal processing", "audio effect"]
        search_terms.extend(faust_terms)
        
        # Retrieve documents using semantic similarity
        all_docs = []
        for term in search_terms:
            try:
                docs = self.vectorstore.similarity_search(term, k=max_docs//len(search_terms)+1)
                all_docs.extend(docs)
            except Exception as e:
                print(f"Context retrieval error for '{term}': {e}")
        
        # Remove duplicates and limit results
        seen_content = set()
        unique_docs = []
        for doc in all_docs:
            if doc.page_content not in seen_content:
                seen_content.add(doc.page_content)
                unique_docs.append(doc)
                if len(unique_docs) >= max_docs:
                    break
        
        return unique_docs
    
    def _retrieve_juce_context(self, query: str, max_docs: int) -> List:
        """Retrieve JUCE-specific context documents"""
        # Build JUCE-focused search
        search_terms = [query, "juce", "audio processor", "plugin development"]
        
        all_docs = []
        for term in search_terms:
            try:
                docs = self.vectorstore.similarity_search(term, k=max_docs//len(search_terms)+1)
                all_docs.extend(docs)
            except Exception as e:
                print(f"JUCE context retrieval error for '{term}': {e}")
        
        # Remove duplicates
        seen_content = set()
        unique_docs = []
        for doc in all_docs:
            if doc.page_content not in seen_content:
                seen_content.add(doc.page_content)
                unique_docs.append(doc)
                if len(unique_docs) >= max_docs:
                    break
        
        return unique_docs
    
    def _retrieve_general_context(self, query: str, max_docs: int) -> List:
        """Retrieve general programming context"""
        try:
            return self.vectorstore.similarity_search(query, k=max_docs)
        except Exception as e:
            print(f"General context retrieval error: {e}")
            return []
    
    def _extract_faust_functions(self, query: str) -> List[str]:
        """Extract FAUST function references from query"""
        functions = []
        
        for category, func_list in self.faust_functions.items():
            for func in func_list:
                if func in query:
                    functions.append(func)
        
        return functions
    
    def _extract_juce_classes(self, query: str) -> List[str]:
        """Extract JUCE class references from query"""
        classes = []
        query_lower = query.lower()
        
        for category, class_list in self.juce_hierarchy.items():
            for class_name in class_list:
                if class_name.lower() in query_lower:
                    classes.append(class_name)
        
        return classes
    
    def _get_relevant_templates(self, query: str) -> List[str]:
        """Get relevant DSP algorithm templates"""
        templates = []
        query_lower = query.lower()
        
        template_keywords = {
            "biquad_filter_design": ["biquad", "filter", "iir", "frequency response"],
            "state_variable_filter": ["svf", "state variable", "filter", "topology"],
            "anti_aliased_oscillator": ["oscillator", "anti-alias", "polyblep", "bandlimited"]
        }
        
        for template_name, keywords in template_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                if template_name in self.templates:
                    templates.append(self.templates[template_name])
        
        return templates
    
    def _is_multi_domain_query(self, query: str) -> bool:
        """Check if query involves multiple domains (FAUST + JUCE)"""
        query_lower = query.lower()
        has_faust = any(term in query_lower for term in ["faust", "dsp", "signal"])
        has_juce = any(term in query_lower for term in ["juce", "plugin", "vst", "au"])
        return has_faust and has_juce
    
    def _get_integration_patterns(self, query: str) -> List[str]:
        """Get relevant integration patterns"""
        from prompts import JUCE_INTEGRATION_PATTERNS, INTEGRATION_EXAMPLES
        
        patterns = []
        query_lower = query.lower()
        
        if "faust" in query_lower and "juce" in query_lower:
            patterns.append(JUCE_INTEGRATION_PATTERNS["faust_juce_processor"])
            patterns.append(INTEGRATION_EXAMPLES["faust_to_juce_workflow"])
        
        if "plugin" in query_lower:
            patterns.append(JUCE_INTEGRATION_PATTERNS["plugin_architecture"])
        
        if "gui" in query_lower or "interface" in query_lower:
            patterns.append(JUCE_INTEGRATION_PATTERNS["gui_patterns"])
        
        return patterns
    
    def get_context_summary(self, context: Dict) -> str:
        """Generate a summary of the retrieved context"""
        summary_parts = []
        
        if context["documents"]:
            summary_parts.append(f"📚 Retrieved {len(context['documents'])} relevant documents")
        
        if context["function_references"]:
            summary_parts.append(f"🔧 Found {len(context['function_references'])} function references")
        
        if context["algorithm_templates"]:
            summary_parts.append(f"📐 Included {len(context['algorithm_templates'])} algorithm templates")
        
        if context["integration_patterns"]:
            summary_parts.append(f"🔗 Added {len(context['integration_patterns'])} integration patterns")
        
        return " | ".join(summary_parts) if summary_parts else "📋 Basic context retrieved"


# Integration with MultiModelGLMSystem
def enhance_vectorstore_retrieval(vectorstore: Chroma, 
                                 query: str, 
                                 task_type: str = "general") -> str:
    """
    Enhanced vectorstore retrieval function for use in MultiModelGLMSystem
    
    Args:
        vectorstore: ChromaDB vectorstore instance
        query: User query
        task_type: Type of task (faust, juce, general)
    
    Returns:
        Enhanced context string
    """
    enhancer = ContextEnhancer(vectorstore)
    context = enhancer.enhance_context_for_query(query, task_type)
    
    # Build enhanced context string
    context_parts = []
    
    # Add document content
    if context["documents"]:
        doc_content = "\\n\\n".join([doc.page_content[:500] for doc in context["documents"][:3]])
        context_parts.append(f"=== RELEVANT DOCUMENTATION ===\\n{doc_content}")
    
    # Add function references
    if context["function_references"]:
        functions = ", ".join(context["function_references"][:10])
        context_parts.append(f"=== RELEVANT FUNCTIONS ===\\n{functions}")
    
    # Add algorithm templates
    if context["algorithm_templates"]:
        templates = "\\n\\n".join(context["algorithm_templates"][:2])
        context_parts.append(f"=== ALGORITHM TEMPLATES ===\\n{templates}")
    
    # Add integration patterns
    if context["integration_patterns"]:
        patterns = "\\n\\n".join(context["integration_patterns"][:1])
        context_parts.append(f"=== INTEGRATION PATTERNS ===\\n{patterns}")
    
    enhanced_context = "\\n\\n".join(context_parts) if context_parts else ""
    
    # Log context enhancement
    summary = enhancer.get_context_summary(context)
    print(f"🔍 Context Enhancement: {summary}")
    
    return enhanced_context


# Usage example
if __name__ == "__main__":
    # Example usage with mock vectorstore
    print("Context Enhancer Test")
    print("=" * 50)
    
    # Test queries
    test_queries = [
        ("Create a FAUST reverb with early reflections", "faust"),
        ("Build a JUCE audio plugin with parameter automation", "juce"),
        ("Integrate FAUST DSP into JUCE processor", "general"),
        ("Implement a state-variable filter in FAUST", "faust")
    ]
    
    for query, task_type in test_queries:
        print(f"\\nQuery: {query}")
        print(f"Task Type: {task_type}")
        print(f"Expected enhancements: Domain-specific context retrieval")
        print("-" * 30)