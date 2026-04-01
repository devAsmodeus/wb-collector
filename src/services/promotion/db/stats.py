"""Сервис DB: Маркетинг — Чтение статистики кампаний из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.promotion.campaign_stats import CampaignStatsRepository
from src.services.base import BaseService


class StatsDbService(BaseService):

    async def get_stats(
        self,
        session: AsyncSession,
        advert_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Возвращает статистику кампаний из БД."""
        repo = CampaignStatsRepository(session)
        total = await repo.count()
        if advert_id is not None:
            items = await repo.get_by_campaign(advert_id, limit=limit, offset=offset)
        else:
            items = await repo.get_all(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "advert_id": s.advert_id,
                    "date": s.date.isoformat() if s.date else None,
                    "views": s.views,
                    "clicks": s.clicks,
                    "ctr": float(s.ctr) if s.ctr is not None else None,
                    "cpc": float(s.cpc) if s.cpc is not None else None,
                    "sum": float(s.sum_) if s.sum_ is not None else None,
                    "atbs": s.atbs,
                    "orders": s.orders,
                    "cr": float(s.cr) if s.cr is not None else None,
                    "shks": s.shks,
                    "sum_price": float(s.sum_price) if s.sum_price is not None else None,
                    "fetched_at": s.fetched_at.isoformat() if s.fetched_at else None,
                }
                for s in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }
