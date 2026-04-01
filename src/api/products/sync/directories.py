"""Sync: Products / Справочники (категории, предметы)."""
from litestar import Controller, post
from src.services.products.sync.directories import DirectoriesSyncService
from src.utils.db_manager import DBManager


class SyncDirectoriesController(Controller):
    path = "/directories"
    tags = ["02. Синхронизация"]

    @post(
        "/categories",
        summary="Синхронизировать родительские категории",
        description=(
            "Загружает родительские категории товаров и сохраняет в `wb_categories`.\n\n"
            "**WB:** `GET content-api.wildberries.ru/content/v2/object/parent/all`"
        ),
    )
    async def sync_categories(self) -> dict:
        async with DBManager() as db:
            return await DirectoriesSyncService().sync_categories(db.session)

    @post(
        "/subjects",
        summary="Синхронизировать предметы (подкатегории)",
        description=(
            "Загружает предметы (подкатегории) товаров и сохраняет в `wb_subjects`.\n\n"
            "**WB:** `GET content-api.wildberries.ru/content/v2/object/all`"
        ),
    )
    async def sync_subjects(self) -> dict:
        async with DBManager() as db:
            return await DirectoriesSyncService().sync_subjects(db.session)

    @post(
        "/categories/incremental",
        summary="Инкрементальная синхронизация категорий",
        description=(
            "Категории — справочные данные, инкрементальная = полная синхронизация.\n\n"
            "**WB:** `GET content-api.wildberries.ru/content/v2/object/parent/all`"
        ),
    )
    async def sync_categories_incremental(self) -> dict:
        async with DBManager() as db:
            return await DirectoriesSyncService().sync_categories_incremental(db.session)

    @post(
        "/subjects/incremental",
        summary="Инкрементальная синхронизация предметов",
        description=(
            "Предметы — справочные данные, инкрементальная = полная синхронизация.\n\n"
            "**WB:** `GET content-api.wildberries.ru/content/v2/object/all`"
        ),
    )
    async def sync_subjects_incremental(self) -> dict:
        async with DBManager() as db:
            return await DirectoriesSyncService().sync_subjects_incremental(db.session)
