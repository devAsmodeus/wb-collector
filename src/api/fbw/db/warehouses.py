"""DB: FBW / Склады WB для FBW-поставок."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.fbw.db.warehouses import FbwWarehousesDbService
from src.utils.db_manager import DBManager


class DbFbwWarehousesController(Controller):
    path = "/warehouses"
    tags = ["07. База данных"]

    @get(
        "/",
        summary="Склады WB для FBW из БД",
        description=(
            "Возвращает склады WB для FBW-поставок из таблицы `fbw_warehouses` с пагинацией.\n\n"
            "Перед первым вызовом выполните `POST /fbw/sync/warehouses/full`."
        ),
    )
    async def get_warehouses(
        self,
        limit: int = Parameter(default=500, query="limit", description="Кол-во записей (макс. 5000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await FbwWarehousesDbService().get_warehouses(db.session, limit=limit, offset=offset)
