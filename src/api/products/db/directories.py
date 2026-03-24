"""DB: Products / Справочники (категории, предметы)."""
from litestar import Controller, get
from src.services.products.db.directories import DirectoriesDbService
from src.utils.db_manager import DBManager


class DbDirectoriesController(Controller):
    path = "/directories"
    tags = ["DB / Products"]

    @get(
        "/categories",
        summary="Категории из БД",
        description=(
            "Возвращает все родительские категории из таблицы `wb_categories`.\n\n"
            "Перед первым вызовом выполните `POST /products/sync/directories/categories`."
        ),
    )
    async def get_categories(self) -> dict:
        async with DBManager() as db:
            return await DirectoriesDbService().get_categories(db.session)

    @get(
        "/subjects",
        summary="Предметы из БД",
        description=(
            "Возвращает все предметы (подкатегории) из таблицы `wb_subjects`.\n\n"
            "Перед первым вызовом выполните `POST /products/sync/directories/subjects`."
        ),
    )
    async def get_subjects(self) -> dict:
        async with DBManager() as db:
            return await DirectoriesDbService().get_subjects(db.session)
