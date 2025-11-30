"""
Streamlit app for multi-agent system visualization.
"""
import streamlit as st
import time
from typing import Dict, Any

from src.agents import ResearchAgent, AnalystAgent, CoderAgent, WriterAgent, PlannerAgent
from src.orchestration import AgentOrchestrator
from src.utils import setup_logging, format_execution_time

# Setup
setup_logging()
st.set_page_config(
    page_title="Multi-Agent System",
    page_icon="🤖",
    layout="wide"
)


# Initialize session state
if "orchestrator" not in st.session_state:
    # Create agents
    agents = {
        "planner": PlannerAgent(
            name="Planner",
            model="llama3.1:8b",
            system_prompt="You are a task planning expert.",
            temperature=0.3
        ),
        "researcher": ResearchAgent(
            name="Researcher",
            model="llama3.1:8b",
            system_prompt="You are a research specialist.",
            temperature=0.5
        ),
        "analyst": AnalystAgent(
            name="Analyst",
            model="llama3.1:8b",
            system_prompt="You are a data analyst.",
            temperature=0.2
        ),
        "coder": CoderAgent(
            name="Coder",
            model="codellama:13b",
            system_prompt="You are a coding expert.",
            temperature=0.1
        ),
        "writer": WriterAgent(
            name="Writer",
            model="llama3.1:8b",
            system_prompt="You are a content writer.",
            temperature=0.7
        )
    }
    
    st.session_state.orchestrator = AgentOrchestrator(agents)
    st.session_state.task_history = []


# Header
st.title("🤖 Multi-Agent System Dashboard")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Execution mode
    execution_mode = st.selectbox(
        "Execution Mode",
        ["Hierarchical", "Sequential", "Single Agent"]
    )
    
    # Agent selection
    available_agents = st.session_state.orchestrator.list_agents()
    
    if execution_mode == "Single Agent":
        selected_agent = st.selectbox("Select Agent", available_agents)
    elif execution_mode == "Sequential":
        selected_agents = st.multiselect(
            "Select Agents (in order)",
            available_agents,
            default=["researcher", "analyst"]
        )
    
    st.markdown("---")
    
    # System info
    st.subheader("📊 System Info")
    st.info(f"Active Agents: {len(available_agents)}")
    st.info(f"Tasks Executed: {len(st.session_state.task_history)}")
    
    if st.button("Clear History"):
        st.session_state.task_history = []
        st.session_state.orchestrator.clear_history()
        st.rerun()


# Main area
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📈 Analytics", "🔧 Tools"])

