"""DB: FBS / Пропуска."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.fbs.db.passes import FbsPassesDbService
from src.utils.db_manager import DBManager


class DbFbsPassesController(Controller):
    path = "/passes"
    tags = ["03. База данных"]

    @get(
        "/",
        summary="Пропуска FBS из БД",
        description=(
            "Возвращает пропуска на склад WB из таблицы `fbs_passes` с фильтрацией.\n\n"
            "Перед первым вызовом выполните `POST /fbs/sync/passes/full`."
        ),
    )
    async def get_passes(
        self,
        status: str | None = Parameter(default=None, query="status", description="Фильтр по статусу"),
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await FbsPassesDbService().get_passes(
                db.session, status=status, limit=limit, offset=offset,
            )
