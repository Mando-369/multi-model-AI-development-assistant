import os
import re
from typing import Optional, List, Tuple, Dict, Union
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .project_manager import ProjectManager
from .file_processor import FileProcessor
from .prompts import SYSTEM_PROMPTS
from .context_enhancer import ContextEnhancer, enhance_vectorstore_retrieval

# HRM local wrapper import
from ..integrations.hrm_local_wrapper import HRMLocalWrapper, HRMDecomposition, SubTask



class MultiModelGLMSystem:
    def __init__(self):
        # Initialize models - Updated model configuration
        self.models = {
            "DeepSeek-R1 (Reasoning)": "deepseek-r1:70b",
            "Qwen2.5-Coder (Implementation)": "qwen2.5-coder:32b",
            "Qwen2.5 (Math/Physics)": "qwen2.5:32b",
        }

        # Cache for model instances
        self._model_instances = {}
        
        # Initialize pattern-based routing rules
        self.routing_patterns = self._initialize_routing_patterns()
        
        # Initialize fallback strategies
        self.fallback_matrix = self._initialize_fallback_matrix()
        
        # Initialize HRM local wrapper
        self.hrm_wrapper = HRMLocalWrapper(
            device="auto",  # Will auto-detect MPS on M4 Max
            enable_caching=True
        )

        # Initialize embeddings and vectorstore
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        self.vectorstore = Chroma(
            persist_directory="./chroma_db", embedding_function=self.embeddings
        )

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )

        # Initialize managers
        self.project_manager = ProjectManager()
        self.file_processor = FileProcessor(self.vectorstore, self.text_splitter)

        # Create necessary directories
        os.makedirs("./uploads", exist_ok=True)
        os.makedirs("./projects", exist_ok=True)
        os.makedirs("./chroma_db", exist_ok=True)
        os.makedirs("./faust_documentation", exist_ok=True)
        
        # Initialize context enhancer after vectorstore is ready
        self.context_enhancer = ContextEnhancer(self.vectorstore)
    
    def _initialize_routing_patterns(self):
        """Initialize pattern-based routing rules for intelligent task routing"""
        return {
            "faust_synthesis": {
                "patterns": [
                    r"(create|write|generate|implement).*(faust|dsp|filter|oscillator|reverb|delay|chorus|flanger|phaser)",
                    r"(audio|sound|synthesis|signal)\s+processing",
                    r"impulse response|transfer function|biquad|state.variable|butterworth|chebyshev",
                    r"(anti.alias|band.limit|polyblep|wavetable|granular)",
                    r"(adsr|envelope|lfo|modulation|vibrato|tremolo)"
                ],
                "primary_model": "Qwen2.5-Coder (Implementation)",
                "secondary_model": "DeepSeek-R1 (Reasoning)",
                "confidence_threshold": 0.8,
                "complexity_threshold": 6
            },
            "system_architecture": {
                "patterns": [
                    r"(design|architect|structure|organize).*(system|application|framework|class|module)",
                    r"(refactor|reorganize|restructure).*(architecture|code|system)",
                    r"(dependency|coupling|cohesion|solid|design.pattern)",
                    r"(multi.model|orchestration|routing|dispatch)",
                    r"(thread.safe|lock.free|concurrent|parallel)"
                ],
                "primary_model": "DeepSeek-R1 (Reasoning)",
                "secondary_model": "Qwen2.5-Coder (Implementation)",
                "confidence_threshold": 0.75,
                "complexity_threshold": 7
            },
            "juce_integration": {
                "patterns": [
                    r"(juce|plugin|vst|au|aax|processor).*(integration|implementation|development)",
                    r"(audio.processor|parameter|value.tree|midi|buffer)",
                    r"(gui|editor|component|look.and.feel|animation)",
                    r"(real.time|callback|thread.safety|memory.pool)"
                ],
                "primary_model": "Qwen2.5-Coder (Implementation)",
                "secondary_model": "DeepSeek-R1 (Reasoning)",
                "confidence_threshold": 0.8,
                "complexity_threshold": 6
            },
            "optimization_performance": {
                "patterns": [
                    r"(optimize|improve|speed.up|accelerate|performance)",
                    r"(simd|vectorize|sse|avx|neon|cache.friendly)",
                    r"(memory.management|allocation|pool|leak)",
                    r"(profile|benchmark|measure|latency|throughput)",
                    r"(c\+\+20|c\+\+23|concepts|ranges|coroutines)"
                ],
                "primary_model": "Qwen2.5-Coder (Implementation)",
                "secondary_model": "DeepSeek-R1 (Reasoning)",
                "confidence_threshold": 0.7,
                "complexity_threshold": 5
            },
            "math_physics": {
                "patterns": [
                    r"(calculate|compute|solve|derive|equation)",
                    r"(math|physics|calculus|algebra|trigonometry)",
                    r"(differential|integral|fourier|laplace|z.transform)",
                    r"(signal|frequency|amplitude|phase|spectrum)",
                    r"(acoustic|resonance|harmonic|overtone)"
                ],
                "primary_model": "Qwen2.5 (Math/Physics)",
                "secondary_model": "DeepSeek-R1 (Reasoning)",
                "confidence_threshold": 0.8,
                "complexity_threshold": 5
            }
        }
    
    def _initialize_fallback_matrix(self):
        """Initialize fallback strategies for model unavailability"""
        return {
            "DeepSeek-R1 (Reasoning)": {
                "unavailable": ["Qwen2.5-Coder (Implementation)", "Qwen2.5 (Math/Physics)"],
                "timeout": ["Split task into smaller parts", "Retry with simplified prompt"],
                "error": ["Clear context and retry", "Use alternative model"]
            },
            "Qwen2.5-Coder (Implementation)": {
                "unavailable": ["DeepSeek-R1 (Reasoning)", "Qwen2.5 (Math/Physics)"],
                "timeout": ["Reduce code complexity", "Break into smaller functions"],
                "error": ["Validate syntax", "Check documentation context"]
            },
            "Qwen2.5 (Math/Physics)": {
                "unavailable": ["DeepSeek-R1 (Reasoning)", "Qwen2.5-Coder (Implementation)"],
                "timeout": ["Simplify calculation", "Break into smaller steps"],
                "error": ["Fall back to reasoning model", "Use standard patterns"]
            }
        }

    def get_model_instance(self, model_name: str):
        """Get or create a cached model instance"""
        if model_name not in self._model_instances:
            model_id = self.models.get(model_name)
            if model_id:
                try:
                    self._model_instances[model_name] = Ollama(
                        model=model_id,
                        temperature=0.7,
                        system=SYSTEM_PROMPTS.get(model_name, ""),
                    )
                except Exception as e:
                    print(f"Error loading model {model_name}: {e}")
                    return None

        return self._model_instances.get(model_name)

    def generate_response(
        self, 
        prompt: str, 
        selected_model: str = "auto", 
        routing_mode: str = "auto", 
        context: str = "",
        use_context: bool = True,
        project_name: str = "Default", 
        chat_history: Optional[List[Tuple[str, str]]] = None,
        use_hrm_decomposition: bool = True
    ) -> Dict[str, Union[str, Dict]]:
        """Enhanced routing with hybrid manual + auto mode support
        
        Args:
            prompt: User's request
            selected_model: "auto" or specific model name
            routing_mode: "manual", "auto", or "assisted"
            context: Additional context
            use_context: Whether to use knowledge base context
            project_name: Project name for context
            chat_history: Previous conversation
            use_hrm_decomposition: Whether to use HRM for complex tasks
            
        Returns:
            Dict with response and routing metadata
        """
        try:
            # Step 1: Always run HRM analysis (even in manual mode for recommendations)
            hrm_analysis = self._analyze_with_hrm(prompt, context)
            
            # Step 2: Determine final model based on routing mode
            final_model, routing_decision = self._determine_final_model(
                prompt, selected_model, routing_mode, hrm_analysis
            )
            
            # Step 3: Execute with chosen model
            if hrm_analysis.get("complexity_score", 0) > 0.7 and routing_mode == "auto":
                # Complex task - use HRM orchestration
                response_text = self._execute_complex_orchestration(
                    prompt, hrm_analysis, use_context, project_name, chat_history
                )
            else:
                # Simple task - direct model execution
                response_text = self.chat_with_model(
                    prompt, final_model, use_context, project_name, chat_history
                )
            
            # Step 4: Compile routing metadata
            routing_info = {
                "mode": routing_mode,
                "selected_model": final_model,
                "hrm_recommendation": hrm_analysis.get("recommended_model", final_model),
                "complexity_score": hrm_analysis.get("complexity_score", 0),
                "domain": hrm_analysis.get("domain", "general"),
                "confidence": hrm_analysis.get("confidence_score", 1.0),
                "subtasks": hrm_analysis.get("subtask_count", 0),
                "execution_time": hrm_analysis.get("execution_time", 0),
                "fallback_used": routing_decision.get("fallback_used", False),
                "routing_reason": routing_decision.get("reason", "Direct selection")
            }
            
            return {
                "response": response_text,
                "routing": routing_info
            }
            
        except Exception as e:
            # Fallback to basic chat
            fallback_model = self._get_fallback_model(selected_model)
            response_text = self.chat_with_model(
                prompt, fallback_model, use_context, project_name, chat_history
            )
            
            return {
                "response": response_text,
                "routing": {
                    "mode": "fallback",
                    "selected_model": fallback_model,
                    "error": str(e),
                    "fallback_used": True
                }
            }
    
    def _analyze_with_hrm(self, prompt: str, context: str) -> Dict:
        """Always run HRM analysis for routing intelligence"""
        try:
            # Pattern-based quick analysis
            domain, confidence = self._detect_domain_patterns(prompt)
            complexity_score = self._estimate_complexity(prompt)
            recommended_model = self._recommend_model_from_patterns(prompt, domain, complexity_score)
            
            # For complex tasks, use full HRM decomposition
            if complexity_score > 0.7:
                hrm_decomposition = self.hrm_wrapper.decompose_task(prompt, context={"domain": domain})
                return {
                    "complexity_score": complexity_score,
                    "domain": domain,
                    "confidence_score": confidence,
                    "recommended_model": recommended_model,
                    "subtask_count": len(hrm_decomposition.subtasks),
                    "hrm_decomposition": hrm_decomposition,
                    "execution_time": 0
                }
            else:
                return {
                    "complexity_score": complexity_score,
                    "domain": domain,
                    "confidence_score": confidence,
                    "recommended_model": recommended_model,
                    "subtask_count": 0,
                    "execution_time": 0
                }
                
        except Exception as e:
            print(f"⚠️ HRM analysis failed, using basic routing: {e}")
            return {
                "complexity_score": 0.3,
                "domain": "general",
                "confidence_score": 0.5,
                "recommended_model": "DeepSeek-R1 (Reasoning)",
                "subtask_count": 0,
                "execution_time": 0
            }
    
    def _detect_domain_patterns(self, prompt: str) -> Tuple[str, float]:
        """Detect domain using pattern matching"""
        prompt_lower = prompt.lower()
        best_domain = "general"
        best_confidence = 0.0
        
        for domain, config in self.routing_patterns.items():
            domain_confidence = 0.0
            pattern_matches = 0
            
            for pattern in config["patterns"]:
                if re.search(pattern, prompt_lower):
                    pattern_matches += 1
                    domain_confidence += 0.2  # Each pattern adds 20% confidence
            
            # Normalize confidence based on pattern matches
            if pattern_matches > 0:
                domain_confidence = min(domain_confidence, 1.0)
                if domain_confidence > best_confidence:
                    best_confidence = domain_confidence
                    best_domain = domain
        
        return best_domain, best_confidence
    
    def _estimate_complexity(self, prompt: str) -> float:
        """Estimate task complexity on 0-1 scale"""
        complexity_indicators = [
            (r"(create|build|implement|develop).*(complete|full|entire|comprehensive)", 0.3),
            (r"(multiple|several|many|various).*(component|module|class|function)", 0.2),
            (r"(integrate|combine|merge|connect).*(with|and|plus)", 0.2),
            (r"(optimize|refactor|redesign|restructure)", 0.15),
            (r"(real.time|thread.safe|high.performance|low.latency)", 0.2),
            (r"(test|debug|profile|benchmark)", 0.1),
            (r"(documentation|comment|explain|describe)", -0.1),
            (r"(simple|basic|quick|small)", -0.2)
        ]
        
        base_complexity = 0.3  # Base complexity
        prompt_lower = prompt.lower()
        
        for pattern, weight in complexity_indicators:
            if re.search(pattern, prompt_lower):
                base_complexity += weight
        
        # Word count factor
        word_count = len(prompt.split())
        if word_count > 50:
            base_complexity += 0.2
        elif word_count > 100:
            base_complexity += 0.3
            
        return max(0.0, min(1.0, base_complexity))
    
    def get_routing_suggestion(self, prompt: str, selected_model: str) -> Dict[str, Union[str, float]]:
        """Get routing suggestion for UI display in assisted mode"""
        hrm_analysis = self._analyze_with_hrm(prompt, "")
        
        suggestion = {
            "recommended_model": hrm_analysis.get("recommended_model"),
            "confidence": hrm_analysis.get("confidence_score", 0.0),
            "complexity": hrm_analysis.get("complexity_score", 0.0),
            "domain": hrm_analysis.get("domain", "general"),
            "reason": f"Best suited for {hrm_analysis.get('domain')} tasks with complexity {hrm_analysis.get('complexity_score', 0):.2f}"
        }
        
        if selected_model != hrm_analysis.get("recommended_model"):
            suggestion["alternative_suggested"] = True
            suggestion["user_choice_supported"] = True
        else:
            suggestion["alternative_suggested"] = False
            
        return suggestion
    
    def _recommend_model_from_patterns(self, prompt: str, domain: str, complexity_score: float) -> str:
        """Recommend model based on patterns and complexity"""
        if domain in self.routing_patterns:
            config = self.routing_patterns[domain]
            
            # Use secondary model for very complex tasks in this domain
            if complexity_score > config.get("complexity_threshold", 7) / 10:
                return config.get("secondary_model", config["primary_model"])
            else:
                return config["primary_model"]
        
        # Fallback based on complexity
        if complexity_score > 0.7:
            return "DeepSeek-R1 (Reasoning)"  # Best for complex reasoning
        elif "faust" in prompt.lower() or "dsp" in prompt.lower():
            return "Qwen2.5-Coder (Implementation)"
        elif "math" in prompt.lower() or "physics" in prompt.lower() or "calculate" in prompt.lower():
            return "Qwen2.5 (Math/Physics)"
        else:
            return "Qwen2.5-Coder (Implementation)"
    
    def _determine_final_model(self, prompt: str, selected_model: str, routing_mode: str, hrm_analysis: Dict) -> Tuple[str, Dict]:
        """Determine final model based on routing mode"""
        routing_decision = {"reason": "", "fallback_used": False}
        
        if routing_mode == "manual" and selected_model != "auto":
            # Manual mode - respect user choice but provide suggestion
            routing_decision["reason"] = "Manual selection by user"
            if selected_model != hrm_analysis.get("recommended_model"):
                routing_decision["suggestion"] = f"HRM recommends {hrm_analysis.get('recommended_model')}"
            return selected_model, routing_decision
            
        elif routing_mode == "auto" or selected_model == "auto":
            # Auto mode - use HRM recommendation
            routing_decision["reason"] = f"HRM auto-routing (domain: {hrm_analysis.get('domain')}, complexity: {hrm_analysis.get('complexity_score'):.2f})"
            return hrm_analysis.get("recommended_model", "DeepSeek-R1 (Reasoning)"), routing_decision
            
        elif routing_mode == "assisted":
            # Assisted mode - provide recommendation but wait for confirmation
            # For now, use recommendation (UI would handle confirmation)
            routing_decision["reason"] = "Assisted mode using HRM recommendation"
            return hrm_analysis.get("recommended_model", selected_model), routing_decision
            
        else:
            # Fallback
            routing_decision["reason"] = "Fallback to default model"
            return "DeepSeek-R1 (Reasoning)", routing_decision
    
    def _execute_complex_orchestration(self, prompt: str, hrm_analysis: Dict, use_context: bool, project_name: str, chat_history: Optional[List[Tuple[str, str]]]) -> str:
        """Execute complex task using HRM orchestration"""
        if "hrm_decomposition" in hrm_analysis:
            return self._process_hrm_decomposition(
                hrm_analysis["hrm_decomposition"], 
                use_context, 
                project_name, 
                chat_history
            )
        else:
            # Fallback to enhanced chat if no decomposition available
            return self.chat_with_model_enhanced(
                prompt, 
                hrm_analysis.get("recommended_model", "DeepSeek-R1 (Reasoning)"),
                use_context, 
                project_name, 
                chat_history, 
                use_hrm_decomposition=True
            )
    
    def _get_fallback_model(self, failed_model: str) -> str:
        """Get fallback model when primary fails"""
        if failed_model in self.fallback_matrix:
            fallback_options = self.fallback_matrix[failed_model].get("unavailable", [])
            for fallback in fallback_options:
                if self.get_model_instance(fallback):
                    return fallback
        
        # Ultimate fallback
        return "DeepSeek-R1 (Reasoning)"
    
    def chat_with_model_enhanced(
        self,
        question: str,
        model_name: str,
        use_context: bool = True,
        project_name: str = "Default", 
        chat_history: Optional[List[Tuple[str, str]]] = None,
        use_hrm_decomposition: bool = True,
    ) -> str:
        """Enhanced chat with HRM task decomposition for complex queries"""
        try:
            # Step 1: Use HRM for task decomposition
            if use_hrm_decomposition:
                context_info = {
                    'project': project_name,
                    'model': model_name,
                    'use_context': use_context
                }
                
                hrm_decomposition = self.hrm_wrapper.decompose_task(
                    question, 
                    context=context_info
                )
                
                # If task has multiple subtasks, process hierarchically
                if len(hrm_decomposition.subtasks) > 1:
                    print(f"🧠 HRM decomposed task into {len(hrm_decomposition.subtasks)} subtasks")
                    return self._process_hrm_decomposition(hrm_decomposition, use_context, project_name, chat_history)
            
            # Step 2: Use original processing for simple tasks
            return self.chat_with_model(
                question, model_name, use_context, project_name, chat_history
            )
            
        except Exception as e:
            print(f"❌ Enhanced chat failed, falling back to standard: {e}")
            return self.chat_with_model(
                question, model_name, use_context, project_name, chat_history
            )
    
    def _process_hrm_decomposition(
        self, 
        hrm_decomposition: HRMDecomposition, 
        use_context: bool, 
        project_name: str,
        chat_history: Optional[List[Tuple[str, str]]]
    ) -> str:
        """Process HRM decomposition with structured execution"""
        results = []
        context_accumulator = []
        
        # Get optimal execution order
        execution_order = self.hrm_wrapper.get_execution_order(hrm_decomposition)
        
        print(f"📋 Processing {len(hrm_decomposition.subtasks)} HRM subtasks:")
        print(f"🎯 Execution strategy: {hrm_decomposition.execution_strategy}")
        
        subtasks_by_id = {st.id: st for st in hrm_decomposition.subtasks}
        
        # Process subtasks in optimal order
        for phase, task_ids in enumerate(execution_order, 1):
            print(f"\n🔄 Phase {phase}: Processing {len(task_ids)} task(s)")
            
            phase_results = []
            for task_id in task_ids:
                subtask = subtasks_by_id[task_id]
                
                print(f"  🎯 {subtask.id}: {subtask.description}")
                print(f"     Model: {subtask.model_preference} | Complexity: {subtask.complexity}/10")
                
                # Build enhanced prompt with HRM context
                enhanced_prompt = self._build_hrm_prompt(
                    subtask,
                    hrm_decomposition,
                    context_accumulator
                )
                
                # Process subtask
                try:
                    subtask_result = self.chat_with_model(
                        enhanced_prompt,
                        subtask.model_preference,
                        use_context,
                        project_name,
                        chat_history
                    )
                    
                    result_entry = {
                        'subtask_id': subtask.id,
                        'description': subtask.description,
                        'result': subtask_result,
                        'model': subtask.model_preference,
                        'complexity': subtask.complexity,
                        'phase': phase
                    }
                    
                    results.append(result_entry)
                    phase_results.append(result_entry)
                    
                    # Add to context for subsequent subtasks
                    context_accumulator.append(f"Subtask {subtask.id}: {subtask.description}")
                    context_accumulator.append(f"Result: {subtask_result[:300]}{'...' if len(subtask_result) > 300 else ''}")
                    
                    print(f"     ✅ Completed successfully")
                    
                except Exception as e:
                    print(f"     ❌ Failed: {e}")
                    results.append({
                        'subtask_id': subtask.id,
                        'description': subtask.description,
                        'result': f"Error processing subtask: {e}",
                        'model': subtask.model_preference,
                        'complexity': subtask.complexity,
                        'phase': phase
                    })
            
            print(f"✅ Phase {phase} completed ({len([r for r in phase_results if 'Error' not in r['result']])}/{len(task_ids)} successful)")
        
        # Synthesize final result
        return self._synthesize_hrm_results(hrm_decomposition, results)
    
    def _build_hrm_prompt(
        self, 
        subtask: SubTask, 
        hrm_decomposition: HRMDecomposition,
        context_accumulator: List[str]
    ) -> str:
        """Build enhanced prompt for HRM subtask"""
        prompt_parts = [
            f"=== HRM TASK DECOMPOSITION CONTEXT ===",
            f"Original Query: {hrm_decomposition.original_query}",
            f"Current Subtask: {subtask.description}",
            f"Task Type: {subtask.task_type}",
            f"Complexity Level: {subtask.complexity}/10",
            f"Priority: {subtask.priority}/5",
            ""
        ]
        
        # Add dependency context
        if subtask.dependencies:
            prompt_parts.extend([
                "=== DEPENDENCIES ===",
                f"This subtask depends on: {', '.join(subtask.dependencies)}",
                "Please build upon the results from these previous subtasks.",
                ""
            ])
        
        # Add previous context
        if context_accumulator:
            prompt_parts.extend([
                "=== PREVIOUS SUBTASKS ===",
                "\n".join(context_accumulator[-4:]),  # Last 2 subtasks for context
                ""
            ])
        
        # Add domain expertise requirements
        if subtask.domain_expertise_required:
            prompt_parts.extend([
                "=== DOMAIN EXPERTISE REQUIRED ===",
                f"This subtask requires specialized {subtask.task_type.upper()} knowledge.",
                "Please provide detailed, technically accurate implementation.",
                ""
            ])
        
        # Add context requirements
        if subtask.context_requirements:
            prompt_parts.extend([
                "=== CONTEXT REQUIREMENTS ===",
                f"Please consider: {', '.join(subtask.context_requirements)}",
                ""
            ])
        
        prompt_parts.extend([
            "=== SPECIFIC SUBTASK ===",
            subtask.description,
            "",
            f"Target output length: ~{subtask.estimated_tokens} tokens",
            "Please provide a focused, comprehensive response for this specific subtask."
        ])
        
        return "\n".join(prompt_parts)
    
    def _synthesize_hrm_results(
        self, 
        hrm_decomposition: HRMDecomposition, 
        results: List[Dict]
    ) -> str:
        """Synthesize HRM subtask results into final response"""
        successful_results = [r for r in results if 'Error' not in r['result']]
        
        synthesis_parts = [
            f"# 🧠 HRM Hierarchical Response\n",
            f"**Original Query:** {hrm_decomposition.original_query}\n",
            f"**Execution Strategy:** {hrm_decomposition.execution_strategy}\n",
            f"**Subtasks Processed:** {len(successful_results)}/{len(results)}\n",
            f"**Total Complexity:** {hrm_decomposition.total_complexity}/10\n",
            f"**Confidence Score:** {hrm_decomposition.confidence_score:.1%}\n"
        ]
        
        # Add reasoning chain
        if hrm_decomposition.reasoning_chain:
            synthesis_parts.extend([
                "## 🔍 HRM Reasoning Chain",
                "\n".join(f"- {step}" for step in hrm_decomposition.reasoning_chain),
                ""
            ])
        
        # Group results by phase
        results_by_phase = {}
        for result in results:
            phase = result.get('phase', 1)
            if phase not in results_by_phase:
                results_by_phase[phase] = []
            results_by_phase[phase].append(result)
        
        # Add results by execution phase
        synthesis_parts.append("## 📋 Subtask Results by Execution Phase\n")
        
        for phase in sorted(results_by_phase.keys()):
            phase_results = results_by_phase[phase]
            synthesis_parts.append(f"### Phase {phase}\n")
            
            for result in phase_results:
                status = "✅" if 'Error' not in result['result'] else "❌"
                synthesis_parts.extend([
                    f"#### {status} {result['subtask_id']}: {result['description']}",
                    f"*Model: {result['model']} | Complexity: {result['complexity']}/10*\n",
                    result['result'],
                    "---\n"
                ])
        
        # Add execution summary
        synthesis_parts.extend([
            "## 🎯 Execution Summary",
            f"The task was decomposed using HRM into {len(hrm_decomposition.subtasks)} specialized subtasks.",
            f"Each subtask was assigned to the optimal model based on domain expertise and complexity.",
            f"Execution followed a {hrm_decomposition.execution_strategy} strategy with proper dependency management.\n"
        ])
        
        # Add model usage statistics
        model_usage = {}
        for result in successful_results:
            model = result['model']
            model_usage[model] = model_usage.get(model, 0) + 1
        
        if model_usage:
            synthesis_parts.extend([
                "### 📊 Model Usage Statistics",
                "\n".join(f"- **{model}**: {count} subtask(s)" for model, count in model_usage.items()),
                ""
            ])
        
        # Add HRM metadata
        if hrm_decomposition.metadata:
            device = hrm_decomposition.metadata.get('device', 'unknown')
            method = hrm_decomposition.metadata.get('method', 'unknown')
            synthesis_parts.append(f"*Processed using HRM {method} method on {device} device*")
        
        return "\n".join(synthesis_parts)
    
    def chat_with_model(
        self,
        question: str,
        model_name: str,
        use_context: bool = True,
        project_name: str = "Default",
        chat_history: Optional[List[Tuple[str, str]]] = None,
    ) -> str:
        """Chat with a specific model with enhanced context"""
        try:
            # Get model instance
            llm = self.get_model_instance(model_name)
            if not llm:
                return f"❌ Model {model_name} is not available. Please check if it's installed with 'ollama pull {self.models[model_name]}'"

            # Ensure chat_history is a list
            if chat_history is None:
                chat_history = []

            # Build enhanced context if enabled
            if use_context:
                context_parts = []

                # 1. Get enhanced knowledge base context
                try:
                    # Determine task type from question
                    task_type = "general"
                    question_lower = question.lower()
                    if any(term in question_lower for term in ["faust", "dsp", "signal processing", "audio effect"]):
                        task_type = "faust"
                    elif any(term in question_lower for term in ["juce", "plugin", "vst", "au", "processor"]):
                        task_type = "juce"
                    
                    # Get enhanced context
                    enhanced_context = enhance_vectorstore_retrieval(self.vectorstore, question, task_type)
                    
                    if enhanced_context:
                        context_parts.append(enhanced_context)
                        print(f"✅ Enhanced context retrieved for {task_type} task")
                    else:
                        # Fallback to basic retrieval
                        relevant_docs = self.vectorstore.similarity_search(question, k=5)
                        if relevant_docs:
                            kb_context = "\n\n".join(
                                [doc.page_content for doc in relevant_docs]
                            )
                            context_parts.append(
                                f"=== KNOWLEDGE BASE CONTEXT ===\n{kb_context[:3000]}"
                            )
                            print(f"✅ Found {len(relevant_docs)} relevant documents from knowledge base")
                        else:
                            print("⚠️ No relevant documents found in knowledge base")
                except Exception as e:
                    print(f"❌ Error accessing enhanced knowledge base: {e}")

                # 2. Get conversation history context
                if chat_history and len(chat_history) > 0:
                    # Include last 5 exchanges for context
                    recent_history = (
                        chat_history[-5:] if len(chat_history) > 5 else chat_history
                    )
                    history_context = []

                    for i, (prev_q, prev_a) in enumerate(recent_history, 1):
                        history_context.append(f"Exchange {i}:")
                        history_context.append(f"Human: {prev_q}")
                        history_context.append(
                            f"Assistant: {prev_a[:500]}{'...' if len(prev_a) > 500 else ''}"
                        )
                        history_context.append("")

                    if history_context:
                        context_parts.append(
                            f"=== CONVERSATION HISTORY ===\n"
                            + "\n".join(history_context)
                        )
                        print(
                            f"✅ Including {len(recent_history)} previous exchanges for context"
                        )

                # 3. Get project context
                try:
                    project_context = self.project_manager.get_project_context(
                        project_name
                    )
                    if project_context:
                        context_parts.append(
                            f"=== PROJECT CONTEXT ===\n{project_context}"
                        )
                        print(f"✅ Including project context from {project_name}")
                except Exception as e:
                    print(f"❌ Error getting project context: {e}")

                # Build the enhanced prompt
                if context_parts:
                    full_context = "\n\n".join(context_parts)
                    enhanced_prompt = f"""{full_context}

=== CURRENT QUESTION ===
{question}

=== INSTRUCTIONS ===
Please provide a detailed and helpful response based on the context above and your knowledge. 
If the conversation history shows we were discussing something specific, please continue that conversation naturally.
Reference the knowledge base information when relevant."""

                    print(
                        f"🚀 Sending enhanced prompt with {len(context_parts)} context sections"
                    )
                    response = llm.invoke(enhanced_prompt)
                else:
                    print("⚠️ No context available, using basic prompt")
                    response = llm.invoke(question)
            else:
                print("📝 Context disabled, using direct question")
                response = llm.invoke(question)

            # Track model usage in project
            metadata = self.project_manager.get_project_metadata(project_name)
            if model_name not in metadata.get("models_used", []):
                metadata.setdefault("models_used", []).append(model_name)
                self.project_manager.update_project_metadata(project_name, metadata)

            return response

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}\n\nMake sure the model is installed with:\nollama pull {self.models[model_name]}"
            print(f"❌ Chat error: {e}")
            return error_msg

    def check_vectorstore_status(self):
        """Check if vectorstore has documents and get count (excluding test documents)"""
        try:
            # Get actual document count from ChromaDB collection, excluding test documents
            collection = self.vectorstore._collection
            
            # Get all documents with metadata to filter out test documents
            all_docs = collection.get(include=['metadatas'])
            
            # Count only non-test documents
            real_doc_count = 0
            test_doc_count = 0
            
            for meta in all_docs['metadatas']:
                if meta.get('is_test_data', False):
                    test_doc_count += 1
                else:
                    real_doc_count += 1
            
            total_count = real_doc_count + test_doc_count
            
            # Status message includes both counts for transparency
            if real_doc_count > 0:
                message = f"Knowledge base contains {real_doc_count} documents"
                if test_doc_count > 0:
                    message += f" ({test_doc_count} test documents excluded)"
            else:
                if test_doc_count > 0:
                    message = f"No real documents loaded ({test_doc_count} test documents excluded). Upload files or load documentation."
                else:
                    message = "No documents in knowledge base. Upload files to improve context."
            
            return {
                "status": "✅ Ready" if real_doc_count > 0 else "⚠️ Empty",
                "document_count": real_doc_count,
                "total_count": total_count,
                "test_count": test_doc_count,
                "message": message,
            }
            
        except Exception as e:
            # Fallback to similarity search method if direct count fails
            try:
                test_results = self.vectorstore.similarity_search("test", k=100)  # Higher limit
                doc_count = len(test_results)
                return {
                    "status": "✅ Ready" if doc_count > 0 else "⚠️ Empty",
                    "document_count": doc_count,
                    "total_count": doc_count,
                    "test_count": 0,
                    "message": (
                        f"Knowledge base contains {doc_count}+ documents (test filtering unavailable)"
                        if doc_count > 0
                        else "No documents in knowledge base. Upload files to improve context."
                    ),
                }
            except Exception as fallback_error:
                return {
                    "status": "❌ Error",
                    "document_count": 0,
                    "total_count": 0,
                    "test_count": 0,
                    "message": f"Error accessing knowledge base: {fallback_error}",
                }

    def check_model_availability(self):
        """Check which models are available"""
        status = {}

        for model_name, model_id in self.models.items():
            try:
                # Try to create an instance
                llm = Ollama(model=model_id)
                # Try a simple test
                llm.invoke("test")
                status[model_name] = "✅ Available"
            except Exception as e:
                if "not found" in str(e).lower():
                    status[model_name] = f"❌ Not installed"
                else:
                    status[model_name] = f"⚠️ Error: {str(e)[:50]}"

        return status

    def get_available_models(self):
        """Get list of available models"""
        available = []
        for model_name in self.models.keys():
            if model_name in self._model_instances:
                available.append(model_name)
            else:
                # Try to load it
                if self.get_model_instance(model_name):
                    available.append(model_name)

        return available
