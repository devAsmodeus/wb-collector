"""Коллектор: Маркетинг — Статистика и медиакампании."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.promotion.stats import FullStatsResponse


class StatsCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_ADVERT_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_fullstats(self, ids: str, begin_date: str | None = None, end_date: str | None = None) -> FullStatsResponse:
        params: dict = {"ids": ids}
        if begin_date: params["beginDate"] = begin_date
        if end_date: params["endDate"] = end_date
        data = await self._client.get("/adv/v3/fullstats", params=params)
        return FullStatsResponse.model_validate({"data": data} if isinstance(data, list) else data if isinstance(data, dict) else {})

    async def get_stats(self, payload: list) -> dict:
        return await self._client.post("/adv/v1/stats", json=payload)

    async def get_media_count(self) -> dict:
        return await self._client.get("/adv/v1/count")

    async def get_media_adverts(
        self,
        status: int | None = None,
        type_: int | None = None,
        limit: int = 50,
        offset: int = 0,
        order: str | None = None,
        direction: str | None = None,
    ) -> dict:
        params: dict = {"limit": limit, "offset": offset}
        if status is not None: params["status"] = status
        if type_ is not None: params["type"] = type_
        if order: params["order"] = order
        if direction: params["direction"] = direction
        return await self._client.get("/adv/v1/adverts", params=params)

    async def get_media_advert(self, advert_id: int) -> dict:
        return await self._client.get("/adv/v1/advert", params={"id": advert_id})
