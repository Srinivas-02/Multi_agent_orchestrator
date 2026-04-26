from fastapi import APIRouter 
from pydantic import BaseModel
from app.services.connection_manager import manager
from app.schemas.broadcast import BroadcastModel
router = APIRouter()

@router.post('/notifyAll')
async def notify_all(response : BroadcastModel):
    await manager.broadcast(response)
    return {"status" : "success"}