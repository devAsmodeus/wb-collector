"""Репозиторий: Чаты с покупателями."""
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.communications import WbChat


class ChatsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, chats: list[dict]) -> int:
        if not chats:
            return 0
        rows = [
            {
                "chat_id": c.get("chatID", ""),
                "reply_sign": c.get("replySign"),
                "client_name": c.get("clientName"),
                "nm_id": c.get("goodCard", {}).get("nmId") if c.get("goodCard") else None,
                "subject_name": c.get("goodCard", {}).get("subjectName") if c.get("goodCard") else None,
                "last_message_text": c.get("lastMessage", {}).get("text") if c.get("lastMessage") else None,
                "last_message_dt": c.get("lastMessage", {}).get("addTime") if c.get("lastMessage") else None,
                "is_new": c.get("lastMessage", {}).get("isNewChat") if c.get("lastMessage") else None,
                "good_card": c.get("goodCard"),
                "last_message": c.get("lastMessage"),
                "fetched_at": datetime.utcnow(),
            }
            for c in chats if c.get("chatID")
        ]
        if not rows:
            return 0
        # 11 columns → chunk_size = 32767 // 11 = 2978
        CHUNK = 2900
        total = 0
        for i in range(0, len(rows), CHUNK):
            batch = rows[i:i + CHUNK]
            stmt = insert(WbChat).values(batch)
            stmt = stmt.on_conflict_do_update(
                index_elements=["chat_id"],
                set_={k: getattr(stmt.excluded, k) for k in batch[0] if k != "chat_id"},
            )
            await self._session.execute(stmt)
            total += len(batch)
        await self._session.commit()
        return total

    async def count(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(WbChat))
        return result.scalar_one()

    async def get_filtered(self, limit: int = 100, offset: int = 0) -> list[WbChat]:
        result = await self._session.execute(
            select(WbChat).order_by(WbChat.last_message_dt.desc().nulls_last()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())
