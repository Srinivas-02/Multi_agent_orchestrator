from app.llm.schemas.action_schema import AgentAction


def _get_value(obj, key: str, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def parse_gemini_response(response) -> AgentAction:
    """Parse a Gemini SDK response into a normalized AgentAction."""
    candidates = _get_value(response, "candidates") or []
    if not candidates:
        raise ValueError("Gemini response has no candidates")

    candidate = candidates[0]
    content = _get_value(candidate, "content")
    parts = _get_value(content, "parts") or []
    if not parts:
        raise ValueError("Gemini response candidate has no content parts")

    text_parts = []

    for part in parts:
        function_call = _get_value(part, "function_call")
        if function_call:
            name = _get_value(function_call, "name")
            args = _get_value(function_call, "args") or {}
            if not name:
                raise ValueError("Gemini function call is missing a name")
            return AgentAction(type="tool", tool_name=name, tool_args=args, raw_part=part)

        text = _get_value(part, "text")
        if text:
            text_parts.append(text)

    final_text = "".join(text_parts).strip()
    if final_text:
        return AgentAction(type="final", text=final_text)

    raise ValueError("Gemini response did not contain a function call or text")
