"""Sync: Products / Теги."""
from litestar import Controller, post
from src.services.products.sync.tags import TagsSyncService
from src.utils.db_manager import DBManager


class SyncTagsController(Controller):
    path = "/tags"
    tags = ["Sync / Products"]

    @post(
        "/full",
        summary="Полная выгрузка тегов в БД",
        description=(
            "Загружает все теги продавца и сохраняет в `wb_tags`.\n\n"
            "**WB:** `GET content-api.wildberries.ru/content/v2/tags`"
        ),
    )
    async def sync_tags_full(self) -> dict:
        async with DBManager() as db:
            return await TagsSyncService().sync_tags(db.session)
