from pydantic import BaseModel
from typing import  Literal, Optional

TaskType = Literal[
    "reverse",
    "uppercase",
    "count",
    "delay_stream"
]

class TaskRequest(BaseModel):
    task : TaskType
    data: str
    task_id : Optional[str] = None

class CancelRequest(BaseModel):
    action : Literal["cancel"]
    task_id : str

class TaskResponse(BaseModel):
    task_id : str
    status : str
    chunk : Optional[str] = None