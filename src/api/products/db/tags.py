"""DB: Products / Теги."""
from litestar import Controller, get
from src.services.products.db.tags import TagsDbService
from src.utils.db_manager import DBManager


class DbTagsController(Controller):
    path = "/tags"
    tags = ["DB / Products"]

    @get(
        "/",
        summary="Теги из БД",
        description=(
            "Возвращает все теги из таблицы `wb_tags`.\n\n"
            "Перед первым вызовом выполните `POST /products/sync/tags/full`."
        ),
    )
    async def get_tags(self) -> dict:
        async with DBManager() as db:
            return await TagsDbService().get_tags(db.session)
