"""Sync: Products / Карточки товаров."""
from litestar import Controller, post
from src.services.products.sync.cards import CardsSyncService
from src.utils.db_manager import DBManager


class SyncCardsController(Controller):
    path = "/cards"
    tags = ["Sync / Products"]

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
