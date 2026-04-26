from fastapi import FastAPI, Request, HTTPException
from app.routes import websocket, notify

app = FastAPI()

app.include_router(websocket.router)
app.include_router(notify.router)

