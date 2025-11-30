"""
Multi-agent orchestration system.
"""
import asyncio
from typing import List, Dict, Any, Optional
from loguru import logger

from src.agents import BaseAgent, PlannerAgent
from src.core import TaskResult


class AgentOrchestrator:
    """Orchestrates multiple agents to solve complex tasks."""
    
    def __init__(self, agents: Dict[str, BaseAgent]):
        """
        Initialize orchestrator with a dictionary of agents.
        
        Args:
            agents: Dictionary mapping agent names to agent instances
        """
        self.agents = agents
        self.task_history: List[Dict[str, Any]] = []
    
    def execute_sequential(
        self,
        task: str,
        agent_sequence: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute task sequentially through multiple agents.
        
        Args:
            task: The task to execute
            agent_sequence: List of agent names in order
            context: Optional context to pass to agents
        
        Returns:
            Dictionary containing results from all agents
        """
        logger.info(f"Starting sequential execution: {agent_sequence}")
        
        results = {}
        current_context = context or {}
        
        for agent_name in agent_sequence:
            if agent_name not in self.agents:
                logger.error(f"Agent {agent_name} not found")
                continue
            
            agent = self.agents[agent_name]
            logger.info(f"Executing with agent: {agent_name}")
            
            # Execute task with current context
            result = agent.execute(task, current_context)
            results[agent_name] = result
            
            # Update context with result for next agent
            if result.success:
                current_context[f"{agent_name}_result"] = result.result
            
            # Store in history
            self.task_history.append({
                "agent": agent_name,
                "task": task,
                "result": result.dict()
            })
        
        return {
            "results": results,
            "final_context": current_context,
            "success": all(r.success for r in results.values())
        }
    
    async def execute_parallel(
        self,
        tasks: List[Dict[str, Any]],
        max_concurrent: int = 3
    ) -> List[TaskResult]:
        """
        Execute multiple tasks in parallel across different agents.
        
        Args:
            tasks: List of task dictionaries with 'agent' and 'task' keys
            max_concurrent: Maximum number of concurrent executions
        
        Returns:
            List of TaskResult objects
        """
        logger.info(f"Starting parallel execution of {len(tasks)} tasks")
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def execute_with_semaphore(task_info: Dict[str, Any]):
            async with semaphore:
                agent_name = task_info["agent"]
                task = task_info["task"]
                context = task_info.get("context", {})
                
                if agent_name not in self.agents:
                    logger.error(f"Agent {agent_name} not found")
                    return None
                
                agent = self.agents[agent_name]
                
                # Run in executor to avoid blocking
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, agent.execute, task, context
                )
                
                return result
        
        # Execute all tasks
        results = await asyncio.gather(
            *[execute_with_semaphore(task) for task in tasks],
            return_exceptions=True
        )
        
        # Filter out None and exceptions
        valid_results = [r for r in results if isinstance(r, TaskResult)]
        
        return valid_results
    
    def execute_hierarchical(
        self,
        task: str,
        planner_agent: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute task using hierarchical planning.
        A planner agent breaks down the task and delegates to specialists.
        
        Args:
            task: The complex task to execute
            planner_agent: Name of the planner agent (optional)
            context: Optional context
        
        Returns:
            Dictionary with plan and execution results
        """
        logger.info(f"Starting hierarchical execution for task: {task}")
        
        # Use planner agent or create one
        if planner_agent and planner_agent in self.agents:
            planner = self.agents[planner_agent]
        else:
            planner = next(
                (a for a in self.agents.values() if isinstance(a, PlannerAgent)),
                None
            )
        
        if not planner:
            logger.error("No planner agent available")
            return {"success": False, "error": "No planner agent found"}
        
        # Get available agents
        available_agents = list(self.agents.keys())
        planning_context = context or {}
        planning_context["available_agents"] = available_agents
        
        # Create plan
        logger.info("Creating execution plan...")
        plan_result = planner.execute(task, planning_context)
        
        if not plan_result.success:
            return {"success": False, "error": "Planning failed", "details": plan_result}
        
        plan = plan_result.result
        steps = plan.get("steps", [])
        
        # Execute plan
        logger.info(f"Executing {len(steps)} steps...")
        step_results = []
        execution_context = context or {}
        
        for step in steps:
            agent_name = step.get("agent", "")
            step_task = step.get("description", "")
            
            if agent_name not in self.agents:
                logger.warning(f"Agent {agent_name} not found, skipping step")
                continue
            
            agent = self.agents[agent_name]
            result = agent.execute(step_task, execution_context)
            
            step_results.append({
                "step": step,
                "result": result.dict()
            })
            
            # Update context
            if result.success:
                execution_context[f"step_{step.get('step', 0)}_result"] = result.result
        
        return {
            "success": True,
            "plan": plan,
            "step_results": step_results,
            "final_context": execution_context
        }
    
    def add_agent(self, name: str, agent: BaseAgent):
        """Add a new agent to the orchestrator."""
        self.agents[name] = agent
        logger.info(f"Added agent: {name}")
    
    def remove_agent(self, name: str):
        """Remove an agent from the orchestrator."""
        if name in self.agents:
            del self.agents[name]
            logger.info(f"Removed agent: {name}")
    
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Get an agent by name."""
        return self.agents.get(name)
    
    def list_agents(self) -> List[str]:
        """List all available agent names."""
        return list(self.agents.keys())
    
    def get_task_history(self) -> List[Dict[str, Any]]:
        """Get the history of all executed tasks."""
        return self.task_history
    
    def clear_history(self):
        """Clear the task history."""
        self.task_history = []
        logger.info("Task history cleared")
