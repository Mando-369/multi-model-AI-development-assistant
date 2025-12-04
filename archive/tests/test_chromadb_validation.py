#!/usr/bin/env python3
"""
ChromaDB Validation Test Suite
Tests the complete context enhancement and knowledge retrieval pipeline
"""

import sys
import os
import time
from typing import Dict, List, Tuple
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import ContextEnhancer, enhance_vectorstore_retrieval, MultiModelGLMSystem


class ChromaDBValidator:
    """Comprehensive ChromaDB validation suite"""
    
    def __init__(self):
        print("🚀 Initializing ChromaDB Validation Suite...")
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        
        # Initialize vectorstore
        self.vectorstore = Chroma(
            persist_directory="./chroma_db", 
            embedding_function=self.embeddings
        )
        
        # Initialize context enhancer
        self.context_enhancer = ContextEnhancer(self.vectorstore)
        
        # Initialize multi-model system
        self.system = MultiModelGLMSystem()
        
        # Test queries for different domains
        self.test_queries = {
            "faust_basic": "Create a simple lowpass filter in FAUST",
            "faust_advanced": "Implement a state-variable filter with resonance control using fi.svf",
            "juce_basic": "How do I create an AudioProcessor in JUCE?",
            "juce_advanced": "Implement parameter automation with AudioProcessorValueTreeState",
            "multi_domain": "How to integrate FAUST DSP code into a JUCE plugin",
            "complex_task": "Build a complete reverb plugin with FAUST processing and JUCE GUI",
            "general": "What are the best practices for real-time audio programming?"
        }
        
        self.test_results = {}
    
    def test_chromadb_connection(self) -> bool:
        """Test basic ChromaDB connectivity and document count"""
        print("\n📊 Testing ChromaDB Connection...")
        
        try:
            # Test similarity search
            test_results = self.vectorstore.similarity_search("audio", k=3)
            doc_count = len(test_results)
            
            print(f"✅ ChromaDB connected successfully")
            print(f"📚 Found {doc_count} documents in knowledge base")
            
            if doc_count > 0:
                print("📄 Sample document preview:")
                for i, doc in enumerate(test_results[:2]):
                    preview = doc.page_content[:100].replace('\n', ' ')
                    print(f"   {i+1}. {preview}...")
                return True
            else:
                print("⚠️ Knowledge base is empty - no documents found")
                return False
                
        except Exception as e:
            print(f"❌ ChromaDB connection failed: {e}")
            return False
    
    def test_context_enhancer_domain_detection(self) -> Dict[str, any]:
        """Test domain detection accuracy"""
        print("\n🎯 Testing Context Enhancer Domain Detection...")
        
        results = {}
        
        for test_name, query in self.test_queries.items():
            print(f"\n  Testing: {test_name}")
            print(f"  Query: {query}")
            
            try:
                # Test domain detection via system
                domain, confidence = self.system._detect_domain_patterns(query)
                complexity = self.system._estimate_complexity(query)
                
                # Test keyword extraction
                faust_keywords = self.context_enhancer._extract_faust_keywords(query)
                juce_keywords = self.context_enhancer._extract_juce_keywords(query)
                tech_terms = self.context_enhancer._extract_technical_terms(query)
                
                result = {
                    'domain': domain,
                    'confidence': confidence,
                    'complexity': complexity,
                    'faust_keywords': faust_keywords,
                    'juce_keywords': juce_keywords,
                    'technical_terms': tech_terms
                }
                
                results[test_name] = result
                
                print(f"    🎪 Domain: {domain} (confidence: {confidence:.2f})")
                print(f"    🔢 Complexity: {complexity:.2f}")
                print(f"    🔧 Keywords: FAUST={len(faust_keywords)}, JUCE={len(juce_keywords)}, Tech={len(tech_terms)}")
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
                results[test_name] = {'error': str(e)}
        
        return results
    
    def test_faust_knowledge_retrieval(self) -> Dict[str, any]:
        """Test FAUST-specific knowledge retrieval"""
        print("\n🎵 Testing FAUST Knowledge Retrieval...")
        
        faust_queries = [
            "os.osc oscillator FAUST",
            "fi.lowpass filter implementation", 
            "re.freeverb reverb algorithm",
            "de.delay echo effect"
        ]
        
        results = {}
        
        for query in faust_queries:
            print(f"\n  Query: {query}")
            
            try:
                # Test enhanced context retrieval
                context = self.context_enhancer.enhance_context_for_query(query, "faust", max_docs=5)
                
                result = {
                    'documents_found': len(context['documents']),
                    'function_references': context['function_references'],
                    'algorithm_templates': len(context['algorithm_templates']),
                    'search_terms': context.get('search_terms', []),
                    'domain_keywords': context.get('domain_keywords', [])
                }
                
                results[query] = result
                
                print(f"    📚 Documents: {result['documents_found']}")
                print(f"    🔧 Functions: {len(result['function_references'])}")
                print(f"    📐 Templates: {result['algorithm_templates']}")
                
                if result['function_references']:
                    print(f"    🎯 Found functions: {', '.join(result['function_references'][:3])}")
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
                results[query] = {'error': str(e)}
        
        return results
    
    def test_juce_knowledge_retrieval(self) -> Dict[str, any]:
        """Test JUCE-specific knowledge retrieval"""
        print("\n🎹 Testing JUCE Knowledge Retrieval...")
        
        juce_queries = [
            "AudioProcessor JUCE plugin",
            "AudioProcessorValueTreeState parameters",
            "Component GUI JUCE",
            "dsp::IIR::Filter JUCE"
        ]
        
        results = {}
        
        for query in juce_queries:
            print(f"\n  Query: {query}")
            
            try:
                context = self.context_enhancer.enhance_context_for_query(query, "juce", max_docs=5)
                
                result = {
                    'documents_found': len(context['documents']),
                    'class_references': context['function_references'],  # JUCE classes
                    'integration_patterns': len(context['integration_patterns']),
                    'domain_keywords': context.get('domain_keywords', [])
                }
                
                results[query] = result
                
                print(f"    📚 Documents: {result['documents_found']}")
                print(f"    🏗️ Classes: {len(result['class_references'])}")
                print(f"    🔗 Patterns: {result['integration_patterns']}")
                
                if result['class_references']:
                    print(f"    🎯 Found classes: {', '.join(result['class_references'][:3])}")
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
                results[query] = {'error': str(e)}
        
        return results
    
    def test_enhanced_vectorstore_retrieval(self) -> Dict[str, any]:
        """Test the integrated enhanced retrieval function"""
        print("\n🔍 Testing Enhanced Vectorstore Retrieval...")
        
        test_cases = [
            ("Create FAUST reverb", "faust"),
            ("JUCE AudioProcessor setup", "juce"), 
            ("Real-time audio optimization", "general")
        ]
        
        results = {}
        
        for query, task_type in test_cases:
            print(f"\n  Query: {query} (type: {task_type})")
            
            try:
                start_time = time.time()
                enhanced_context = enhance_vectorstore_retrieval(
                    self.vectorstore, query, task_type
                )
                retrieval_time = time.time() - start_time
                
                result = {
                    'context_length': len(enhanced_context),
                    'retrieval_time': retrieval_time,
                    'has_documentation': '=== RELEVANT DOCUMENTATION ===' in enhanced_context,
                    'has_functions': '=== RELEVANT FUNCTIONS ===' in enhanced_context,
                    'has_templates': '=== ALGORITHM TEMPLATES ===' in enhanced_context,
                    'has_patterns': '=== INTEGRATION PATTERNS ===' in enhanced_context
                }
                
                results[f"{query}_{task_type}"] = result
                
                print(f"    📏 Context length: {result['context_length']} chars")
                print(f"    ⏱️ Retrieval time: {retrieval_time:.3f}s")
                print(f"    📚 Sections: Doc={result['has_documentation']}, Func={result['has_functions']}, Template={result['has_templates']}, Pattern={result['has_patterns']}")
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
                results[f"{query}_{task_type}"] = {'error': str(e)}
        
        return results
    
    def test_model_routing_patterns(self) -> Dict[str, any]:
        """Test multi-model routing pattern detection"""
        print("\n🧠 Testing Model Routing Patterns...")
        
        results = {}
        
        for test_name, query in self.test_queries.items():
            print(f"\n  Testing: {test_name}")
            
            try:
                # Test routing suggestion
                suggestion = self.system.get_routing_suggestion(query, "auto")
                
                result = {
                    'recommended_model': suggestion['recommended_model'],
                    'confidence': suggestion['confidence'],
                    'complexity': suggestion['complexity'],
                    'domain': suggestion['domain'],
                    'reason': suggestion['reason']
                }
                
                results[test_name] = result
                
                print(f"    🤖 Recommended: {result['recommended_model']}")
                print(f"    🎯 Domain: {result['domain']} (confidence: {result['confidence']:.2f})")
                print(f"    🔢 Complexity: {result['complexity']:.2f}")
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
                results[test_name] = {'error': str(e)}
        
        return results
    
    def test_hrm_decomposition(self) -> Dict[str, any]:
        """Test HRM task decomposition"""
        print("\n🧩 Testing HRM Task Decomposition...")
        
        complex_queries = [
            "Build a complete FAUST reverb with early reflections and late reverberation",
            "Create a JUCE plugin with FAUST processing and parameter automation"
        ]
        
        results = {}
        
        for query in complex_queries:
            print(f"\n  Query: {query}")
            
            try:
                # Test HRM analysis
                hrm_analysis = self.system._analyze_with_hrm(query, "")
                
                result = {
                    'complexity_score': hrm_analysis.get('complexity_score', 0),
                    'domain': hrm_analysis.get('domain', 'unknown'),
                    'recommended_model': hrm_analysis.get('recommended_model', 'unknown'),
                    'subtask_count': hrm_analysis.get('subtask_count', 0),
                    'confidence': hrm_analysis.get('confidence_score', 0)
                }
                
                results[query] = result
                
                print(f"    🔢 Complexity: {result['complexity_score']:.2f}")
                print(f"    🎪 Domain: {result['domain']}")
                print(f"    🤖 Model: {result['recommended_model']}")
                print(f"    🧩 Subtasks: {result['subtask_count']}")
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
                results[query] = {'error': str(e)}
        
        return results
    
    def run_comprehensive_validation(self) -> Dict[str, any]:
        """Run all validation tests"""
        print("=" * 60)
        print("🧪 CHROMADB VALIDATION SUITE")
        print("=" * 60)
        
        validation_results = {}
        
        # Test 1: ChromaDB Connection
        validation_results['chromadb_connection'] = self.test_chromadb_connection()
        
        # Test 2: Domain Detection  
        validation_results['domain_detection'] = self.test_context_enhancer_domain_detection()
        
        # Test 3: FAUST Knowledge
        validation_results['faust_knowledge'] = self.test_faust_knowledge_retrieval()
        
        # Test 4: JUCE Knowledge
        validation_results['juce_knowledge'] = self.test_juce_knowledge_retrieval()
        
        # Test 5: Enhanced Retrieval
        validation_results['enhanced_retrieval'] = self.test_enhanced_vectorstore_retrieval()
        
        # Test 6: Model Routing
        validation_results['model_routing'] = self.test_model_routing_patterns()
        
        # Test 7: HRM Decomposition
        validation_results['hrm_decomposition'] = self.test_hrm_decomposition()
        
        return validation_results
    
    def generate_validation_report(self, results: Dict[str, any]) -> str:
        """Generate comprehensive validation report"""
        report_lines = [
            "=" * 80,
            "📋 CHROMADB VALIDATION REPORT",
            "=" * 80,
            ""
        ]
        
        # Summary
        total_tests = 0
        passed_tests = 0
        
        for test_category, test_results in results.items():
            if isinstance(test_results, bool):
                total_tests += 1
                if test_results:
                    passed_tests += 1
            elif isinstance(test_results, dict):
                for test_name, test_result in test_results.items():
                    total_tests += 1
                    if isinstance(test_result, dict) and 'error' not in test_result:
                        passed_tests += 1
        
        report_lines.extend([
            f"🎯 OVERALL RESULTS: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)",
            ""
        ])
        
        # Detailed results
        for test_category, test_results in results.items():
            report_lines.extend([
                f"📊 {test_category.upper().replace('_', ' ')}:",
                "-" * 40
            ])
            
            if isinstance(test_results, bool):
                status = "✅ PASSED" if test_results else "❌ FAILED"
                report_lines.append(f"  Status: {status}")
            elif isinstance(test_results, dict):
                for test_name, test_result in test_results.items():
                    if isinstance(test_result, dict):
                        if 'error' in test_result:
                            report_lines.append(f"  ❌ {test_name}: {test_result['error']}")
                        else:
                            report_lines.append(f"  ✅ {test_name}: Success")
                            # Add key metrics
                            for key, value in test_result.items():
                                if key in ['domain', 'recommended_model', 'complexity_score', 'documents_found']:
                                    report_lines.append(f"     {key}: {value}")
            
            report_lines.append("")
        
        # Recommendations
        report_lines.extend([
            "🔧 RECOMMENDATIONS:",
            "-" * 40
        ])
        
        if not results.get('chromadb_connection', False):
            report_lines.append("  - ChromaDB connection failed - check database initialization")
        
        domain_results = results.get('domain_detection', {})
        if any('error' in str(result) for result in domain_results.values()):
            report_lines.append("  - Domain detection has errors - check pattern matching logic")
        
        if results.get('enhanced_retrieval', {}):
            retrieval_errors = sum(1 for result in results['enhanced_retrieval'].values() 
                                 if isinstance(result, dict) and 'error' in result)
            if retrieval_errors > 0:
                report_lines.append(f"  - Enhanced retrieval has {retrieval_errors} errors - check vectorstore integration")
        
        report_lines.extend([
            "",
            "=" * 80,
            f"Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 80
        ])
        
        return "\n".join(report_lines)


def main():
    """Run ChromaDB validation suite"""
    validator = ChromaDBValidator()
    
    try:
        # Run comprehensive validation
        results = validator.run_comprehensive_validation()
        
        # Generate report
        report = validator.generate_validation_report(results)
        
        # Display report
        print(report)
        
        # Save report to file
        report_file = f"chromadb_validation_report_{int(time.time())}.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"\n💾 Full report saved to: {report_file}")
        
        return results
        
    except Exception as e:
        print(f"❌ Validation suite failed: {e}")
        return None


if __name__ == "__main__":
    main()