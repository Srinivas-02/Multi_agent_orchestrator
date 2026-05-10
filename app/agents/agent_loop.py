# app/agents/agent_loop.py

from app.agents.state import AgentState
from app.agents.retry import should_retry, build_retry_message
from app.agents.constants import MAX_AGENT_STEPS

from app.llm.validators.action_validator import validate_action
from app.llm.schemas.action_schema import AgentAction, ValidationResult
from app.llm.providers.base_provider import BaseLLMProvider


from app.tools.registry import TOOLS
from app.tools.executor import execute_tool

import logging

class AgentRuntime:

    def __init__(self):
        
        self.logger = logging.getLogger(__name__)

    async def run(
        self,
        query: str,
        state: AgentState,
        provider: BaseLLMProvider,
        max_steps: int = MAX_AGENT_STEPS
    ):        

        state.messages.append(
            provider.build_user_message(query)            
        )      

        for step in range(max_steps):

            state.current_step += 1
            yield f"Step {step+1}: Thinking..."    
            try:
                response = await provider.generate(state.messages)
            except Exception as e:
                yield f"LLM call failed: {str(e)}"
                return
            
            try:
                action: AgentAction = provider.parse_response(response)
            except Exception as e:
                if should_retry(state.retry_count):
                    state.retry_count += 1
                    retry_message = build_retry_message(str(e))
                    state.messages.append(
                        provider.build_retry_message(retry_message)                        
                    )
                    yield f"Parser Error: {str(e)}"
                    yield f"Retrying... ({state.retry_count})"
                    continue

                yield f"Parser failed after retries: {str(e)}"
                return
        
            state.retry_count = 0
            validation_result: ValidationResult = validate_action(
                action,
                TOOLS
            )

            if not validation_result.is_valid:
                if should_retry(state.retry_count):
                    state.retry_count += 1
                    retry_message = build_retry_message(
                        validation_result.error
                    )
                    state.messages.append(
                        provider.build_retry_message(retry_message)                        
                    )
                    yield f"Validation Failed: {validation_result.error}"
                    yield f"Retrying... ({state.retry_count})"
                    continue
                yield (
                    f"Validation failed after retries: "
                    f"{validation_result.error}"
                )
                return
            
            state.retry_count = 0
            if action.type == "tool":
                if state.last_tool == action.tool_name:
                    yield (
                        f"Stopping: repeated tool call "
                        f"({action.tool_name})"
                    )
                    return

                state.last_tool = action.tool_name
                yield (
                    f"Calling tool: "
                    f"{action.tool_name} "
                    f"with {action.tool_args}"
                )

                tool_result = execute_tool(action)
                yield f"Observation: {tool_result}"

                state.messages.append(
                    provider.build_tool_call_message(action)
                )

                state.messages.append(
                    provider.build_tool_result_message(action, tool_result)    
                )

                continue

            if action.type == "final":            
                yield f"Final Answer: {action.text}"
                return
            
        yield "Max steps reached."

