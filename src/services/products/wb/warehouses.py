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

    async def create_seller_warehouse(self, name: str, office_id: int) -> dict:
        async with ProductsCollector() as c:
            return await c.warehouses.create_seller_warehouse(name=name, office_id=office_id)

    async def update_seller_warehouse(self, warehouse_id: int, data: dict) -> dict:
        async with ProductsCollector() as c:
            return await c.warehouses.update_seller_warehouse(
                warehouse_id=warehouse_id,
                name=data.get("name", ""),
                office_id=data.get("officeId", 0),
            )

    async def delete_seller_warehouse(self, warehouse_id: int) -> dict:
        async with ProductsCollector() as c:
            return await c.warehouses.delete_seller_warehouse(warehouse_id=warehouse_id)

    async def get_stocks(self, warehouse_id: int, skus: list[str]) -> dict:
        async with ProductsCollector() as c:
            return await c.warehouses.get_stocks(warehouse_id=warehouse_id, skus=skus)

    async def update_stocks(self, warehouse_id: int, stocks: list) -> dict:
        async with ProductsCollector() as c:
            return await c.warehouses.update_stocks(warehouse_id=warehouse_id, stocks=stocks)

    async def delete_stocks(self, warehouse_id: int, skus: list) -> dict:
        async with ProductsCollector() as c:
            return await c.warehouses.delete_stocks(warehouse_id=warehouse_id, skus=skus)
