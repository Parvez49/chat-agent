"""
Multi-agent research pipeline example.
Demonstrates hierarchical coordination of multiple specialized agents.
"""
from src.agents import ResearchAgent, AnalystAgent, WriterAgent, PlannerAgent
from src.orchestration import AgentOrchestrator
from src.utils import setup_logging

# Setup logging
setup_logging()


def main():
    """Run a multi-agent research pipeline."""
    
    print("\n" + "="*80)
    print("Multi-Agent Research Pipeline")
    print("="*80 + "\n")
    
    # Create specialized agents
    planner = PlannerAgent(
        name="TaskPlanner",
        model="llama3.1:8b",
        system_prompt="You are an expert task planner. Break down complex tasks into actionable steps.",
        temperature=0.3
    )
    
    researcher = ResearchAgent(
        name="ResearchSpecialist",
        model="llama3.1:8b",
        system_prompt="You are a thorough researcher. Gather comprehensive information.",
        temperature=0.5
    )
    
    analyst = AnalystAgent(
        name="DataAnalyst",
        model="llama3.1:8b",
        system_prompt="You are a critical analyst. Evaluate information and extract insights.",
        temperature=0.2
    )
    
    writer = WriterAgent(
        name="ContentWriter",
        model="llama3.1:8b",
        system_prompt="You are a skilled writer. Create clear, engaging content.",
        temperature=0.7
    )
    
    # Create orchestrator
    agents = {
        "planner": planner,
        "researcher": researcher,
        "analyst": analyst,
        "writer": writer
    }
    
    orchestrator = AgentOrchestrator(agents)
    
    # Define complex task
    task = """
    Research the impact of Large Language Models on software development.
    Analyze current trends, benefits, and challenges.
    Create a comprehensive report with recommendations.
    """
    
    print(f"Task: {task.strip()}\n")
    print("-" * 80 + "\n")
    
    # Execute using hierarchical orchestration
    print("🚀 Starting hierarchical execution...\n")
    
    result = orchestrator.execute_hierarchical(
        task=task,
        planner_agent="planner"
    )
    
    # Display results
    if result.get("success"):
        print("\n✅ Pipeline completed successfully!\n")
        print("="*80)
        
        # Show plan
        plan = result.get("plan", {})
        print(f"\n📋 Execution Plan:")
        print("-" * 80)
        print(plan.get("plan", "No plan details"))
        
        # Show step results
        step_results = result.get("step_results", [])
        print(f"\n📊 Execution Results ({len(step_results)} steps):")
        print("-" * 80)
        
        for idx, step_result in enumerate(step_results, 1):
            step = step_result.get("step", {})
            res = step_result.get("result", {})
            
            print(f"\nStep {idx}: {step.get('description', 'N/A')}")
            print(f"Agent: {step.get('agent', 'N/A')}")
            print(f"Status: {'✅ Success' if res.get('success') else '❌ Failed'}")
            print(f"Time: {res.get('execution_time', 0):.2f}s")
        
        print("\n" + "="*80)
        
    else:
        print("❌ Pipeline failed!")
        print(f"Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
