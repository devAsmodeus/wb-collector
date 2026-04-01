"""DB: Маркетинг / Кампании."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.promotion.db.campaigns import CampaignsDbService
from src.utils.db_manager import DBManager


class DbCampaignsController(Controller):
    path = "/campaigns"
    tags = ["08. База данных"]

    @get(
        "/",
        summary="Кампании из БД",
        description=(
            "Возвращает рекламные кампании из таблицы `wb_campaigns` с фильтрацией.\n\n"
            "Перед первым вызовом выполните `POST /promotion/sync/campaigns/full`."
        ),
    )
    async def get_campaigns(
        self,
        status: int | None = Parameter(default=None, query="status", description="Фильтр по статусу"),
        type_: int | None = Parameter(default=None, query="type", description="Фильтр по типу кампании"),
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await CampaignsDbService().get_campaigns(
                db.session,
                status=status,
                type_=type_,
                limit=limit,
                offset=offset,
            )
