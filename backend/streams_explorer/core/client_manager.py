from dataclasses import dataclass, field

from fastapi import WebSocket
from loguru import logger
from pydantic import BaseModel


@dataclass(frozen=True)
class ClientManager:
    _clients: list[WebSocket] = field(init=False, default_factory=list)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        logger.info("WebSocket client {} connected", websocket.client)
        self._clients.append(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        await websocket.close()
        logger.info("WebSocket client {} disconnected", websocket.client)
        self._clients.remove(websocket)

    async def send(self, websocket: WebSocket, obj: BaseModel) -> None:
        await websocket.send_json(obj.dict())

    async def broadcast(self, obj: BaseModel) -> None:
        data = obj.dict()
        for client in self._clients:
            await client.send_json(data)

    @property
    def clients(self) -> list[WebSocket]:
        return self._clients
