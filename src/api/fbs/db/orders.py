"""DB: FBS / Сборочные задания."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.fbs.db.orders import FbsOrdersDbService
from src.utils.db_manager import DBManager


class DbFbsOrdersController(Controller):
    path = "/orders"
    tags = ["03. База данных"]

    @get(
        "/",
        summary="Сборочные задания FBS из БД",
        description=(
            "Возвращает сборочные задания FBS из таблицы `fbs_orders` с фильтрацией.\n\n"
            "Перед первым вызовом выполните `POST /fbs/sync/orders/full`."
        ),
    )
    async def get_orders(
        self,
        date_from: str | None = Parameter(default=None, query="date_from", description="Начало периода (ISO 8601)"),
        date_to: str | None = Parameter(default=None, query="date_to", description="Конец периода (ISO 8601)"),
        status: str | None = Parameter(default=None, query="status", description="Фильтр по supplierStatus"),
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await FbsOrdersDbService().get_orders(
                db.session,
                date_from=date_from,
                date_to=date_to,
                status=status,
                limit=limit,
                offset=offset,
            )
