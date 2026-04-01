"""Sync: Communications / Претензии."""
from litestar import Controller, post
from src.services.communications.sync.claims import ClaimsSyncService
from src.utils.db_manager import DBManager


class SyncClaimsController(Controller):
    path = "/claims"
    tags = ["09. Синхронизация"]

    @post(
        "/full",
        summary="Полная выгрузка претензий в БД",
        description=(
            "Загружает все претензии с пагинацией и сохраняет в `wb_claims`.\n\n"
            "**WB:** `GET feedbacks-api.wildberries.ru/api/v1/claims`"
        ),
    )
    async def sync_claims_full(self) -> dict:
        async with DBManager() as db:
            return await ClaimsSyncService().sync_claims(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная выгрузка претензий в БД",
        description=(
            "Claims API возвращает только последние 14 дней. Инкрементальная = полная синхронизация.\n\n"
            "**WB:** `GET feedbacks-api.wildberries.ru/api/v1/claims`"
        ),
    )
    async def sync_claims_incremental(self) -> dict:
        async with DBManager() as db:
            result = await ClaimsSyncService().sync_claims(db.session)
            result["source"] = "incremental"
            return result
