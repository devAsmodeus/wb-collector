"""Сервис: Маркетинг — Календарь акций."""
from src.collectors.promotion.calendar import CalendarCollector
from src.schemas.promotion.calendar import UploadPromotionNomenclaturesRequest
from src.services.base import BaseService


class CalendarService(BaseService):
    async def get_promotions(self, params: dict | None = None) -> dict:
        async with CalendarCollector() as c: return await c.get_promotions(params)

    async def get_promotion_details(self, params: dict | None = None) -> dict:
        async with CalendarCollector() as c: return await c.get_promotion_details(params)

    async def get_promotion_nomenclatures(self, params: dict | None = None) -> dict:
        async with CalendarCollector() as c: return await c.get_promotion_nomenclatures(params)

    async def upload_promotion_nomenclatures(self, data: UploadPromotionNomenclaturesRequest) -> dict:
        async with CalendarCollector() as c:
            return await c.upload_promotion_nomenclatures(data.model_dump())
