"""
Simple agent example demonstrating basic usage.
"""
from src.agents import ResearchAgent
from src.utils import setup_logging

# Setup logging
setup_logging()


def main():
    """Run a simple agent example."""
    
    # Create a research agent
    agent = ResearchAgent(
        name="SimpleResearcher",
        model="llama3.1:8b",
        system_prompt="You are a helpful research assistant.",
        temperature=0.7
    )
    
    # Define a task
    task = "Explain the concept of multi-agent systems and their applications in AI"
    
    print(f"\n{'='*80}")
    print(f"Task: {task}")
    print(f"{'='*80}\n")
    
    # Execute the task
    result = agent.execute(task)
    
    # Display results
    if result.success:
        print("✅ Task completed successfully!\n")
        print("Findings:")
        print("-" * 80)
        print(result.result.get('findings', 'No findings'))
        print("\n" + "="*80)
        print(f"Execution time: {result.execution_time:.2f}s")
    else:
        print("❌ Task failed!")
        print(f"Error: {result.error}")


if __name__ == "__main__":
    main()
