"""Сервис DB: Коммуникации — Чтение чатов из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.communications.chats import ChatsRepository
from src.services.base import BaseService


class ChatsDbService(BaseService):

    async def get_chats(
        self,
        session: AsyncSession,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        repo = ChatsRepository(session)
        total = await repo.count()
        items = await repo.get_filtered(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "chat_id": c.chat_id,
                    "client_name": c.client_name,
                    "nm_id": c.nm_id,
                    "subject_name": c.subject_name,
                    "last_message_text": c.last_message_text,
                    "last_message_dt": c.last_message_dt.isoformat() if c.last_message_dt else None,
                    "is_new": c.is_new,
                    "fetched_at": c.fetched_at.isoformat() if c.fetched_at else None,
                }
                for c in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }
