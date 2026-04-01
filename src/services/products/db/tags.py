"""Сервис DB: Товары — Чтение тегов из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.products.tags import TagsRepository
from src.services.base import BaseService


class TagsDbService(BaseService):

    async def get_tags(self, session: AsyncSession) -> dict:
        """Возвращает все теги из БД."""
        repo = TagsRepository(session)
        total = await repo.count()
        items = await repo.get_all()
        return {
            "data": [
                {
                    "tag_id": t.tag_id,
                    "name": t.name,
                    "color": t.color,
                    "fetched_at": t.fetched_at.isoformat() if t.fetched_at else None,
                }
                for t in items
            ],
            "total": total,
            "limit": total,
            "offset": 0,
        }
