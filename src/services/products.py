"""Сервис 02-products."""
import logging
from src.collectors.products import ProductsCollector
from src.schemas.products import (
    GoodsListResponse, CardsListResponse, CardsListRequest,
    SubjectsResponse, BrandsResponse,
)
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class ProductsService(BaseService):

    # ─── Цены (основная задача) ───────────────────────────────────────────────

    async def get_goods_prices(self, limit: int = 100, offset: int = 0) -> GoodsListResponse:
        """Получить товары с ценами и скидками."""
        async with ProductsCollector() as c:
            return await c.get_goods_list(limit=limit, offset=offset)

    async def get_goods_prices_by_nm(self, nm_ids: list[int]) -> GoodsListResponse:
        """Получить цены по конкретным артикулам."""
        async with ProductsCollector() as c:
            return await c.get_goods_list_by_nm(nm_ids)

    async def get_goods_sizes(self, nm_id: int) -> dict:
        """Получить цены по размерам артикула."""
        async with ProductsCollector() as c:
            return await c.get_goods_sizes(nm_id)

    async def get_quarantine(self, limit: int = 100, offset: int = 0) -> dict:
        """Товары на карантине."""
        async with ProductsCollector() as c:
            return await c.get_quarantine_goods(limit=limit, offset=offset)

    # ─── История цен ─────────────────────────────────────────────────────────

    async def get_price_history(self, limit: int = 100, offset: int = 0) -> dict:
        async with ProductsCollector() as c:
            return await c.get_price_upload_history(limit=limit, offset=offset)

    async def get_price_history_goods(self, upload_id: int) -> dict:
        async with ProductsCollector() as c:
            return await c.get_price_upload_goods(upload_id)

    async def get_buffer_tasks(self, limit: int = 100, offset: int = 0) -> dict:
        async with ProductsCollector() as c:
            return await c.get_price_buffer_tasks(limit=limit, offset=offset)

    async def get_buffer_goods(self, upload_id: int) -> dict:
        async with ProductsCollector() as c:
            return await c.get_price_buffer_goods(upload_id)

    # ─── Карточки ────────────────────────────────────────────────────────────

    async def get_cards(self, request: CardsListRequest | None = None, locale: str = "ru") -> CardsListResponse:
        async with ProductsCollector() as c:
            return await c.get_cards_list(request=request, locale=locale)

    async def get_trash_cards(self, locale: str = "ru") -> CardsListResponse:
        async with ProductsCollector() as c:
            return await c.get_trash_cards(locale=locale)

    async def get_cards_errors(self) -> dict:
        async with ProductsCollector() as c:
            return await c.get_cards_errors()

    async def get_cards_limits(self) -> dict:
        async with ProductsCollector() as c:
            return await c.get_cards_limits()

    async def generate_barcodes(self, count: int) -> dict:
        async with ProductsCollector() as c:
            return await c.generate_barcodes(count)

    # ─── Справочники ─────────────────────────────────────────────────────────

    async def get_parent_categories(self, locale: str = "ru") -> dict:
        async with ProductsCollector() as c:
            return await c.get_parent_categories(locale=locale)

    async def get_subjects(self, name: str | None = None, limit: int = 1000) -> SubjectsResponse:
        async with ProductsCollector() as c:
            return await c.get_subjects(name=name, limit=limit)

    async def get_subject_charcs(self, subject_id: int) -> dict:
        async with ProductsCollector() as c:
            return await c.get_subject_charcs(subject_id)

    async def get_brands(self, subject_id: int) -> BrandsResponse:
        async with ProductsCollector() as c:
            return await c.get_brands(subject_id)

    async def get_directory(self, kind: str) -> dict:
        """kind: colors | kinds | countries | seasons | vat"""
        async with ProductsCollector() as c:
            if kind == "colors":
                return await c.get_colors()
            elif kind == "kinds":
                return await c.get_kinds()
            elif kind == "countries":
                return await c.get_countries()
            elif kind == "seasons":
                return await c.get_seasons()
            elif kind == "vat":
                return await c.get_vat_rates()
            else:
                raise ValueError(f"Unknown directory: {kind}")

    # ─── Ярлыки ──────────────────────────────────────────────────────────────

    async def get_tags(self) -> dict:
        async with ProductsCollector() as c:
            return await c.get_tags()

    async def create_tag(self, name: str, color: str) -> dict:
        async with ProductsCollector() as c:
            return await c.create_tag(name=name, color=color)

    # ─── Склады ──────────────────────────────────────────────────────────────

    async def get_wb_offices(self) -> dict:
        async with ProductsCollector() as c:
            return await c.get_wb_offices()

    async def get_seller_warehouses(self) -> dict:
        async with ProductsCollector() as c:
            return await c.get_seller_warehouses()

    async def get_stocks(self, warehouse_id: int, skus: list[str]) -> dict:
        async with ProductsCollector() as c:
            return await c.get_stocks(warehouse_id=warehouse_id, skus=skus)
