"""Сервис WB: Коммуникации — Чат с покупателями."""
from src.collectors.communications.chat import ChatCollector
from src.schemas.communications.chat import SendMessageRequest
from src.services.base import BaseService


class ChatService(BaseService):
    async def get_chats(self, limit=10, offset=0) -> dict:
        async with ChatCollector() as c: return await c.get_chats(limit, offset)

    async def get_events(self, chat_id: str, limit=10, offset=0) -> dict:
        async with ChatCollector() as c: return await c.get_events(chat_id, limit, offset)

    async def send_message(self, data: SendMessageRequest) -> dict:
        async with ChatCollector() as c: return await c.send_message(data.model_dump(exclude_none=True))

    async def download_file(self, file_id: str) -> dict:
        async with ChatCollector() as c: return await c.download_file(file_id)
