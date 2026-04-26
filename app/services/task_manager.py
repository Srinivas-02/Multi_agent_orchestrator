import asyncio
import uuid 
from fastapi import WebSocket
from app.schemas.task import TaskResponse
from app.services.tasks import (
    reverse_stream,
    uppercase_stream,
    count_stream,
    delay_stream
)


TASK_MAP = {
    'reverse' : reverse_stream,
    'uppercase' : uppercase_stream,
    'count' : count_stream,
    'delay_stream': delay_stream

}

class TaskManager():
    def __init__(self):
        self.active_tasks = {} #task_id -> asyncio task
        self.task_owner = {}  # task_id -> websocket

    async def start_task(self, websocket : WebSocket, task_type : str, data: str):
        task_id = str(uuid.uuid4())
        async def runner():
            try:
                await websocket.send_json(
                    TaskResponse(
                        task_id = task_id,
                        status = "created"
                    ).dict()
                )

                async for ch in TASK_MAP[task_type](data):
                    await websocket.send_json(
                        TaskResponse(
                            task_id = task_id,
                            status = "streaming",
                            chunk = ch
                        ).dict()
                    )

                await websocket.send_json(
                    TaskResponse(
                        task_id = task_id,
                        status = "completed"
                    ).dict()
                )
            except asyncio.CancelledError:
                await websocket.send_json(
                    TaskResponse(
                        task_id= task_id,
                        status = "cancelled"
                    ).dict()
                )

        
        task = asyncio.create_task(runner())
        self.active_tasks[task_id] = task
        self.task_owner[task_id] = websocket
        return task_id
    

    async def cancel_task(self, task_id:str):
        task = self.active_tasks.get(task_id)
        if task:
            task.cancel()
            self.active_tasks.pop(task_id, None)
            self.task_owner.pop(task_id, None)