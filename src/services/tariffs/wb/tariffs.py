"""Сервис WB: Тарифы WB."""
from src.collectors.tariffs.tariffs import TariffsCollector
from src.services.base import BaseService


class TariffsWbService(BaseService):
    async def get_commissions(self) -> dict:
        async with TariffsCollector() as c: return await c.get_commissions()

    async def get_return_cost(self, date=None) -> dict:
        async with TariffsCollector() as c: return await c.get_return_cost(date)

    async def get_box_tariffs(self, date=None) -> dict:
        async with TariffsCollector() as c: return await c.get_box_tariffs(date)

    async def get_pallet_tariffs(self, date=None) -> dict:
        async with TariffsCollector() as c: return await c.get_pallet_tariffs(date)

    async def get_supply_tariffs(self, date=None) -> dict:
        async with TariffsCollector() as c: return await c.get_supply_tariffs(date)
