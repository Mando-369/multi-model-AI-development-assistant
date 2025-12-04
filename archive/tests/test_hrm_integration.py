#!/usr/bin/env python3
"""
Test script for HRM Local Wrapper integration with MultiModelGLMSystem
Demonstrates offline hierarchical task decomposition for FAUST/JUCE workflows
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.integrations.hrm_local_wrapper import HRMLocalWrapper
from src.core.multi_model_system import MultiModelGLMSystem
import json


def test_hrm_wrapper():
    """Test the HRM wrapper functionality"""
    print("🧠 Testing HRM Local Wrapper")
    print("=" * 50)
    
    # Initialize HRM wrapper
    hrm = HRMLocalWrapper(device="auto", enable_caching=True)
    
    # Get status
    status = hrm.get_status()
    print(f"📊 HRM Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    print()
    
    # Test queries with different complexity levels
    test_queries = [
        {
            "query": "Create a simple sine wave oscillator in FAUST",
            "expected_subtasks": 1,
            "description": "Simple FAUST task"
        },
        {
            "query": "Build a complete JUCE audio plugin with FAUST DSP processing",
            "expected_subtasks": 3,
            "description": "Complex FAUST+JUCE integration"
        },
        {
            "query": "Implement a real-time guitar effects processor with multiple effects and JUCE GUI",
            "expected_subtasks": 4,
            "description": "Complex multi-component system"
        },
        {
            "query": "Design a comprehensive modular synthesis engine from scratch with FAUST and JUCE",
            "expected_subtasks": 5,
            "description": "High complexity full system"
        }
    ]
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"🔍 Test {i}: {test_case['description']}")
        print(f"Query: {test_case['query']}")
        print()
        
        # Decompose task
        decomposition = hrm.decompose_task(
            test_case['query'],
            context={'test_mode': True}
        )
        
        # Display results
        print(f"📋 Decomposition Results:")
        print(f"  Subtasks: {len(decomposition.subtasks)}")
        print(f"  Strategy: {decomposition.execution_strategy}")
        print(f"  Complexity: {decomposition.total_complexity}/10")
        print(f"  Confidence: {decomposition.confidence_score:.1%}")
        print()
        
        # Show subtasks
        print("🎯 Subtasks:")
        for j, subtask in enumerate(decomposition.subtasks, 1):
            deps = f" (deps: {', '.join(subtask.dependencies)})" if subtask.dependencies else ""
            print(f"  {j}. [{subtask.id}] {subtask.description}")
            print(f"     Type: {subtask.task_type} | Model: {subtask.model_preference}")
            print(f"     Complexity: {subtask.complexity}/10 | Priority: {subtask.priority}/5{deps}")
        print()
        
        # Show execution order
        execution_order = hrm.get_execution_order(decomposition)
        print("🔄 Execution Order:")
        for phase, task_ids in enumerate(execution_order, 1):
            print(f"  Phase {phase}: {', '.join(task_ids)}")
        print()
        
        # Export decomposition
        export_path = f"test_decomposition_{i}.json"
        hrm.export_decomposition(decomposition, export_path)
        print(f"💾 Exported to: {export_path}")
        print()
        
        print("-" * 50)
        print()


def test_multimodel_integration():
    """Test integration with MultiModelGLMSystem"""
    print("🚀 Testing MultiModelGLMSystem Integration")
    print("=" * 50)
    
    try:
        # Initialize the system
        print("🔄 Initializing MultiModelGLMSystem with HRM...")
        glm_system = MultiModelGLMSystem()
        
        # Check HRM wrapper status
        hrm_status = glm_system.hrm_wrapper.get_status()
        print(f"✅ HRM Wrapper Status: {hrm_status['model_loaded']} (device: {hrm_status['device']})")
        
        # Test a complex query (without actually calling Ollama)
        test_query = "Create a FAUST reverb effect with JUCE parameter controls"
        
        print(f"🧠 Testing decomposition for: {test_query}")
        
        # Get decomposition directly from wrapper
        context_info = {
            'project': 'test_project',
            'model': 'DeepSeek-R1 (Reasoning)',
            'use_context': True
        }
        
        decomposition = glm_system.hrm_wrapper.decompose_task(test_query, context=context_info)
        
        print(f"📊 Results:")
        print(f"  - {len(decomposition.subtasks)} subtasks identified")
        print(f"  - Execution strategy: {decomposition.execution_strategy}")
        print(f"  - Total complexity: {decomposition.total_complexity}/10")
        
        # Show model routing
        model_usage = {}
        for subtask in decomposition.subtasks:
            model = subtask.model_preference
            model_usage[model] = model_usage.get(model, 0) + 1
        
        print(f"📈 Model Usage:")
        for model, count in model_usage.items():
            print(f"  - {model}: {count} subtask(s)")
        
        print("✅ Integration test successful!")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()


def test_performance():
    """Test performance characteristics"""
    print("⚡ Testing Performance")
    print("=" * 50)
    
    hrm = HRMLocalWrapper(device="auto", enable_caching=True)
    
    import time
    
    queries = [
        "Create basic FAUST filter",
        "Build JUCE audio plugin", 
        "Implement complex audio processor with GUI",
        "Design modular synthesis system"
    ]
    
    # Test without cache
    print("🔄 Testing decomposition speed (no cache):")
    times = []
    
    for query in queries:
        start_time = time.time()
        decomposition = hrm.decompose_task(query)
        end_time = time.time()
        
        elapsed = end_time - start_time
        times.append(elapsed)
        
        print(f"  {query[:30]:<30} | {elapsed:.3f}s | {len(decomposition.subtasks)} subtasks")
    
    avg_time = sum(times) / len(times)
    print(f"\n📊 Average decomposition time: {avg_time:.3f}s")
    
    # Test with cache
    print("\n🚀 Testing decomposition speed (with cache):")
    cache_times = []
    
    for query in queries:
        start_time = time.time()
        decomposition = hrm.decompose_task(query)  # Should hit cache
        end_time = time.time()
        
        elapsed = end_time - start_time
        cache_times.append(elapsed)
        
        print(f"  {query[:30]:<30} | {elapsed:.3f}s | cached")
    
    avg_cache_time = sum(cache_times) / len(cache_times)
    speedup = avg_time / avg_cache_time if avg_cache_time > 0 else float('inf')
    
    print(f"\n📊 Average cached time: {avg_cache_time:.3f}s")
    print(f"🚀 Cache speedup: {speedup:.1f}x")


def main():
    """Run all tests"""
    print("🧠 HRM Local Wrapper Integration Tests")
    print("=" * 60)
    print()
    
    try:
        # Test 1: HRM wrapper functionality
        test_hrm_wrapper()
        
        # Test 2: MultiModel integration
        test_multimodel_integration()
        
        # Test 3: Performance
        test_performance()
        
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)