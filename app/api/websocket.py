from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.schemas.agent import AgentQuery
from app.agents.agent_loop import GeminiAgent
from app.services.connection_manager import manager
import json

router = APIRouter()

@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)
    client = GeminiAgent()
    try:
        while True:
            data = await websocket.receive_json()
            try:
                req = AgentQuery(**data)
            except Exception:
                await websocket.send_text("Invalid request")


            async for step in client.run(req.message , req.max_steps):
                await websocket.send_text(f"{step}")

            await websocket.send_text("Completed")                
            

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        print("Client disconnected")