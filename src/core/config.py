"""
Core settings and configuration management for the multi-agent system.
"""
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Ollama Configuration
    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="llama3.1:8b")
    
    # Vector Database
    chroma_persist_dir: str = Field(default="./data/chroma")
    embedding_model: str = Field(default="all-MiniLM-L6-v2")
    
    # Agent Configuration
    max_iterations: int = Field(default=10, ge=1, le=50)
    agent_timeout: int = Field(default=300, ge=30, le=600)
    enable_gpu: bool = Field(default=True)
    
    # Memory Configuration
    memory_type: str = Field(default="chromadb")
    max_memory_items: int = Field(default=100, ge=10, le=1000)
    memory_window: int = Field(default=10, ge=1, le=50)
    
    # Logging
    log_level: str = Field(default="INFO")
    log_file: str = Field(default="./logs/agent.log")
    
    # Performance
    batch_size: int = Field(default=4, ge=1, le=32)
    max_concurrent_agents: int = Field(default=3, ge=1, le=10)
    gpu_memory_fraction: float = Field(default=0.8, ge=0.1, le=1.0)
    
    # Optional API Keys
    serper_api_key: Optional[str] = Field(default=None)
    brave_search_api_key: Optional[str] = Field(default=None)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def project_root(self) -> Path:
        """Get the project root directory."""
        return Path(__file__).parent.parent.parent
    
    @property
    def config_dir(self) -> Path:
        """Get the config directory."""
        return self.project_root / "config"
    
    @property
    def data_dir(self) -> Path:
        """Get the data directory."""
        return self.project_root / "data"
    
    @property
    def logs_dir(self) -> Path:
        """Get the logs directory."""
        return self.project_root / "logs"
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        directories = [
            self.data_dir,
            self.logs_dir,
            self.data_dir / "chroma",
            self.data_dir / "workspace",
            self.data_dir / "cache"
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
settings.ensure_directories()
