"""
Контроллер: General / Ping
WB API: все хосты поддерживают /ping
"""
from litestar import Controller, get

from src.services.general.seller import SellerService


class PingController(Controller):
    path = "/ping"
    tags = ["General — Ping"]

    @get(
        "/",
        summary="Проверка подключения к WB API",
        description=(
            "Проверяет доступность WB API (common-api.wildberries.ru).\n\n"
            "**WB endpoint:** `GET common-api.wildberries.ru/ping`"
        ),
    )
    async def ping(self) -> dict:
        return await SellerService().ping()
