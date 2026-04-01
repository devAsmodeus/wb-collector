"""DB: Analytics / Воронка продаж."""
from datetime import date

from litestar import Controller, get
from litestar.params import Parameter
from src.services.analytics.db.funnel import FunnelDbService
from src.utils.db_manager import DBManager


class DbFunnelController(Controller):
    path = "/funnel"
    tags = ["11. База данных"]

    @get(
        "/",
        summary="Воронка продаж из БД",
        description=(
            "Возвращает данные воронки продаж из таблицы `analytics_funnel_products` с фильтрацией.\n\n"
            "Перед первым вызовом выполните `POST /analytics/sync/funnel/full`."
        ),
    )
    async def get_funnel(
        self,
        nm_id: int | None = Parameter(default=None, query="nm_id", description="Фильтр по nm_id"),
        date_from: date | None = Parameter(default=None, query="date_from", description="Дата начала (YYYY-MM-DD)"),
        date_to: date | None = Parameter(default=None, query="date_to", description="Дата окончания (YYYY-MM-DD)"),
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await FunnelDbService().get_funnel(
                db.session,
                nm_id=nm_id,
                date_from=date_from,
                date_to=date_to,
                limit=limit,
                offset=offset,
            )
