"""Sync: Общее — Пользователи."""
from litestar import Controller, post

from src.services.general.sync.users import UsersSyncService
from src.utils.db_manager import DBManager


class SyncUsersController(Controller):
    path = "/users"
    tags = ["01. Синхронизация"]

    @post("/full", summary="Полная синхронизация пользователей WB → БД")
    async def sync_users_full(self) -> dict:
        async with DBManager() as db:
            return await UsersSyncService().sync_users_full(db.session)

    @post("/incremental", summary="Инкрементальная синхронизация пользователей WB → БД")
    async def sync_users_incremental(self) -> dict:
        async with DBManager() as db:
            return await UsersSyncService().sync_users_incremental(db.session)
