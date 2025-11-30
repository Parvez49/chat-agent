"""
Base tool interface for agent tools.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel


class ToolConfig(BaseModel):
    """Configuration for a tool."""
    name: str
    description: str
    parameters: Dict[str, Any] = {}


class BaseTool(ABC):
    """Base class for all agent tools."""
    
    def __init__(self, config: ToolConfig):
        self.name = config.name
        self.description = config.description
        self.parameters = config.parameters
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters."""
        pass
    
    def validate_parameters(self, **kwargs) -> bool:
        """Validate that required parameters are provided."""
        required = self.parameters.get("required", [])
        return all(param in kwargs for param in required)
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the tool schema for LLM function calling."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
