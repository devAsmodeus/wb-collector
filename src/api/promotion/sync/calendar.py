"""Sync: Маркетинг / Календарь акций."""
from litestar import Controller, post
from src.services.promotion.sync.calendar import CalendarSyncService
from src.utils.db_manager import DBManager


class SyncCalendarController(Controller):
    path = "/calendar"
    tags = ["Sync / Promotion"]

    @post(
        "/full",
        summary="Полная выгрузка акций в БД",
        description=(
            "Загружает все акции из календаря и сохраняет в `wb_promotions`.\n\n"
            "**WB:** `GET advert-api.wildberries.ru/api/v1/calendar/promotions`"
        ),
    )
    async def sync_promotions_full(self) -> dict:
        async with DBManager() as db:
            return await CalendarSyncService().sync_promotions(db.session)
