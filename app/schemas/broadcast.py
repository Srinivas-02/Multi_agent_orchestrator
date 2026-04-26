from pydantic import BaseModel

class BroadcastModel(BaseModel):
    sender : str
    msg : str