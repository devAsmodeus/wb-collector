"""Сервис DB: Маркетинг — Чтение кампаний из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.promotion.campaigns import CampaignsRepository
from src.services.base import BaseService


class CampaignsDbService(BaseService):

    async def get_campaigns(
        self,
        session: AsyncSession,
        status: int | None = None,
        type_: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Возвращает кампании из БД с фильтрацией."""
        repo = CampaignsRepository(session)
        total = await repo.count()
        if status is not None or type_ is not None:
            items = await repo.get_filtered(status=status, type_=type_, limit=limit, offset=offset)
        else:
            items = await repo.get_all(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "advert_id": c.advert_id,
                    "name": c.name,
                    "status": c.status,
                    "type": c.type,
                    "payment_type": c.payment_type,
                    "create_time": c.create_time.isoformat() if c.create_time else None,
                    "change_time": c.change_time.isoformat() if c.change_time else None,
                    "start_time": c.start_time.isoformat() if c.start_time else None,
                    "end_time": c.end_time.isoformat() if c.end_time else None,
                    "fetched_at": c.fetched_at.isoformat() if c.fetched_at else None,
                }
                for c in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }
