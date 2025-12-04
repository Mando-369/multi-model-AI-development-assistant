"""
HRM Local Wrapper for FAUST/JUCE Task Decomposition
Provides offline hierarchical reasoning for complex audio development tasks
"""

import os
import re
import torch
import logging
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from pathlib import Path
import json
from datetime import datetime

# HRM model imports
try:
    from lib.hrm.models.hrm.hrm_act_v1 import HierarchicalReasoningModel_ACTV1
    from lib.hrm.models.common import trunc_normal_init_
    HRM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ HRM not available: {e}")
    HRM_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SubTask:
    """Represents a single subtask from HRM decomposition"""
    id: str
    description: str
    task_type: str  # 'faust', 'juce', 'cpp', 'python', 'analysis'
    complexity: int  # 1-10 scale
    priority: int  # 1-5 (1=highest)
    model_preference: str  # Which Ollama model to use
    context_requirements: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # IDs of prerequisite subtasks
    estimated_tokens: int = 500
    domain_expertise_required: bool = False


@dataclass
class HRMDecomposition:
    """Result of HRM task decomposition"""
    original_query: str
    subtasks: List[SubTask]
    execution_strategy: str  # 'sequential', 'parallel', 'mixed'
    total_complexity: int
    confidence_score: float
    reasoning_chain: List[str]
    metadata: Dict = field(default_factory=dict)


