import json
from app.tools.registry import TOOLS
from app.llm.gemini_client import GeminiClient
import logging
class GeminiAgent:
    def __init__(self):
        self.client = GeminiClient()
        self.logger = logging.getLogger(__name__)

    async def run(self, query : str, max_steps: int = 5):
        messages = [
            {
                "role" : "user",
                "parts" : [{"text" : query}]
            }
        ]

        last_tool = None

        for step in range(max_steps):

            yield f"Step {step+1} : Thinking...."

            try:
                response = await self.client.generate(messages)
            
            except Exception as e :
                yield f"LLM call failed : {str(e)}"
                return

            self.logger.info(f"\n\n Response from the gemini model : { response} \n\n")
            candidates = response.candidates or []
            if not candidates:
                yield "No response from model"
                return

            candidate = candidates[0]


            content = candidate.content
            parts = content.parts or []

            if not parts:
                yield "Empty response from model"
                return

            function_call = None
            text_response = None
            function_call_part = None
            for part in parts:
                if getattr(part, "function_call", None):
                    function_call = part.function_call
                    function_call_part = part  
                elif getattr(part, "text", None):
                    text_response = part.text

            if function_call:
                
                name = function_call.name
                args = function_call.args or {}

                if isinstance(args, str):
                    try:
                        args = json.loads(args)                                                    
                    except:
                        yield "Invalid tool arguments format"
                        return

                if name == last_tool:
                    yield "Stopping: repeated tool call"
                    return
                
                last_tool = name


                tool = TOOLS.get(name)

                if not tool:
                    yield f"Tool {name} not found"
                    return
                
                required_fields = tool["declaration"]["parameters"].get("required", [])
                for field in required_fields:
                    if field not in args:
                        yield f"Missing required field : {field}"
                        return

                yield f"Calling tool : {name} with {args}"

                try :
                    result = tool["function"](**args)
                except Exception as e:
                    result = f"error : {str(e)}"
                
                yield f"Observation : {result}"


                messages.append({
                    "role" : "model",
                    "parts" : [function_call_part]
                })

                messages.append({
                    "role" : "user",
                    "parts" : [{
                        "functionResponse" : {
                            "name" : name,
                            "response" : {
                                "result" : result
                            }
                        }
                    }]
                })

            elif text_response:
                yield f"Final Ansewr: {text_response}"
                return
            else:
                yield "Invalid response from model"
                return
        
        yield f"Max Steps Reached..."