"""
Business intelligence analysis pipeline.
Multi-agent system for analyzing business data and generating insights.
"""
from src.agents import AnalystAgent, WriterAgent, ResearchAgent
from src.orchestration import AgentOrchestrator
from src.utils import setup_logging

# Setup logging
setup_logging()


# Sample business data
BUSINESS_DATA = """
Q3 2024 Sales Report:
- Total Revenue: $2.5M (up 15% from Q2)
- Customer Acquisition: 1,200 new customers (up 8%)
- Churn Rate: 5% (down from 7%)
- Average Order Value: $450 (up 12%)
- Top Products: Product A (35%), Product B (28%), Product C (20%)
- Regional Performance:
  * North America: $1.2M (48%)
  * Europe: $800K (32%)
  * Asia: $500K (20%)
- Customer Satisfaction Score: 4.3/5 (up from 4.1)
- Marketing ROI: 3.2x (improved from 2.8x)

Challenges:
- Increased competition in North American market
- Supply chain delays affecting Product A
- Customer support response time increased to 24 hours
"""


def main():
    """Run business intelligence pipeline."""
    
    print("\n" + "="*80)
    print("Business Intelligence Analysis Pipeline")
    print("="*80 + "\n")
    
    # Create specialized agents
    data_analyst = AnalystAgent(
        name="DataAnalyst",
        model="llama3.1:8b",
        system_prompt="You are a business data analyst. Extract insights and identify trends from data.",
        temperature=0.2
    )
    
    market_researcher = ResearchAgent(
        name="MarketResearcher",
        model="llama3.1:8b",
        system_prompt="You are a market research specialist. Provide market context and competitive insights.",
        temperature=0.5
    )
    
    strategy_advisor = AnalystAgent(
        name="StrategyAdvisor",
        model="llama3.1:8b",
        system_prompt="You are a business strategy consultant. Provide strategic recommendations.",
        temperature=0.3
    )
    
    report_writer = WriterAgent(
        name="ReportWriter",
        model="llama3.1:8b",
        system_prompt="You are a business report writer. Create clear, executive-level reports.",
        temperature=0.6
    )
    
    # Create orchestrator
    agents = {
        "data_analyst": data_analyst,
        "market_researcher": market_researcher,
        "strategy_advisor": strategy_advisor,
        "report_writer": report_writer
    }
    
    orchestrator = AgentOrchestrator(agents)
    
    print("Business Data:")
    print("-" * 80)
    print(BUSINESS_DATA)
    print("-" * 80 + "\n")
    
    # Sequential analysis pipeline
    agent_sequence = ["data_analyst", "market_researcher", "strategy_advisor", "report_writer"]
    
    context = {
        "data": BUSINESS_DATA,
        "content_type": "executive_summary",
        "tone": "professional"
    }
    
    print("🚀 Starting sequential analysis pipeline...\n")
    
    # Execute sequential pipeline
    result = orchestrator.execute_sequential(
        task="Analyze Q3 2024 performance and provide strategic recommendations",
        agent_sequence=agent_sequence,
        context=context
    )
    
    # Display results
    if result.get("success"):
        print("\n✅ Analysis completed successfully!\n")
        print("="*80)
        
        results = result.get("results", {})
        
        for agent_name in agent_sequence:
            if agent_name in results:
                agent_result = results[agent_name]
                print(f"\n📊 {agent_name.replace('_', ' ').title()}:")
                print("-" * 80)
                
                if agent_result.success:
                    res = agent_result.result
                    
                    if isinstance(res, dict):
                        # Display based on result type
                        if "analysis" in res:
                            print(res["analysis"])
                        elif "findings" in res:
                            print(res["findings"])
                        elif "content" in res:
                            print(res["content"])
                        else:
                            print(res)
                    else:
                        print(res)
                    
                    print(f"\n⏱️  Time: {agent_result.execution_time:.2f}s")
                else:
                    print(f"❌ Error: {agent_result.error}")
        
        print("\n" + "="*80)
        
    else:
        print("❌ Pipeline failed!")


if __name__ == "__main__":
    main()
