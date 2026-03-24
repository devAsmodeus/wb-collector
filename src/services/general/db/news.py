"""Сервис DB: Общее — Чтение новостей из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.general.news import NewsRepository
from src.services.base import BaseService


class NewsDbService(BaseService):

    async def get_from_db(self, session: AsyncSession, limit: int = 100, offset: int = 0) -> dict:
        """Возвращает новости из БД."""
        repo = NewsRepository(session)
        items = await repo.get_all(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "news_id": n.news_id,
                    "header": n.header,
                    "content": n.content,
                    "date": n.date.isoformat() if n.date else None,
                    "types": n.types,
                }
                for n in items
            ],
            "count": len(items),
        }
