"""
Code review and refactoring pipeline.
Demonstrates multi-agent collaboration for code analysis.
"""
import asyncio
from src.agents import CoderAgent, AnalystAgent
from src.orchestration import AgentOrchestrator
from src.tools import PythonExecutorTool
from src.utils import setup_logging

# Setup logging
setup_logging()


# Sample code to analyze
SAMPLE_CODE = '''
def calculate_total(items):
    total = 0
    for item in items:
        total = total + item["price"] * item["quantity"]
    return total

def get_discount(total):
    if total > 100:
        discount = 0.1
    elif total > 50:
        discount = 0.05
    else:
        discount = 0
    return total * discount

def process_order(items):
    total = calculate_total(items)
    discount = get_discount(total)
    final = total - discount
    return final
'''


async def main():
    """Run code review pipeline."""
    
    print("\n" + "="*80)
    print("Code Review & Refactoring Pipeline")
    print("="*80 + "\n")
    
    # Create specialized agents
    code_analyzer = CoderAgent(
        name="CodeAnalyzer",
        model="codellama:13b",
        system_prompt="You are an expert code reviewer. Analyze code for quality, bugs, and improvements.",
        temperature=0.1,
        tools=[PythonExecutorTool()]
    )
    
    security_analyst = AnalystAgent(
        name="SecurityAnalyst",
        model="llama3.1:8b",
        system_prompt="You are a security expert. Identify security vulnerabilities and best practices violations.",
        temperature=0.2
    )
    
    performance_analyst = AnalystAgent(
        name="PerformanceAnalyst",
        model="llama3.1:8b",
        system_prompt="You are a performance optimization expert. Identify bottlenecks and suggest improvements.",
        temperature=0.2
    )
    
    # Create orchestrator
    agents = {
        "analyzer": code_analyzer,
        "security": security_analyst,
        "performance": performance_analyst
    }
    
    orchestrator = AgentOrchestrator(agents)
    
    print("Code to Review:")
    print("-" * 80)
    print(SAMPLE_CODE)
    print("-" * 80 + "\n")
    
    # Define parallel analysis tasks
    tasks = [
        {
            "agent": "analyzer",
            "task": "Review this code for bugs, code quality, and suggest improvements",
            "context": {"code": SAMPLE_CODE, "language": "python"}
        },
        {
            "agent": "security",
            "task": "Analyze this code for security vulnerabilities",
            "context": {"data": SAMPLE_CODE}
        },
        {
            "agent": "performance",
            "task": "Analyze this code for performance issues and optimization opportunities",
            "context": {"data": SAMPLE_CODE}
        }
    ]
    
    print("🚀 Starting parallel analysis...\n")
    
    # Execute parallel analysis
    results = await orchestrator.execute_parallel(tasks, max_concurrent=3)
    
    # Display results
    print("\n" + "="*80)
    print("Analysis Results")
    print("="*80 + "\n")
    
    for result in results:
        if result and result.success:
            print(f"\n📊 {result.agent_name}:")
            print("-" * 80)
            
            if isinstance(result.result, dict):
                if "analysis" in result.result:
                    print(result.result["analysis"])
                elif "code" in result.result:
                    print("Generated Code:")
                    print(result.result["code"])
            else:
                print(result.result)
            
            print(f"\n⏱️  Execution time: {result.execution_time:.2f}s")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    asyncio.run(main())
