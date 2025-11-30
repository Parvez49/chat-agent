"""
Base agent class for all specialized agents.
"""
import time
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from loguru import logger

from src.core import OllamaLLM, AgentState, MessageRole, TaskResult
from src.tools.base import BaseTool


class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(
        self,
        name: str,
        model: str,
        system_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        tools: Optional[List[BaseTool]] = None,
    ):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = OllamaLLM(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        self.tools = tools or []
        self.state = AgentState(agent_name=name, task="")
        
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> TaskResult:
        """Execute a task and return the result."""
        start_time = time.time()
        
        try:
            self.state.task = task
            self.state.update_status("working")
            self.state.add_message(MessageRole.USER, task)
            
            logger.info(f"Agent {self.name} starting task: {task}")
            
            # Process the task
            result = self.process(task, context or {})
            
            self.state.update_status("completed")
            execution_time = time.time() - start_time
            
            logger.info(f"Agent {self.name} completed task in {execution_time:.2f}s")
            
            return TaskResult(
                success=True,
                result=result,
                agent_name=self.name,
                execution_time=execution_time,
                metadata={"state": self.state.dict()}
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.state.update_status("failed")
            logger.error(f"Agent {self.name} failed: {str(e)}")
            
            return TaskResult(
                success=False,
                result=None,
                error=str(e),
                agent_name=self.name,
                execution_time=execution_time
            )
    
    @abstractmethod
    def process(self, task: str, context: Dict[str, Any]) -> Any:
        """Process the task. Must be implemented by subclasses."""
        pass
    
    def think(self, prompt: str) -> str:
        """Generate a response using the LLM."""
        self.state.update_status("thinking")
        response = self.llm.generate(
            prompt=prompt,
            system_prompt=self.system_prompt
        )
        self.state.add_message(MessageRole.ASSISTANT, response)
        return response
    
    async def athink(self, prompt: str) -> str:
        """Async version of think."""
        self.state.update_status("thinking")
        response = await self.llm.agenerate(
            prompt=prompt,
            system_prompt=self.system_prompt
        )
        self.state.add_message(MessageRole.ASSISTANT, response)
        return response
    
    def use_tool(self, tool_name: str, **kwargs) -> Any:
        """Use a tool by name."""
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            raise ValueError(f"Tool {tool_name} not found")
        
        self.state.tools_used.append(tool_name)
        logger.info(f"Agent {self.name} using tool: {tool_name}")
        
        return tool.execute(**kwargs)
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names."""
        return [tool.name for tool in self.tools]
    
    def reset_state(self):
        """Reset the agent state."""
        self.state = AgentState(agent_name=self.name, task="")
