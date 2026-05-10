from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import Any, Dict

from app.agents.constants import TOOL_EXECUTION_TIMEOUT
from app.llm.schemas.action_schema import AgentAction
from app.tools.registry import TOOLS


def execute_tool(action: AgentAction) -> Dict[str, Any]:
    """Execute a validated tool action and return a standard response."""
    if action.type != "tool":
        return {"success": False, "error": "Only tool actions can be executed"}

    tool = TOOLS.get(action.tool_name or "")
    if not tool:
        return {"success": False, "error": f"Tool not found: {action.tool_name}"}

    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(tool["function"], **action.tool_args)
            result = future.result(timeout=TOOL_EXECUTION_TIMEOUT)
        return {"success": True, "result": result}
    except TimeoutError:
        return {
            "success": False,
            "error": f"Tool execution timed out after {TOOL_EXECUTION_TIMEOUT} seconds",
        }
    except Exception as exc:
        return {"success": False, "error": str(exc)}
