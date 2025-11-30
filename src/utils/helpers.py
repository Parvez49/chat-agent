"""Utility functions for the multi-agent system."""
import yaml
from pathlib import Path
from typing import Dict, Any
from loguru import logger


def load_yaml_config(filepath: str) -> Dict[str, Any]:
    """Load configuration from a YAML file."""
    try:
        path = Path(filepath)
        if not path.exists():
            logger.error(f"Config file not found: {filepath}")
            return {}
        
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config or {}
    except Exception as e:
        logger.error(f"Error loading YAML config: {e}")
        return {}


def setup_logging(log_level: str = "INFO", log_file: str = "./logs/agent.log"):
    """Setup logging configuration."""
    from loguru import logger
    import sys
    
    # Remove default handler
    logger.remove()
    
    # Add console handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True
    )
    
    # Add file handler
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        level=log_level,
        rotation="10 MB",
        retention="7 days"
    )
    
    logger.info("Logging configured")


def format_execution_time(seconds: float) -> str:
    """Format execution time in a human-readable format."""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.0f}s"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
