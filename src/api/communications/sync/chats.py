"""Sync: Communications / Чаты с покупателями."""
from litestar import Controller, post
from src.services.communications.sync.chats import ChatsSyncService
from src.utils.db_manager import DBManager


class SyncChatsController(Controller):
    path = "/chats"
    tags = ["09. Синхронизация"]

    @post(
        "/full",
        summary="Полная синхронизация чатов с покупателями",
        description=(
            "Загружает все чаты из WB API и сохраняет в `chats`.\n\n"
            "**WB:** `GET buyer-chat-api.wildberries.ru/api/v1/seller/chats`"
        ),
    )
    async def sync_chats_full(self) -> dict:
        async with DBManager() as db:
            return await ChatsSyncService().sync_chats(db.session)

    @post(
        "/incremental",
        summary="Инкрементальная синхронизация чатов",
        description="Чаты — полный snapshot, incremental = full.",
    )
    async def sync_chats_incremental(self) -> dict:
        async with DBManager() as db:
            return await ChatsSyncService().sync_chats(db.session)
