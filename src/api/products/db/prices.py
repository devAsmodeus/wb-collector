"""DB: Products / Цены."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.products.db.prices import PricesDbService
from src.utils.db_manager import DBManager


class DbPricesController(Controller):
    path = "/prices"
    tags = ["DB / Products"]

    @get(
        "/",
        summary="Цены товаров из БД",
        description=(
            "Возвращает цены товаров из таблицы `wb_prices` с пагинацией.\n\n"
            "Перед первым вызовом выполните `POST /products/sync/prices/full`."
        ),
    )
    async def get_prices(
        self,
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await PricesDbService().get_prices(db.session, limit=limit, offset=offset)

    @get(
        "/{nm_id:int}",
        summary="Цена товара по nm_id из БД",
        description="Возвращает цену товара по nm_id из таблицы `wb_prices`.",
    )
    async def get_price(self, nm_id: int) -> dict:
        async with DBManager() as db:
            result = await PricesDbService().get_price(db.session, nm_id)
            if result is None:
                return {"error": f"Price with nm_id={nm_id} not found"}
            return result
