from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.task_manager import TaskManager
from app.schemas.task import TaskRequest, CancelRequest
import json

router = APIRouter()
task_manager = TaskManager()

@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)

            # 🔥 Detect cancel request
            if data.get("action") == "cancel":
                cancel_req = CancelRequest(**data)
                await task_manager.cancel_task(cancel_req.task_id)
                continue

            # 🔥 Normal task
            task_req = TaskRequest(**data)

            task_id = await task_manager.start_task(
                websocket,
                task_req.task,
                task_req.data
            )

            await websocket.send_json({
                "task_id": task_id,
                "status": "queued"
            })

    except WebSocketDisconnect:
        print("Client disconnected")