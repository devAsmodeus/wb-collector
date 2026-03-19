"""WB API proxy: General / Ping."""
from litestar import Controller, get
from src.services.general.seller import SellerService


class WbPingController(Controller):
    path = "/ping"
    tags = ["WB / General"]

    @get(
        "/",
        summary="Проверка подключения к WB API",
        description="**WB:** `GET common-api.wildberries.ru/ping`",
    )
    async def ping(self) -> dict:
        return await SellerService().ping()
