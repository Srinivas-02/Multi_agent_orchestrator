from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AgentState(BaseModel):
    # Shared state for the agent loop. The loop will decide how to update it.
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    current_step: int = 0
    last_tool: Optional[str] = None
    retry_count: int = 0    
