"""
Ollama LLM integration with GPU optimization.
"""
import asyncio
from typing import Optional, Dict, Any, List
import ollama
from loguru import logger


class OllamaLLM:
    """Wrapper for Ollama LLM with optimized settings."""
    
    def __init__(
        self,
        model: str = "llama3.1:8b",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ):
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = ollama.Client(host=base_url)
        
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate a response from the model."""
        try:
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": temperature or self.temperature,
                    "num_predict": max_tokens or self.max_tokens,
                    **kwargs
                }
            )
            
            return response['message']['content']
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    async def agenerate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Async generate a response from the model."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.generate(
                prompt, system_prompt, temperature, max_tokens, **kwargs
            )
        )
    
    def stream_generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """Stream generate a response from the model."""
        try:
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            stream = self.client.chat(
                model=self.model,
                messages=messages,
                stream=True,
                options={
                    "temperature": temperature or self.temperature,
                    "num_predict": max_tokens or self.max_tokens,
                    **kwargs
                }
            )
            
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    yield chunk['message']['content']
                    
        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            raise
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embeddings for text."""
        try:
            response = self.client.embeddings(
                model=self.model,
                prompt=text
            )
            return response['embedding']
        except Exception as e:
            logger.error(f"Error getting embeddings: {e}")
            raise
    
    def list_models(self) -> List[str]:
        """List available models."""
        try:
            models = self.client.list()
            return [model['name'] for model in models['models']]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    def check_model_exists(self) -> bool:
        """Check if the specified model exists."""
        available_models = self.list_models()
        return self.model in available_models
