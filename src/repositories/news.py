"""Репозиторий: Новости портала продавцов."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.references import WbNews
from src.schemas.general.news import NewsItem


class NewsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, items: list[NewsItem]) -> int:
        """Вставляет или обновляет новости. Возвращает кол-во обработанных записей."""
        if not items:
            return 0
        rows = [
            {
                "news_id": item.id,
                "header": item.header,
                "content": item.content,
                "date": datetime.fromisoformat(item.date) if item.date else None,
                "types": [t.model_dump() for t in item.types],
                "fetched_at": datetime.utcnow(),
            }
            for item in items
        ]
        stmt = insert(WbNews).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["news_id"],
            set_={
                "header": stmt.excluded.header,
                "content": stmt.excluded.content,
                "date": stmt.excluded.date,
                "types": stmt.excluded.types,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[WbNews]:
        """Возвращает новости из БД (последние сначала)."""
        result = await self._session.execute(
            select(WbNews).order_by(WbNews.date.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_max_id(self) -> int | None:
        """Возвращает максимальный news_id в БД (для инкрементального обновления)."""
        result = await self._session.execute(
            select(WbNews.news_id).order_by(WbNews.news_id.desc()).limit(1)
        )
        return result.scalar_one_or_none()
