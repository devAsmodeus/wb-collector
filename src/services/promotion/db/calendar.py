"""Сервис DB: Маркетинг — Чтение акций из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.promotion.promotions import PromotionsRepository
from src.services.base import BaseService


class CalendarDbService(BaseService):

    async def get_promotions(
        self,
        session: AsyncSession,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Возвращает акции из БД."""
        repo = PromotionsRepository(session)
        items = await repo.get_all(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "promotion_id": p.promotion_id,
                    "name": p.name,
                    "start_date": p.start_date.isoformat() if p.start_date else None,
                    "end_date": p.end_date.isoformat() if p.end_date else None,
                    "type": p.type,
                    "in_action": p.in_action,
                    "fetched_at": p.fetched_at.isoformat() if p.fetched_at else None,
                }
                for p in items
            ],
            "count": len(items),
        }
