from typing import Any, Dict

from app.llm.schemas.action_schema import AgentAction, ValidationResult


def validate_action(action: AgentAction, tools: Dict[str, Dict[str, Any]]) -> ValidationResult:
    """Validate an AgentAction without executing it."""
    if action.type == "final":
        if not action.text or not action.text.strip():
            return ValidationResult(is_valid=False, error="Final response text is required")
        return ValidationResult(is_valid=True)

    if action.type != "tool":
        return ValidationResult(is_valid=False, error=f"Unsupported action type: {action.type}")

    if not action.tool_name:
        return ValidationResult(is_valid=False, error="Tool name is required")

    tool = tools.get(action.tool_name)
    if not tool:
        return ValidationResult(is_valid=False, error=f"Tool not found: {action.tool_name}")

    if not isinstance(action.tool_args, dict):
        return ValidationResult(is_valid=False, error="Tool arguments must be a dictionary")

    declaration = tool.get("declaration", {})
    parameters = declaration.get("parameters", {})
    required_fields = parameters.get("required", [])

    for field in required_fields:
        if field not in action.tool_args:
            return ValidationResult(is_valid=False, error=f"Missing required field: {field}")

    return ValidationResult(is_valid=True)
