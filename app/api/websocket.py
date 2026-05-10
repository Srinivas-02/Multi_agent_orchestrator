from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.schemas.agent import AgentQuery
from app.agents.agent_loop import AgentRuntime
from app.services.connection_manager import manager
from app.agents.state import AgentState
from app.llm.providers.gemini_provider import GeminiProvider
import json

router = APIRouter()

@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)
    client = AgentRuntime()
    agent_provider = GeminiProvider()
    try:
        while True:
            data = await websocket.receive_json()
            try:
                req = AgentQuery(**data)
            except Exception:
                await websocket.send_text("Invalid request")

            state = AgentState()
            async for step in client.run(req.message , state, agent_provider, req.max_steps):
                await websocket.send_text(f"{step}")

            await websocket.send_text("Completed")                
            

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        print("Client disconnected")