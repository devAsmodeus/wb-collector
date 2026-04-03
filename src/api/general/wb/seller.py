"""WB API proxy: Общее — Продавец."""
from litestar import Controller, get

from src.schemas.general.seller import SellerInfo
from src.services.general.wb.seller import SellerWbService


class WbSellerController(Controller):
    path = "/seller"
    tags = ["01. API Wildberries"]

    @get(summary="Информация о продавце (WB API)")
    async def get_seller_info(self) -> SellerInfo:
        return await SellerWbService().get_seller_info()
