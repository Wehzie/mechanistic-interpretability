"""
Model wrapper classes for different API providers.

Provides an abstract base class and implementations for OpenAI and
extensible design for other providers (Together AI, Runpod, HuggingFace, Ollama).
"""

import os
import time
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import openai
from openai import OpenAI


class BaseModel(ABC):
    """Abstract base class for model wrappers."""
    
    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Send a chat completion request.
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        pass
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Input prompt string
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        pass


class OpenAIModel(BaseModel):
    """OpenAI API model wrapper."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, project_id: Optional[str] = None):
        """
        Initialize OpenAI model.
        
        Args:
            model_name: Name of the model (e.g., 'gpt-5.2-2025-12-11')
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            project_id: OpenAI project ID (optional)
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.project_id = project_id or os.getenv("OPENAI_PROJECT_ID")
        
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key, project=self.project_id)
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        max_retries: int = 3,
        reasoning_effort: str = "none",
    ) -> str:
        """
        Send a chat completion request with retry logic.
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys
            temperature: Sampling temperature (only supported with reasoning_effort="none")
            max_tokens: Maximum tokens to generate
            max_retries: Number of retry attempts
            reasoning_effort: Reasoning effort level ("none", "low", "medium", "high", "xhigh")
                             Defaults to "none" to disable reasoning
        """
        for attempt in range(max_retries):
            try:
                # Build request parameters
                params = {
                    "model": self.model_name,
                    "messages": messages,
                    "temperature": temperature,
                }
                
                # Note: The 'reasoning' parameter is not currently supported by the OpenAI SDK
                # Even for GPT-5 models, we skip it since the SDK doesn't accept it
                # If reasoning_effort is not "none", we log a warning but proceed without it
                if (
                    "gpt-5" in self.model_name.lower() 
                    and "gpt-5-mini" not in self.model_name.lower()
                    and reasoning_effort != "none"
                ):
                    # Reasoning parameter not supported by current SDK version
                    # Temperature may not work with reasoning models, but we try anyway
                    pass
                
                if max_tokens is not None:
                    params["max_tokens"] = max_tokens
                
                response = self.client.chat.completions.create(**params)
                return response.choices[0].message.content.strip()
            except (TypeError, AttributeError) as e:
                # Handle case where a parameter is not supported
                error_msg = str(e).lower()
                if "unexpected keyword" in error_msg:
                    # Try to identify which parameter caused the issue
                    if "reasoning" in error_msg:
                        # Retry without reasoning parameter (already not included, so this shouldn't happen)
                        pass
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        time.sleep(wait_time)
                        continue
                raise
            except openai.RateLimitError as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    time.sleep(wait_time)
                    continue
                raise
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    continue
                raise
        
        raise RuntimeError(f"Failed to get response after {max_retries} attempts")
    
    def generate(
        self,
        prompt: str,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        reasoning_effort: str = "none",
    ) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Input prompt string
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            reasoning_effort: Reasoning effort level (defaults to "none" to disable reasoning)
        """
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, temperature=temperature, max_tokens=max_tokens, reasoning_effort=reasoning_effort)


# Placeholder classes for future providers (implement if OpenAI refusals occur)

class TogetherAIModel(BaseModel):
    """Together AI model wrapper (placeholder)."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        raise NotImplementedError("TogetherAIModel not yet implemented")
    
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.0, max_tokens: Optional[int] = None) -> str:
        raise NotImplementedError
    
    def generate(self, prompt: str, temperature: float = 0.0, max_tokens: Optional[int] = None) -> str:
        raise NotImplementedError


class RunpodModel(BaseModel):
    """Runpod model wrapper (placeholder)."""
    
    def __init__(self, model_name: str, endpoint_url: Optional[str] = None, api_key: Optional[str] = None):
        raise NotImplementedError("RunpodModel not yet implemented")
    
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.0, max_tokens: Optional[int] = None) -> str:
        raise NotImplementedError
    
    def generate(self, prompt: str, temperature: float = 0.0, max_tokens: Optional[int] = None) -> str:
        raise NotImplementedError


class HuggingFaceEndpointModel(BaseModel):
    """HuggingFace Endpoint model wrapper (placeholder)."""
    
    def __init__(self, model_name: str, endpoint_url: Optional[str] = None, api_key: Optional[str] = None):
        raise NotImplementedError("HuggingFaceEndpointModel not yet implemented")
    
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.0, max_tokens: Optional[int] = None) -> str:
        raise NotImplementedError
    
    def generate(self, prompt: str, temperature: float = 0.0, max_tokens: Optional[int] = None) -> str:
        raise NotImplementedError


class OllamaModel(BaseModel):
    """Ollama model wrapper (placeholder)."""
    
    def __init__(self, model_name: str, base_url: Optional[str] = None):
        raise NotImplementedError("OllamaModel not yet implemented")
    
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.0, max_tokens: Optional[int] = None) -> str:
        raise NotImplementedError
    
    def generate(self, prompt: str, temperature: float = 0.0, max_tokens: Optional[int] = None) -> str:
        raise NotImplementedError