with tab1:
    st.header("Agent Task Execution")
    
    # Task input
    task = st.text_area(
        "Enter your task:",
        height=100,
        placeholder="Describe what you want the agents to do..."
    )
    
    # Context input (optional)
    with st.expander("Advanced Options"):
        context_input = st.text_area(
            "Additional Context (JSON format, optional):",
            height=100,
            placeholder='{"key": "value"}'
        )
    
    # Execute button
    col1, col2 = st.columns([1, 4])
    with col1:
        execute_button = st.button("🚀 Execute", type="primary", use_container_width=True)
    
    # Execute task
    if execute_button and task:
        with st.spinner("Agents are working..."):
            start_time = time.time()
            
            # Parse context
            context = {}
            if context_input:
                try:
                    import json
                    context = json.loads(context_input)
                except:
                    st.warning("Invalid JSON in context, using empty context")
            
            # Execute based on mode
            try:
                if execution_mode == "Hierarchical":
                    result = st.session_state.orchestrator.execute_hierarchical(
                        task=task,
                        context=context
                    )
                    
                    # Display results
                    st.success("✅ Task completed!")
                    
                    # Show plan
                    if "plan" in result:
                        with st.expander("📋 Execution Plan", expanded=True):
                            st.write(result["plan"].get("plan", ""))
                    
                    # Show steps
                    if "step_results" in result:
                        st.subheader("Step Results:")
                        for idx, step_result in enumerate(result["step_results"], 1):
                            step = step_result.get("step", {})
                            res = step_result.get("result", {})
                            
                            with st.expander(f"Step {idx}: {step.get('description', 'N/A')}", expanded=True):
                                st.write(f"**Agent:** {step.get('agent', 'N/A')}")
                                st.write(f"**Status:** {'✅ Success' if res.get('success') else '❌ Failed'}")
                                
                                if res.get('success'):
                                    result_data = res.get('result', {})
                                    if isinstance(result_data, dict):
                                        for key, value in result_data.items():
                                            st.write(f"**{key.title()}:**")
                                            st.write(value)
                                    else:
                                        st.write(result_data)
                
                elif execution_mode == "Sequential":
                    if not selected_agents:
                        st.error("Please select at least one agent")
                    else:
                        result = st.session_state.orchestrator.execute_sequential(
                            task=task,
                            agent_sequence=selected_agents,
                            context=context
                        )
                        
                        # Display results
                        st.success("✅ Task completed!")
                        
                        for agent_name in selected_agents:
                            if agent_name in result.get("results", {}):
                                agent_result = result["results"][agent_name]
                                
                                with st.expander(f"🤖 {agent_name.title()}", expanded=True):
                                    if agent_result.success:
                                        st.write(agent_result.result)
                                        st.caption(f"Time: {format_execution_time(agent_result.execution_time)}")
                                    else:
                                        st.error(f"Error: {agent_result.error}")
                
                else:  # Single Agent
                    agent = st.session_state.orchestrator.get_agent(selected_agent)
                    result = agent.execute(task, context)
                    
                    # Display result
                    if result.success:
                        st.success("✅ Task completed!")
                        with st.expander("Result", expanded=True):
                            st.write(result.result)
                            st.caption(f"Time: {format_execution_time(result.execution_time)}")
                    else:
                        st.error(f"❌ Task failed: {result.error}")
                
                # Add to history
                execution_time = time.time() - start_time
                st.session_state.task_history.append({
                    "task": task,
                    "mode": execution_mode,
                    "time": execution_time,
                    "timestamp": time.time()
                })
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                import traceback
                with st.expander("Error Details"):
                    st.code(traceback.format_exc())

with tab2:
    st.header("📈 Analytics & History")
    
    if st.session_state.task_history:
        st.subheader("Task History")
        
        for idx, task_info in enumerate(reversed(st.session_state.task_history[-10:]), 1):
            with st.expander(f"Task {len(st.session_state.task_history) - idx + 1}"):
                st.write(f"**Task:** {task_info['task'][:100]}...")
                st.write(f"**Mode:** {task_info['mode']}")
                st.write(f"**Execution Time:** {format_execution_time(task_info['time'])}")
                st.write(f"**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(task_info['timestamp']))}")
        
        # Statistics
        st.subheader("Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Tasks", len(st.session_state.task_history))
        
        with col2:
            avg_time = sum(t['time'] for t in st.session_state.task_history) / len(st.session_state.task_history)
            st.metric("Avg. Time", format_execution_time(avg_time))
        
        with col3:
            total_time = sum(t['time'] for t in st.session_state.task_history)
            st.metric("Total Time", format_execution_time(total_time))
    else:
        st.info("No tasks executed yet. Start by executing a task in the Chat tab!")

with tab3:
    st.header("🔧 Agent Management")
    
    # Display agents
    for agent_name in st.session_state.orchestrator.list_agents():
        agent = st.session_state.orchestrator.get_agent(agent_name)
        
        with st.expander(f"🤖 {agent_name.title()}"):
            st.write(f"**Name:** {agent.name}")
            st.write(f"**Model:** {agent.llm.model}")
            st.write(f"**Temperature:** {agent.llm.temperature}")
            st.write(f"**Tools:** {len(agent.tools)}")
            st.write(f"**System Prompt:**")
            st.text_area("", agent.system_prompt, height=100, key=f"prompt_{agent_name}", disabled=True)
