"""Сервис WB: Коммуникации — Закреплённые отзывы."""
from src.collectors.communications.pins import PinsCollector
from src.schemas.communications.pins import PinFeedbackRequest, UnpinFeedbackRequest
from src.services.base import BaseService


class PinsService(BaseService):
    async def get_list(self, nm_id=None) -> dict:
        async with PinsCollector() as c: return await c.get_list(nm_id)

    async def pin(self, data: PinFeedbackRequest) -> dict:
        async with PinsCollector() as c: return await c.pin(data.model_dump())

    async def unpin(self, data: UnpinFeedbackRequest) -> dict:
        async with PinsCollector() as c: return await c.unpin(data.model_dump())

    async def get_count(self) -> dict:
        async with PinsCollector() as c: return await c.get_count()

    async def get_limits(self) -> dict:
        async with PinsCollector() as c: return await c.get_limits()
