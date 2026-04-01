"""Sync: Products / Карточки товаров."""
from litestar import Controller, post
from src.services.products.sync.cards import CardsSyncService
from src.utils.db_manager import DBManager


class SyncCardsController(Controller):
    path = "/cards"
    tags = ["02. Синхронизация"]

    @post(
        "/full",
        summary="Полная выгрузка карточек товаров в БД",
        description=(
            "Загружает все карточки товаров с cursor-based пагинацией и сохраняет в `wb_cards`.\n\n"
            "**WB:** `POST content-api.wildberries.ru/content/v2/get/cards/list`"
        ),
    )
    async def sync_cards_full(self) -> dict:
        async with DBManager() as db:
            return await CardsSyncService().sync_cards(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная выгрузка карточек товаров в БД",
        description=(
            "Загружает только обновлённые карточки, начиная с max(updated_at) из БД.\n\n"
            "Если БД пуста — выполняет полную синхронизацию.\n\n"
            "**WB:** `POST content-api.wildberries.ru/content/v2/get/cards/list`"
        ),
    )
    async def sync_cards_incremental(self) -> dict:
        async with DBManager() as db:
            return await CardsSyncService().sync_cards_incremental(db.session)
