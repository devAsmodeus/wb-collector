"""DB: Общее — Продавец."""
from litestar import Controller, get

from src.schemas.general.seller import SellerInfo
from src.utils.db_manager import DBManager


class DbSellerController(Controller):
    path = "/seller"
    tags = ["01. База данных"]

    @get(summary="Информация о продавце из БД")
    async def get_seller(self) -> dict:
        async with DBManager() as db:
            seller = await db.seller.get_one()
            data = [seller.model_dump()] if seller else []
            return {"data": data, "total": len(data), "limit": 1, "offset": 0}
