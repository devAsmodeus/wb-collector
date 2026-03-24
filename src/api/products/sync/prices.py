"""Sync: Products / Цены и скидки."""
from litestar import Controller, post
from src.services.products.sync.prices import PricesSyncService
from src.utils.db_manager import DBManager


class SyncPricesController(Controller):
    path = "/prices"
    tags = ["Sync / Products"]

    @post(
        "/full",
        summary="Полная выгрузка цен товаров в БД",
        description=(
            "Загружает все цены товаров с offset-based пагинацией и сохраняет в `wb_prices`.\n\n"
            "**WB:** `GET discounts-prices-api.wildberries.ru/api/v2/list/goods/filter`"
        ),
    )
    async def sync_prices_full(self) -> dict:
        async with DBManager() as db:
            return await PricesSyncService().sync_prices(db.session)
