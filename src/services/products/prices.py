"""Сервис: Работа с товарами — Цены и скидки."""
from src.collectors.products import ProductsCollector
from src.schemas.products.prices import GoodsListResponse
from src.services.base import BaseService


class PricesService(BaseService):

    async def get_goods(self, limit: int = 100, offset: int = 0) -> GoodsListResponse:
        async with ProductsCollector() as c:
            return await c.prices.get_goods_list(limit=limit, offset=offset)

    async def get_goods_by_nm(self, nm_ids: list[int]) -> GoodsListResponse:
        async with ProductsCollector() as c:
            return await c.prices.get_goods_list_by_nm(nm_ids)

    async def get_goods_sizes(self, nm_id: int) -> dict:
        async with ProductsCollector() as c:
            return await c.prices.get_goods_sizes(nm_id)

    async def get_quarantine(self, limit: int = 100, offset: int = 0) -> dict:
        async with ProductsCollector() as c:
            return await c.prices.get_quarantine_goods(limit=limit, offset=offset)

    async def get_upload_history(self, limit: int = 100, offset: int = 0) -> dict:
        async with ProductsCollector() as c:
            return await c.prices.get_price_upload_history(limit=limit, offset=offset)

    async def get_upload_goods(self, upload_id: int) -> dict:
        async with ProductsCollector() as c:
            return await c.prices.get_price_upload_goods(upload_id)

    async def get_buffer_tasks(self, limit: int = 100, offset: int = 0) -> dict:
        async with ProductsCollector() as c:
            return await c.prices.get_buffer_tasks(limit=limit, offset=offset)

    async def get_buffer_goods(self, upload_id: int) -> dict:
        async with ProductsCollector() as c:
            return await c.prices.get_buffer_goods(upload_id)
