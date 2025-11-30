"""
Common tools for agents.
"""
import json
import subprocess
from typing import Any, Dict, List
from pathlib import Path
from loguru import logger

from .base import BaseTool, ToolConfig


class CalculatorTool(BaseTool):
    """Tool for mathematical calculations."""
    
    def __init__(self):
        config = ToolConfig(
            name="calculator",
            description="Perform mathematical calculations",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        )
        super().__init__(config)
    
    def execute(self, expression: str, **kwargs) -> float:
        """Evaluate a mathematical expression."""
        try:
            # Safe evaluation of mathematical expressions
            allowed_names = {
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow
            }
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return float(result)
        except Exception as e:
            logger.error(f"Calculator error: {e}")
            raise ValueError(f"Invalid expression: {expression}")


class FileReadTool(BaseTool):
    """Tool for reading files."""
    
    def __init__(self, base_directory: str = "./data/workspace"):
        config = ToolConfig(
            name="file_read",
            description="Read contents of a file",
            parameters={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to the file to read"
                    }
                },
                "required": ["filepath"]
            }
        )
        super().__init__(config)
        self.base_directory = Path(base_directory)
        self.base_directory.mkdir(parents=True, exist_ok=True)
    
    def execute(self, filepath: str, **kwargs) -> str:
        """Read a file and return its contents."""
        try:
            full_path = self.base_directory / filepath
            
            if not full_path.exists():
                raise FileNotFoundError(f"File not found: {filepath}")
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return content
        except Exception as e:
            logger.error(f"File read error: {e}")
            raise


class FileWriteTool(BaseTool):
    """Tool for writing files."""
    
    def __init__(self, base_directory: str = "./data/workspace"):
        config = ToolConfig(
            name="file_write",
            description="Write content to a file",
            parameters={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to the file to write"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file"
                    }
                },
                "required": ["filepath", "content"]
            }
        )
        super().__init__(config)
        self.base_directory = Path(base_directory)
        self.base_directory.mkdir(parents=True, exist_ok=True)
    
    def execute(self, filepath: str, content: str, **kwargs) -> str:
        """Write content to a file."""
        try:
            full_path = self.base_directory / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Successfully wrote to {filepath}"
        except Exception as e:
            logger.error(f"File write error: {e}")
            raise


class PythonExecutorTool(BaseTool):
    """Tool for executing Python code."""
    
    def __init__(self, timeout: int = 30):
        config = ToolConfig(
            name="python_executor",
            description="Execute Python code and return the output",
            parameters={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute"
                    }
                },
                "required": ["code"]
            }
        )
        super().__init__(config)
        self.timeout = timeout
    
    def execute(self, code: str, **kwargs) -> Dict[str, Any]:
        """Execute Python code safely."""
        try:
            # Create a temporary file for the code
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Execute the code
            result = subprocess.run(
                ['python', temp_file],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            # Clean up
            Path(temp_file).unlink()
            
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0
            }
            
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"Execution timed out after {self.timeout} seconds",
                "returncode": -1,
                "success": False
            }
        except Exception as e:
            logger.error(f"Python execution error: {e}")
            return {
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
                "success": False
            }


class SearchTool(BaseTool):
    """Tool for searching in documents or data."""
    
    def __init__(self):
        config = ToolConfig(
            name="search",
            description="Search for information in documents",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "documents": {
                        "type": "array",
                        "description": "List of documents to search"
                    }
                },
                "required": ["query"]
            }
        )
        super().__init__(config)
    
    def execute(self, query: str, documents: List[str] = None, **kwargs) -> List[Dict[str, Any]]:
        """Search for query in documents."""
        if not documents:
            return []
        
        results = []
        query_lower = query.lower()
        
        for idx, doc in enumerate(documents):
            if query_lower in doc.lower():
                # Simple relevance scoring based on frequency
                score = doc.lower().count(query_lower)
                results.append({
                    "document_id": idx,
                    "content": doc,
                    "relevance_score": score
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results
