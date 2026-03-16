"""Сервис: Работа с товарами — Остатки и склады продавца."""
from src.collectors.products import ProductsCollector
from src.services.base import BaseService


class WarehousesService(BaseService):

    async def get_wb_offices(self) -> dict:
        async with ProductsCollector() as c:
            return await c.warehouses.get_wb_offices()

    async def get_seller_warehouses(self) -> dict:
        async with ProductsCollector() as c:
            return await c.warehouses.get_seller_warehouses()

    async def get_stocks(self, warehouse_id: int, skus: list[str]) -> dict:
        async with ProductsCollector() as c:
            return await c.warehouses.get_stocks(warehouse_id=warehouse_id, skus=skus)
