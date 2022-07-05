from dataclasses import dataclass, field
from typing import List

from fastapi import WebSocket
from loguru import logger
from pydantic import BaseModel


@dataclass(init=False)
class ClientManager:
    _clients: List[WebSocket] = field(default_factory=list)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        logger.info("WebSocket client {} connected", websocket.client.host)
        self._clients.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        await websocket.close()
        logger.info("WebSocket client {} disconnected", websocket.client.host)
        self._clients.remove(websocket)

    async def send(self, websocket: WebSocket, obj: BaseModel):
        await websocket.send_json(obj.dict())

    async def broadcast(self, obj: BaseModel):
        data = obj.dict()
        for client in self._clients:
            await client.send_json(data)

    @property
    def clients(self) -> List[WebSocket]:
        return self._clients
