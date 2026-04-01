"""DB: General / Продавец."""
from litestar import Controller, get
from src.schemas.general.seller import SellerInfo
from src.services.general.db.seller import SellerDbService
from src.utils.db_manager import DBManager


class DbSellerController(Controller):
    path = "/seller"
    tags = ["01. База данных"]

    @get(
        "/",
        summary="Информация о продавце из БД",
        description=(
            "Возвращает данные о продавце из таблицы `sellers`.\n\n"
            "Перед первым вызовом выполните `POST /general/sync/seller/full`."
        ),
    )
    async def get_seller(self) -> SellerInfo:
        async with DBManager() as db:
            return await SellerDbService().get_seller(db)
