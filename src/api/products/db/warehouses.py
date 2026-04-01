"""DB: Products / Склады."""
from litestar import Controller, get
from src.services.products.db.warehouses import WarehousesDbService
from src.utils.db_manager import DBManager


class DbWarehousesController(Controller):
    path = "/warehouses"
    tags = ["02. База данных"]

    @get(
        "/",
        summary="Склады продавца из БД",
        description=(
            "Возвращает все склады продавца из таблицы `wb_warehouses`.\n\n"
            "Перед первым вызовом выполните `POST /products/sync/warehouses/full`."
        ),
    )
    async def get_warehouses(self) -> dict:
        async with DBManager() as db:
            return await WarehousesDbService().get_warehouses(db.session)
