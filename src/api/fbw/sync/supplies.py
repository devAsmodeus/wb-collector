"""Sync: FBW / Поставки FBW."""
from litestar import Controller, post
from src.services.fbw.sync.supplies import FbwSuppliesSyncService
from src.utils.db_manager import DBManager


class SyncFbwSuppliesController(Controller):
    path = "/supplies"
    tags = ["07. Синхронизация"]

    @post(
        "/full",
        summary="Полная выгрузка поставок FBW в БД",
        description=(
            "Загружает все поставки FBW с товарами и сохраняет в `fbw_supplies` + `fbw_supply_goods`.\n\n"
            "Использует offset-пагинацию. Для каждой поставки загружает список товаров.\n\n"
            "**WB:** `POST marketplace-api.wildberries.ru/api/v1/supplies`\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v1/supplies/{ID}/goods`"
        ),
    )
    async def sync_supplies_full(self) -> dict:
        async with DBManager() as db:
            return await FbwSuppliesSyncService().sync_supplies_full(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная выгрузка поставок FBW в БД",
        description=(
            "Загружает поставки FBW, обновлённые после max(updated_date) из БД.\n\n"
            "Если БД пуста — выполняет полную синхронизацию.\n\n"
            "**WB:** `POST marketplace-api.wildberries.ru/api/v1/supplies`\n"
            "**WB:** `GET marketplace-api.wildberries.ru/api/v1/supplies/{ID}/goods`"
        ),
    )
    async def sync_supplies_incremental(self) -> dict:
        async with DBManager() as db:
            return await FbwSuppliesSyncService().sync_supplies_incremental(db.session)

    @post(
        "/supply-goods",
        summary="Синхронизация товаров в поставках FBW",
        description="Загружает товары для всех поставок FBW из WB API. Тяжёлая операция — 1 запрос на поставку.",
    )
    async def sync_supply_goods(self) -> dict:
        async with DBManager() as db:
            return await FbwSuppliesSyncService().sync_supply_goods(db.session)
