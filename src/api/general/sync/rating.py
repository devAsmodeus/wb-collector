"""Sync: General / Рейтинг продавца."""
from litestar import Controller, post
from src.schemas.general.rating import SupplierRatingModel
from src.services.general.sync.rating import RatingSyncService
from src.utils.db_manager import DBManager


class SyncRatingController(Controller):
    path = "/rating"
    tags = ["01. Синхронизация"]

    @post(
        "/full",
        summary="Синхронизировать рейтинг продавца",
        description=(
            "Запрашивает рейтинг у WB и сохраняет/обновляет запись в таблице `wb_seller_rating`.\n\n"
            "**WB:** `GET feedbacks-api.wildberries.ru/api/common/v1/rating`"
        ),
    )
    async def sync_rating_full(self) -> SupplierRatingModel:
        async with DBManager() as db:
            return await RatingSyncService().sync_full(db.session)
