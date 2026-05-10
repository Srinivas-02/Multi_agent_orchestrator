from typing import Any, Literal, Optional
from pydantic import BaseModel, Field


class AgentAction(BaseModel):
    type: Literal["tool", "final"]
    tool_name: Optional[str] = None
    tool_args: Any = Field(default_factory=dict)
    text: Optional[str] = None
    raw_part: Any = None


class ValidationResult(BaseModel):
    is_valid: bool
    error: Optional[str] = None
