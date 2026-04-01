"""Sync: Маркетинг / Кампании."""
from litestar import Controller, post
from src.services.promotion.sync.campaigns import CampaignsSyncService
from src.utils.db_manager import DBManager


class SyncCampaignsController(Controller):
    path = "/campaigns"
    tags = ["08. Синхронизация"]

    @post(
        "/full",
        summary="Полная выгрузка кампаний в БД",
        description=(
            "Загружает все рекламные кампании и сохраняет в `wb_campaigns`.\n\n"
            "**WB:** `GET advert-api.wildberries.ru/api/advert/v2/adverts`"
        ),
    )
    async def sync_campaigns_full(self) -> dict:
        async with DBManager() as db:
            return await CampaignsSyncService().sync_campaigns(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная выгрузка кампаний в БД",
        description=(
            "Кампании могут изменяться в любой момент — инкрементальная = полная синхронизация.\n\n"
            "**WB:** `GET advert-api.wildberries.ru/api/advert/v2/adverts`"
        ),
    )
    async def sync_campaigns_incremental(self) -> dict:
        async with DBManager() as db:
            return await CampaignsSyncService().sync_campaigns_incremental(db.session)
