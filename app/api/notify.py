from fastapi import APIRouter 
from pydantic import BaseModel
from app.services.connection_manager import manager
from app.schemas.broadcast import BroadcastModel
router = APIRouter()

@router.post('/notifyAll')
async def notify_all(response : BroadcastModel):
    parsed_message = f" {response.sender} sent - {response.msg} "
    await manager.broadcast(parsed_message)
    return {"status" : "success"}