"""Коллектор: Маркетинг — Календарь акций."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.promotion.calendar import PromotionsResponse


class CalendarCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_ADVERT_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_promotions(self, params: dict | None = None) -> PromotionsResponse:
        data = await self._client.get("/api/v1/calendar/promotions", params=params or {})
        return PromotionsResponse.model_validate(data if isinstance(data, dict) else {})

    async def get_promotion_details(self, params: dict | None = None) -> dict:
        return await self._client.get("/api/v1/calendar/promotions/details", params=params or {})

    async def get_promotion_nomenclatures(self, params: dict | None = None) -> dict:
        return await self._client.get("/api/v1/calendar/promotions/nomenclatures", params=params or {})

    async def upload_promotion_nomenclatures(self, payload: dict) -> dict:
        return await self._client.post("/api/v1/calendar/promotions/upload", json=payload)
