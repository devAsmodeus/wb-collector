"""DB: Analytics / Остатки по группам."""
from datetime import date

from litestar import Controller, get
from litestar.params import Parameter
from src.services.analytics.db.stocks import StocksDbService
from src.utils.db_manager import DBManager


class DbStocksController(Controller):
    path = "/stocks"
    tags = ["11. База данных"]

    @get(
        "/",
        summary="Остатки по группам из БД",
        description=(
            "Возвращает аналитику остатков из таблицы `analytics_stocks_groups` с фильтрацией.\n\n"
            "Перед первым вызовом выполните `POST /analytics/sync/stocks/full`."
        ),
    )
    async def get_stocks(
        self,
        nm_id: int | None = Parameter(default=None, query="nm_id", description="Фильтр по nm_id"),
        date_from: date | None = Parameter(default=None, query="date_from", description="Дата начала (YYYY-MM-DD)"),
        date_to: date | None = Parameter(default=None, query="date_to", description="Дата окончания (YYYY-MM-DD)"),
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await StocksDbService().get_stocks(
                db.session,
                nm_id=nm_id,
                date_from=date_from,
                date_to=date_to,
                limit=limit,
                offset=offset,
            )
