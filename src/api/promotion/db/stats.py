"""DB: Маркетинг / Статистика кампаний."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.promotion.db.stats import StatsDbService
from src.utils.db_manager import DBManager


class DbStatsController(Controller):
    path = "/stats"
    tags = ["DB / Promotion"]

    @get(
        "/",
        summary="Статистика кампаний из БД",
        description=(
            "Возвращает статистику рекламных кампаний из таблицы `wb_campaign_stats`.\n\n"
            "Перед первым вызовом выполните `POST /promotion/sync/stats/full`."
        ),
    )
    async def get_stats(
        self,
        advert_id: int | None = Parameter(default=None, query="advert_id", description="Фильтр по ID кампании"),
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await StatsDbService().get_stats(
                db.session,
                advert_id=advert_id,
                limit=limit,
                offset=offset,
            )
