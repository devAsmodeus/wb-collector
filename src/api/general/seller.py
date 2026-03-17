"""
Контроллер: General / Продавец
WB API: common-api.wildberries.ru
"""
from litestar import Controller, get, post

from src.schemas.general.seller import SellerInfo
from src.services.general.seller import SellerService
from src.utils.db_manager import DBManager


class SellerController(Controller):
    path = "/seller"
    tags = ["General — Продавец"]

    @get(
        "/ping",
        summary="Ping WB API",
        description=(
            "Проверяет доступность WB API.\n\n"
            "**WB endpoint:** `GET common-api.wildberries.ru/ping`"
        ),
    )
    async def ping(self) -> dict:
        return await SellerService().ping()

    @post(
        "/sync",
        summary="Синхронизировать инфо о продавце",
        description=(
            "Запрашивает инфо о продавце из WB API и сохраняет в БД.\n\n"
            "**WB endpoint:** `GET common-api.wildberries.ru/api/v1/seller-info`"
        ),
    )
    async def sync_seller_info(self) -> SellerInfo:
        return await SellerService(db=DBManager()).sync_seller_info()

    @get(
        "/info",
        summary="Инфо о продавце из БД",
        description=(
            "Возвращает последние сохранённые данные о продавце из БД.\n\n"
            "Перед первым вызовом выполните `POST /general/seller/sync`."
        ),
    )
    async def get_seller_info(self) -> SellerInfo:
        async with DBManager() as db:
            return await db.seller.get_one()
