import asyncio
from google import genai
from google.genai import types
from app.tools.registry import get_tool_declarations

client = genai.Client()

tools = types.Tool(function_declarations=get_tool_declarations())

config = types.GenerateContentConfig(
    tools=[tools]
)


class GeminiClient:
    
    async def generate(self, messages):        
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-3-flash-preview",
            contents=messages,
            config=config
        )

        return response  