"""DB: FBW / Тарифы транзитной доставки."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.fbw.db.transit_tariffs import FbwTransitTariffsDbService
from src.utils.db_manager import DBManager


class DbFbwTransitTariffsController(Controller):
    path = "/transit-tariffs"
    tags = ["07. База данных"]

    @get(
        "/",
        summary="Тарифы транзита FBW из БД",
        description=(
            "Возвращает тарифы транзитной доставки FBW из таблицы `fbw_transit_tariffs` с пагинацией.\n\n"
            "Перед первым вызовом выполните `POST /fbw/sync/transit-tariffs/full`."
        ),
    )
    async def get_transit_tariffs(
        self,
        limit: int = Parameter(default=500, query="limit", description="Кол-во записей (макс. 5000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await FbwTransitTariffsDbService().get_transit_tariffs(db.session, limit=limit, offset=offset)
