from app.llm.providers.base_provider import BaseLLMProvider
from app.llm.gemini_client import GeminiClient
from app.llm.parsers.gemini_parser import parse_gemini_response
from app.llm.schemas.action_schema import AgentAction


class GeminiProvider(BaseLLMProvider):
    def __init__(self):
        self.client = GeminiClient()

    async def generate(self, messages):
        return await self.client.generate(messages)
    
    def parse_response(self, response) -> AgentAction:
        return parse_gemini_response(response)

    def build_user_message(self, text: str) :
        return {
            "role" : "user",
            "parts" : [{
                "text" : text
            }]
        }

    def build_retry_message(self, text: str):
        return {
            "role" : "user",
            "parts" : [{
                "text" : text
            }]
        }

    def build_tool_call_message(self, action: AgentAction):

        return {
            "role": "model",
            "parts": [action.raw_part]
        }
    
    def build_tool_result_message(
        self,
        action: AgentAction,
        result: dict
    ):
        return {
            "role": "user",
            "parts": [
                {
                    "functionResponse": {
                        "name": action.tool_name,
                        "response": result
                    }
                }
            ]
        }