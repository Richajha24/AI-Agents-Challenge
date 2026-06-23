from abc import ABC, abstractmethod
from typing import Dict, Any
import os


class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self._setup_client()
    
    def _setup_client(self):
        """Setup the AI client based on provider"""
        if self.provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif self.provider == "anthropic":
            from anthropic import Anthropic
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the input data and return results"""
        pass
    
    def _call_openai(self, messages: list, model: str = "gpt-4") -> str:
        """Call OpenAI API"""
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    
    def _call_anthropic(self, messages: list, model: str = "claude-3-sonnet-20240229") -> str:
        """Call Anthropic API"""
        response = self.client.messages.create(
            model=model,
            max_tokens=4096,
            messages=messages
        )
        return response.content[0].text
