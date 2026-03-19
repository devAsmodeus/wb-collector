"""WB API proxy: General / Продавец."""
from litestar import Controller, get
from src.schemas.general.seller import SellerInfo
from src.services.general.seller import SellerService


class WbSellerController(Controller):
    path = "/seller"
    tags = ["WB / General"]

    @get(
        "/info",
        summary="Информация о продавце (WB API)",
        description="**WB:** `GET common-api.wildberries.ru/api/v1/seller-info`",
    )
    async def get_seller_info(self) -> SellerInfo:
        return await SellerService().get_seller_info()
