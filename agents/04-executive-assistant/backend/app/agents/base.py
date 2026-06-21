from abc import ABC, abstractmethod
from typing import Dict, Any
from app.ai.provider import AIProvider

class Agent(ABC):
    """Base agent class"""
    
    def __init__(self, provider: AIProvider):
        self.provider = provider
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute agent task"""
        pass
