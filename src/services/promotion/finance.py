"""Сервис: Маркетинг — Финансы."""
from src.collectors.promotion.finance import FinanceCollector
from src.schemas.promotion.finance import DepositRequest
from src.services.base import BaseService


class FinanceService(BaseService):
    async def get_balance(self) -> dict:
        async with FinanceCollector() as c: return await c.get_balance()

    async def get_budget(self, advert_id: int) -> dict:
        async with FinanceCollector() as c: return await c.get_budget(advert_id)

    async def deposit_budget(self, advert_id: int, data: DepositRequest) -> dict:
        async with FinanceCollector() as c:
            return await c.deposit_budget(advert_id, data.model_dump(by_alias=True, exclude_none=True))

    async def get_upd(self, date_from: str, date_to: str) -> dict:
        async with FinanceCollector() as c: return await c.get_upd(date_from, date_to)

    async def get_payments(self, date_from: str, date_to: str) -> dict:
        async with FinanceCollector() as c: return await c.get_payments(date_from, date_to)
