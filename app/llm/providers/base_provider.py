from abc import ABC, abstractmethod
from typing import Any, Dict

from app.llm.schemas.action_schema import AgentAction

class BaseLLMProvider(ABC):

    @abstractmethod
    async def generate(self, messages):
        """
        send messages to the provider and return raw response
        """
        pass

    @abstractmethod
    def parse_response(self, response) -> AgentAction:
        """
        Convert provider response into normalized AgentAction.
        """
        pass

    @abstractmethod
    def build_user_message(
        self,
        text: str
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def build_retry_message(
        self,
        text: str
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def build_tool_call_message(
        self,
        action: AgentAction,

    ) -> Dict[str, Any]:
        """
        Build provider-specific tool call message
 
        """
        pass

    @abstractmethod
    def build_tool_result_message(
        self,
        action: AgentAction,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build provider-specific tool result message
        """
        pass