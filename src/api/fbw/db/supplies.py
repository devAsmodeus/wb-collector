"""DB: FBW / Поставки FBW."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.fbw.db.supplies import FbwSuppliesDbService
from src.utils.db_manager import DBManager


class DbFbwSuppliesController(Controller):
    path = "/supplies"
    tags = ["07. База данных"]

    @get(
        "/",
        summary="Поставки FBW из БД",
        description=(
            "Возвращает поставки FBW из таблицы `fbw_supplies` с пагинацией.\n\n"
            "Перед первым вызовом выполните `POST /fbw/sync/supplies/full`."
        ),
    )
    async def get_supplies(
        self,
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await FbwSuppliesDbService().get_supplies(db.session, limit=limit, offset=offset)

    @get(
        "/{supply_id:int}",
        summary="Поставка FBW по ID из БД",
        description=(
            "Возвращает одну поставку FBW по supply_id из таблицы `fbw_supplies` с товарами."
        ),
    )
    async def get_supply(self, supply_id: int) -> dict:
        async with DBManager() as db:
            result = await FbwSuppliesDbService().get_supply(db.session, supply_id)
            if result is None:
                return {"error": f"Supply with supply_id={supply_id} not found"}
            return result

    @get(
        "/{supply_id:int}/goods",
        summary="Товары поставки FBW из БД",
        description=(
            "Возвращает товары поставки FBW из таблицы `fbw_supply_goods` с пагинацией."
        ),
    )
    async def get_supply_goods(
        self,
        supply_id: int,
        limit: int = Parameter(default=1000, query="limit", description="Кол-во записей (макс. 5000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await FbwSuppliesDbService().get_supply_goods(db.session, supply_id, limit=limit, offset=offset)
