"""DB: FBS / Поставки."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.fbs.db.supplies import FbsSuppliesDbService
from src.utils.db_manager import DBManager


class DbFbsSuppliesController(Controller):
    path = "/supplies"
    tags = ["03. База данных"]

    @get(
        "/",
        summary="Поставки FBS из БД",
        description=(
            "Возвращает поставки FBS из таблицы `fbs_supplies` с фильтрацией.\n\n"
            "Перед первым вызовом выполните `POST /fbs/sync/supplies/full`."
        ),
    )
    async def get_supplies(
        self,
        done: bool | None = Parameter(default=None, query="done", description="Фильтр по статусу done"),
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await FbsSuppliesDbService().get_supplies(
                db.session, done=done, limit=limit, offset=offset,
            )
