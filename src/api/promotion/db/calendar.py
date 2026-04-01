"""DB: Маркетинг / Календарь акций."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.promotion.db.calendar import CalendarDbService
from src.utils.db_manager import DBManager


class DbCalendarController(Controller):
    path = "/calendar"
    tags = ["08. База данных"]

    @get(
        "/",
        summary="Акции из БД",
        description=(
            "Возвращает акции из таблицы `wb_promotions`.\n\n"
            "Перед первым вызовом выполните `POST /promotion/sync/calendar/full`."
        ),
    )
    async def get_promotions(
        self,
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await CalendarDbService().get_promotions(
                db.session,
                limit=limit,
                offset=offset,
            )
