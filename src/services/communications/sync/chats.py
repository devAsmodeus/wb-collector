"""Сервис Sync: Коммуникации — Синхронизация чатов с покупателями."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.communications.chat import ChatCollector
from src.repositories.communications.chats import ChatsRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class ChatsSyncService(BaseService):

    async def sync_chats(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка всех чатов.
        WB API /api/v1/seller/chats возвращает все чаты без пагинации.
        """
        repo = ChatsRepository(session)

        async with ChatCollector() as collector:
            response = await collector.get_chats()

        chats = []
        if isinstance(response, dict):
            chats = response.get("result", response.get("chats", []))
        elif isinstance(response, list):
            chats = response

        if not chats:
            return {"synced": 0, "source": "full"}

        saved = await repo.upsert_many(chats)
        logger.info(f"Chats synced: {saved} chats")
        return {"synced": saved, "source": "full"}
