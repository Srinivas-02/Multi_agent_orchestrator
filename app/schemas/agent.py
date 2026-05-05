from pydantic import BaseModel

class AgentQuery(BaseModel):
    message: str
    max_steps : int = 5