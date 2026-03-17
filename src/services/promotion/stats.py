"""Сервис: Маркетинг — Статистика и медиакампании."""
from src.collectors.promotion.stats import StatsCollector
from src.schemas.promotion.stats import CampaignStatsRequest
from src.services.base import BaseService


class StatsService(BaseService):
    async def get_fullstats(self, ids: str, begin_date=None, end_date=None) -> dict:
        async with StatsCollector() as c: return await c.get_fullstats(ids, begin_date, end_date)

    async def get_stats(self, data: CampaignStatsRequest) -> dict:
        async with StatsCollector() as c: return await c.get_stats(data.intervals)

    async def get_media_count(self) -> dict:
        async with StatsCollector() as c: return await c.get_media_count()

    async def get_media_adverts(self, status=None, type_=None, limit=50, offset=0, order=None, direction=None) -> dict:
        async with StatsCollector() as c:
            return await c.get_media_adverts(status, type_, limit, offset, order, direction)

    async def get_media_advert(self, advert_id: int) -> dict:
        async with StatsCollector() as c: return await c.get_media_advert(advert_id)