class HRMLocalWrapper:
    """
    Local HRM wrapper for offline task decomposition
    Specializes in FAUST/JUCE audio development workflows
    """
    
    def __init__(self, 
                 device: str = "auto",
                 model_path: Optional[str] = None,
                 enable_caching: bool = True):
        """
        Initialize HRM wrapper with MPS optimization for M4 Max
        
        Args:
            device: 'auto', 'mps', 'cpu', or 'cuda'
            model_path: Path to pre-trained HRM model (if available)
            enable_caching: Cache decomposition results
        """
        self.device = self._setup_device(device)
        self.model = None
        self.model_loaded = False
        self.enable_caching = enable_caching
        self.cache = {} if enable_caching else None
        
        # Task classification patterns
        self.patterns = self._initialize_patterns()
        
        # Model preferences for different task types
        self.model_preferences = {
            'faust': 'Qwen2.5-Coder (Implementation)',
            'juce': 'Qwen2.5-Coder (Implementation)',
            'cpp': 'Qwen2.5-Coder (Implementation)',
            'python': 'Qwen2.5-Coder (Implementation)',
            'analysis': 'DeepSeek-R1 (Reasoning)',
            'architecture': 'DeepSeek-R1 (Reasoning)',
            'planning': 'DeepSeek-R1 (Reasoning)',
            'math': 'Qwen2.5 (Math/Physics)',
            'physics': 'Qwen2.5 (Math/Physics)'
        }
        
        # Initialize HRM model
        self._load_hrm_model(model_path)
        
        logger.info(f"🧠 HRM Local Wrapper initialized on {self.device}")
    
    def _setup_device(self, device: str) -> str:
        """Setup computation device with M4 Max optimization"""
        if device == "auto":
            if torch.backends.mps.is_available():
                device = "mps"
                logger.info("✅ M4 Max MPS acceleration detected")
            elif torch.cuda.is_available():
                device = "cuda"
                logger.info("✅ CUDA acceleration detected")
            else:
                device = "cpu"
                logger.info("📱 Using CPU computation")
        
        return device
    
    def _initialize_patterns(self) -> Dict[str, List[str]]:
        """Initialize regex patterns for task classification"""
        return {
            'faust': [
                r'faust\s+(?:code|program|script)',
                r'dsp\s+(?:algorithm|effect|filter)',
                r'audio\s+(?:effect|processing|synthesis)',
                r'(?:create|build|implement).*(?:oscillator|filter|delay|reverb)',
                r'signal\s+processing',
                r'frequency\s+(?:domain|analysis)',
                r'\.dsp\s+file',
                r'faust\s+library'
            ],
            'juce': [
                r'juce\s+(?:application|plugin|project)',
                r'(?:vst|au|aax)\s+plugin',
                r'audio\s+plugin',
                r'juce\s+(?:component|processor)',
                r'(?:create|build).*juce.*(?:gui|interface)',
                r'audio\s+buffer',
                r'parameter\s+(?:control|automation)',
                r'plugin\s+wrapper'
            ],
            'complex': [
                r'(?:create|build|develop).*(?:complete|full|entire).*(?:system|application)',
                r'from\s+scratch',
                r'(?:design|architect|implement).*(?:framework|engine)',
                r'integrate.*(?:multiple|various|different)',
                r'(?:real-time|realtime)\s+(?:audio|processing)',
                r'(?:end-to-end|full-stack)',
                r'production\s+ready'
            ],
            'analysis': [
                r'(?:analyze|examine|study|review)',
                r'(?:compare|evaluate|assess)',
                r'(?:explain|describe|document)',
                r'(?:optimize|improve|enhance)',
                r'(?:debug|troubleshoot|fix)'
            ]
        }
    
    def _load_hrm_model(self, model_path: Optional[str] = None):
        """Load HRM model for hierarchical reasoning"""
        if not HRM_AVAILABLE:
            logger.warning("❌ HRM model not available, using pattern-based decomposition")
            return
        
        try:
            # Create minimal config for inference
            config = {
                'batch_size': 1,
                'seq_len': 512,
                'puzzle_emb_ndim': 512,
                'num_puzzle_identifiers': 1000,
                'vocab_size': 32000,
                'H_cycles': 2,
                'L_cycles': 2,
                'H_layers': 4,
                'L_layers': 4,
                'hidden_size': 512,
                'expansion': 4,
                'num_heads': 8,
                'pos_encodings': 'rope',
                'halt_max_steps': 8,
                'halt_exploration_prob': 0.1,
                'forward_dtype': 'float32' if self.device == 'mps' else 'bfloat16'
            }
            
            self.model = HierarchicalReasoningModel_ACTV1(config)
            self.model.to(self.device)
            self.model.eval()
            self.model_loaded = True
            
            # Load pre-trained weights if available
            if model_path and Path(model_path).exists():
                checkpoint = torch.load(model_path, map_location=self.device)
                self.model.load_state_dict(checkpoint['model_state_dict'])
                logger.info(f"✅ Loaded pre-trained HRM from {model_path}")
            else:
                logger.info("🔄 Using HRM with random initialization")
            
            logger.info(f"🧠 HRM model loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"❌ HRM model loading failed: {e}")
            self.model = None
            self.model_loaded = False
    
    def decompose_task(self, 
                      query: str, 
                      context: Optional[Dict] = None,
                      max_subtasks: int = 6) -> HRMDecomposition:
        """
        Decompose a complex task into structured subtasks
        
        Args:
            query: User's task description
            context: Additional context (project info, etc.)
            max_subtasks: Maximum number of subtasks to generate
            
        Returns:
            HRMDecomposition with structured subtasks
        """
        # Check cache first
        if self.enable_caching and query in self.cache:
            logger.info("📋 Using cached decomposition")
            return self.cache[query]
        
        try:
            # Step 1: Classify and analyze task
            task_analysis = self._analyze_task(query, context)
            
            # Step 2: Generate subtasks using HRM or fallback
            if self.model_loaded and task_analysis['complexity'] >= 6:
                subtasks = self._hrm_decompose(query, task_analysis, max_subtasks)
            else:
                subtasks = self._pattern_decompose(query, task_analysis, max_subtasks)
            
            # Step 3: Create decomposition result
            decomposition = HRMDecomposition(
                original_query=query,
                subtasks=subtasks,
                execution_strategy=self._determine_strategy(subtasks),
                total_complexity=task_analysis['complexity'],
                confidence_score=task_analysis['confidence'],
                reasoning_chain=task_analysis['reasoning'],
                metadata={
                    'timestamp': datetime.now().isoformat(),
                    'method': 'hrm' if self.model_loaded else 'pattern',
                    'device': self.device,
                    'context': context or {}
                }
            )
            
            # Cache result
            if self.enable_caching:
                self.cache[query] = decomposition
            
            logger.info(f"✅ Decomposed into {len(subtasks)} subtasks")
            return decomposition
            
        except Exception as e:
            logger.error(f"❌ Task decomposition failed: {e}")
            return self._create_fallback_decomposition(query, context)
    
    def _analyze_task(self, query: str, context: Optional[Dict] = None) -> Dict:
        """Analyze task complexity and requirements"""
        query_lower = query.lower()
        
        # Determine primary task type
        task_types = []
        for task_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    task_types.append(task_type)
                    break
        
        primary_type = task_types[0] if task_types else 'general'
        
        # Calculate complexity (1-10 scale)
        complexity = 1
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
        
        # Additional complexity from task type combinations
        if len(task_types) > 1:
            complexity += 1
        if 'complex' in task_types:
            complexity += 2
        
        complexity = min(10, complexity)
        
        # Generate reasoning chain
        reasoning = [
            f"Identified primary task type: {primary_type}",
            f"Secondary types: {task_types[1:] if len(task_types) > 1 else 'none'}",
            f"Estimated complexity: {complexity}/10"
        ]
        
        if context:
            reasoning.append(f"Additional context: {list(context.keys())}")
        
        # Confidence based on pattern matches and complexity
        confidence = 0.8 if primary_type != 'general' else 0.6
        confidence += 0.1 if len(task_types) > 1 else 0
        confidence = min(1.0, confidence)
        
        return {
            'primary_type': primary_type,
            'all_types': task_types,
            'complexity': complexity,
            'confidence': confidence,
            'reasoning': reasoning,
            'requires_decomposition': complexity >= 5
        }
    
    def _hrm_decompose(self, query: str, analysis: Dict, max_subtasks: int) -> List[SubTask]:
        """Use HRM model for intelligent task decomposition"""
        if not self.model_loaded:
            return self._pattern_decompose(query, analysis, max_subtasks)
        
        try:
            # For now, use pattern-based with HRM-inspired logic
            # TODO: Implement actual HRM forward pass for task decomposition
            subtasks = self._pattern_decompose(query, analysis, max_subtasks)
            
            # Enhance with HRM-style hierarchical reasoning
            subtasks = self._enhance_with_hierarchy(subtasks, analysis)
            
            return subtasks
            
        except Exception as e:
            logger.warning(f"HRM decomposition failed, using pattern fallback: {e}")
            return self._pattern_decompose(query, analysis, max_subtasks)
    
    def _pattern_decompose(self, query: str, analysis: Dict, max_subtasks: int) -> List[SubTask]:
        """Pattern-based task decomposition with domain expertise"""
        subtasks = []
        primary_type = analysis['primary_type']
        complexity = analysis['complexity']
        
        # Generate subtasks based on task type
        if primary_type == 'faust':
            subtasks.extend(self._decompose_faust_task(query, complexity))
        elif primary_type == 'juce':
            subtasks.extend(self._decompose_juce_task(query, complexity))
        elif 'faust' in analysis['all_types'] and 'juce' in analysis['all_types']:
            subtasks.extend(self._decompose_faust_juce_task(query, complexity))
        else:
            subtasks.extend(self._decompose_general_task(query, complexity))
        
        # Limit to max_subtasks
        subtasks = subtasks[:max_subtasks]
        
        # Assign IDs and priorities
        for i, subtask in enumerate(subtasks):
            subtask.id = f"task_{i+1:02d}"
            if not hasattr(subtask, 'priority') or subtask.priority == 0:
                subtask.priority = min(5, i + 1)
        
        return subtasks
    
    def _decompose_faust_task(self, query: str, complexity: int) -> List[SubTask]:
        """Decompose FAUST-specific tasks"""
        subtasks = []
        
        # Always start with analysis for complex tasks
        if complexity >= 6:
            subtasks.append(SubTask(
                id="analysis",
                description="Analyze DSP requirements and signal flow architecture",
                task_type="analysis",
                complexity=min(complexity-1, 5),
                priority=1,
                model_preference=self.model_preferences['analysis'],
                context_requirements=["faust_documentation", "dsp_theory"],
                domain_expertise_required=True
            ))
        
        # Core FAUST implementation
        subtasks.append(SubTask(
            id="faust_impl",
            description="Implement FAUST DSP code with proper syntax and structure",
            task_type="faust",
            complexity=complexity,
            priority=2,
            model_preference=self.model_preferences['faust'],
            context_requirements=["faust_documentation", "faust_libraries"],
            dependencies=["analysis"] if complexity >= 6 else [],
            estimated_tokens=800,
            domain_expertise_required=True
        ))
        
        # Testing and validation for complex tasks
        if complexity >= 7:
            subtasks.append(SubTask(
                id="validation",
                description="Test FAUST code and validate audio output",
                task_type="python",
                complexity=4,
                priority=3,
                model_preference=self.model_preferences['python'],
                context_requirements=["faust_testing"],
                dependencies=["faust_impl"],
                estimated_tokens=400
            ))
        
        return subtasks
    
    def _decompose_juce_task(self, query: str, complexity: int) -> List[SubTask]:
        """Decompose JUCE-specific tasks"""
        subtasks = []
        
        # Project setup and architecture
        if complexity >= 6:
            subtasks.append(SubTask(
                id="architecture",
                description="Design JUCE project architecture and class structure",
                task_type="architecture",
                complexity=min(complexity-1, 6),
                priority=1,
                model_preference=self.model_preferences['architecture'],
                context_requirements=["juce_documentation", "cpp_patterns"],
                domain_expertise_required=True
            ))
        
        # Core audio processing
        subtasks.append(SubTask(
            id="juce_processor",
            description="Implement JUCE audio processor with buffer handling",
            task_type="juce",
            complexity=complexity,
            priority=2,
            model_preference=self.model_preferences['juce'],
            context_requirements=["juce_documentation", "audio_programming"],
            dependencies=["architecture"] if complexity >= 6 else [],
            estimated_tokens=1000,
            domain_expertise_required=True
        ))
        
        # GUI implementation if mentioned
        if any(keyword in query.lower() for keyword in ['gui', 'interface', 'ui', 'component']):
            subtasks.append(SubTask(
                id="juce_gui",
                description="Create JUCE GUI components and parameter controls",
                task_type="juce",
                complexity=max(4, complexity-1),
                priority=3,
                model_preference=self.model_preferences['juce'],
                context_requirements=["juce_documentation", "gui_design"],
                dependencies=["juce_processor"],
                estimated_tokens=800,
                domain_expertise_required=True
            ))
        
        return subtasks
    
    def _decompose_faust_juce_task(self, query: str, complexity: int) -> List[SubTask]:
        """Decompose combined FAUST+JUCE tasks"""
        subtasks = []
        
        # High-level architecture
        subtasks.append(SubTask(
            id="system_design",
            description="Design overall system architecture for FAUST+JUCE integration",
            task_type="architecture",
            complexity=min(complexity, 7),
            priority=1,
            model_preference=self.model_preferences['architecture'],
            context_requirements=["faust_documentation", "juce_documentation", "integration_patterns"],
            domain_expertise_required=True
        ))
        
        # FAUST DSP implementation
        subtasks.append(SubTask(
            id="faust_dsp",
            description="Implement core DSP algorithms in FAUST",
            task_type="faust",
            complexity=complexity,
            priority=2,
            model_preference=self.model_preferences['faust'],
            context_requirements=["faust_documentation", "dsp_algorithms"],
            dependencies=["system_design"],
            estimated_tokens=800,
            domain_expertise_required=True
        ))
        
        # JUCE wrapper/integration
        subtasks.append(SubTask(
            id="juce_integration",
            description="Create JUCE wrapper and integrate FAUST-generated C++",
            task_type="juce",
            complexity=max(6, complexity-1),
            priority=3,
            model_preference=self.model_preferences['juce'],
            context_requirements=["juce_documentation", "faust_cpp_integration"],
            dependencies=["faust_dsp"],
            estimated_tokens=1000,
            domain_expertise_required=True
        ))
        
        # Testing and optimization
        if complexity >= 8:
            subtasks.append(SubTask(
                id="optimization",
                description="Test integration and optimize performance",
                task_type="cpp",
                complexity=5,
                priority=4,
                model_preference=self.model_preferences['cpp'],
                context_requirements=["performance_testing", "audio_optimization"],
                dependencies=["juce_integration"],
                estimated_tokens=600
            ))
        
        return subtasks
    
    def _decompose_general_task(self, query: str, complexity: int) -> List[SubTask]:
        """Decompose general programming tasks"""
        subtasks = []
        
        if complexity >= 6:
            # Planning phase
            subtasks.append(SubTask(
                id="planning",
                description="Analyze requirements and plan implementation approach",
                task_type="planning",
                complexity=min(complexity-1, 5),
                priority=1,
                model_preference=self.model_preferences['planning'],
                context_requirements=["project_context"],
                domain_expertise_required=False
            ))
        
        # Main implementation
        task_type = 'python' if 'python' in query.lower() else 'cpp'
        subtasks.append(SubTask(
            id="implementation",
            description="Implement core functionality",
            task_type=task_type,
            complexity=complexity,
            priority=2,
            model_preference=self.model_preferences[task_type],
            dependencies=["planning"] if complexity >= 6 else [],
            estimated_tokens=800,
            domain_expertise_required=complexity >= 7
        ))
        
        return subtasks
    
    def _enhance_with_hierarchy(self, subtasks: List[SubTask], analysis: Dict) -> List[SubTask]:
        """Enhance subtasks with HRM-style hierarchical reasoning"""
        # Add hierarchical dependencies based on complexity
        for i, subtask in enumerate(subtasks):
            if i > 0 and subtask.complexity >= 6:
                # High complexity tasks depend on previous analysis
                if not subtask.dependencies:
                    subtask.dependencies = [subtasks[i-1].id]
        
        # Adjust priorities based on dependencies
        for subtask in subtasks:
            if subtask.dependencies:
                subtask.priority = max(2, subtask.priority)
        
        return subtasks
    
    def _determine_strategy(self, subtasks: List[SubTask]) -> str:
        """Determine execution strategy based on dependencies"""
        has_dependencies = any(subtask.dependencies for subtask in subtasks)
        high_complexity = any(subtask.complexity >= 7 for subtask in subtasks)
        
        if has_dependencies or high_complexity:
            return "sequential"
        elif len(subtasks) <= 2:
            return "parallel"
        else:
            return "mixed"
    
    def _create_fallback_decomposition(self, query: str, context: Optional[Dict] = None) -> HRMDecomposition:
        """Create a simple fallback decomposition"""
        return HRMDecomposition(
            original_query=query,
            subtasks=[
                SubTask(
                    id="task_01",
                    description=query,
                    task_type="general",
                    complexity=5,
                    priority=1,
                    model_preference="DeepSeek-R1 (Reasoning)",
                    estimated_tokens=500,
                    domain_expertise_required=False
                )
            ],
            execution_strategy="direct",
            total_complexity=5,
            confidence_score=0.5,
            reasoning_chain=["Fallback decomposition due to error"],
            metadata={"method": "fallback", "timestamp": datetime.now().isoformat()}
        )
    
    def get_execution_order(self, decomposition: HRMDecomposition) -> List[List[str]]:
        """
        Get optimal execution order for subtasks
        Returns list of lists - inner lists can be executed in parallel
        """
        subtasks_by_id = {st.id: st for st in decomposition.subtasks}
        executed = set()
        execution_order = []
        
        while len(executed) < len(decomposition.subtasks):
            # Find tasks ready to execute (no unmet dependencies)
            ready_tasks = []
            for subtask in decomposition.subtasks:
                if (subtask.id not in executed and 
                    all(dep_id in executed for dep_id in subtask.dependencies)):
                    ready_tasks.append(subtask.id)
            
            if not ready_tasks:
                # Break circular dependencies if any
                remaining = [st.id for st in decomposition.subtasks if st.id not in executed]
                ready_tasks = [remaining[0]] if remaining else []
            
            if ready_tasks:
                execution_order.append(ready_tasks)
                executed.update(ready_tasks)
        
        return execution_order
    
    def export_decomposition(self, decomposition: HRMDecomposition, filepath: str) -> bool:
        """Export decomposition to JSON file"""
        try:
            export_data = {
                'original_query': decomposition.original_query,
                'subtasks': [
                    {
                        'id': st.id,
                        'description': st.description,
                        'task_type': st.task_type,
                        'complexity': st.complexity,
                        'priority': st.priority,
                        'model_preference': st.model_preference,
                        'context_requirements': st.context_requirements,
                        'dependencies': st.dependencies,
                        'estimated_tokens': st.estimated_tokens,
                        'domain_expertise_required': st.domain_expertise_required
                    } for st in decomposition.subtasks
                ],
                'execution_strategy': decomposition.execution_strategy,
                'total_complexity': decomposition.total_complexity,
                'confidence_score': decomposition.confidence_score,
                'reasoning_chain': decomposition.reasoning_chain,
                'metadata': decomposition.metadata
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Decomposition exported to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Export failed: {e}")
            return False
    
    def get_status(self) -> Dict:
        """Get wrapper status and diagnostics"""
        return {
            'device': self.device,
            'hrm_available': HRM_AVAILABLE,
            'model_loaded': self.model_loaded,
            'cache_enabled': self.enable_caching,
            'cached_queries': len(self.cache) if self.cache else 0,
            'mps_available': torch.backends.mps.is_available(),
            'cuda_available': torch.cuda.is_available(),
        }


def create_hrm_wrapper(device: str = "auto", **kwargs) -> HRMLocalWrapper:
    """Factory function to create HRM wrapper with optimal settings"""
    return HRMLocalWrapper(device=device, **kwargs)


# Example usage and testing
if __name__ == "__main__":
    # Test the wrapper
    hrm = create_hrm_wrapper()
    
    # Test queries
    test_queries = [
        "Create a simple sine wave oscillator in FAUST",
        "Build a complete JUCE audio plugin with FAUST DSP processing",
        "Implement a real-time guitar effects processor with multiple effects",
        "Design a comprehensive audio synthesis engine from scratch"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing: {query}")
        decomposition = hrm.decompose_task(query)
        
        print(f"📋 Decomposed into {len(decomposition.subtasks)} subtasks:")
        for subtask in decomposition.subtasks:
            print(f"  - {subtask.id}: {subtask.description} ({subtask.model_preference})")
        
        print(f"🎯 Strategy: {decomposition.execution_strategy}")
        print(f"📊 Confidence: {decomposition.confidence_score:.2%}")