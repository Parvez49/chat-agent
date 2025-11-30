"""
Message and state management for agents.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """Message role types."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(BaseModel):
    """Individual message in a conversation."""
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    agent_name: Optional[str] = None
    
    class Config:
        use_enum_values = True


class AgentState(BaseModel):
    """State of an agent during execution."""
    agent_name: str
    task: str
    status: str = "idle"  # idle, thinking, working, completed, failed
    current_step: int = 0
    max_steps: int = 10
    messages: List[Message] = Field(default_factory=list)
    tools_used: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def add_message(self, role: MessageRole, content: str, **kwargs):
        """Add a message to the state."""
        message = Message(
            role=role,
            content=content,
            agent_name=self.agent_name,
            **kwargs
        )
        self.messages.append(message)
        self.updated_at = datetime.utcnow()
    
    def get_conversation_history(self, last_n: Optional[int] = None) -> List[Dict[str, str]]:
        """Get conversation history in dict format."""
        messages = self.messages[-last_n:] if last_n else self.messages
        return [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
        ]
    
    def update_status(self, status: str):
        """Update the agent status."""
        self.status = status
        self.updated_at = datetime.utcnow()


class TaskResult(BaseModel):
    """Result of a task execution."""
    success: bool
    result: Any
    error: Optional[str] = None
    agent_name: str
    execution_time: float
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
