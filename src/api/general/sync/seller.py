"""Sync: General / Продавец."""
from litestar import Controller, post
from src.schemas.general.seller import SellerInfo
from src.services.general.sync.seller import SellerSyncService
from src.utils.db_manager import DBManager


class SyncSellerController(Controller):
    path = "/seller"
    tags = ["Sync / General"]

    @post(
        "/full",
        summary="Синхронизировать информацию о продавце",
        description=(
            "Запрашивает данные у WB и сохраняет/обновляет запись в таблице `sellers`.\n\n"
            "Запускать при первом старте и при изменении реквизитов.\n\n"
            "**WB:** `GET common-api.wildberries.ru/api/v1/seller-info`"
        ),
    )
    async def sync_seller_full(self) -> SellerInfo:
        return await SellerSyncService(db=DBManager()).sync_seller_info()
