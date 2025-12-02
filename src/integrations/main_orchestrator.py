import ollama
from chromadb import Client
from .hrm_integration import HRMOrchestrator


class UnifiedCodingAssistant:
    def __init__(self):
        # HRM for hierarchical reasoning
        self.hrm = HRMOrchestrator()

        # Models via Ollama
        self.deepseek_r1 = "deepseek-r1:70b"
        self.qwen_coder = "qwen2.5-coder:32b"
        self.qwen_math = "qwen2.5:32b"

        # Knowledge base
        self.chromadb = Client()
        self.faust_collection = self.chromadb.get_collection("faust_docs")
        self.juce_collection = self.chromadb.get_collection("juce_docs")

    async def process_request(self, user_request):
        # Step 1: Analyze with Claude Code agent
        analysis = await self.analyze_requirements(user_request)

        # Step 2: HRM hierarchical planning
        plan = self.hrm.decompose_task(analysis)

        # Step 3: Route to specialized models
        results = await self.execute_plan(plan)

        # Step 4: Validate and test
        validated = await self.validate_results(results)

        return validated

    async def execute_plan(self, plan):
        results = []
        for subtask in plan.subtasks:
            if subtask.requires_deep_reasoning:
                # Use DeepSeek-R1 for reasoning
                result = ollama.generate(model=self.deepseek_r1, prompt=subtask.prompt)
            elif subtask.is_faust_code:
                # Use Qwen2.5-Coder with FAUST context
                context = self.faust_collection.query(subtask.query)
                result = ollama.generate(
                    model=self.qwen_coder, prompt=f"{context}\n{subtask.prompt}"
                )
            else:
                # Use Qwen2.5-Coder for general coding
                result = ollama.generate(model=self.qwen_coder, prompt=subtask.prompt)
            results.append(result)
        return results
