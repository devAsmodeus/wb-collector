"""Сервис WB: Общее — Управление пользователями."""
from src.collectors.general.users import UsersCollector
from src.schemas.general.users import UsersResponse, InviteResponse
from src.services.base import BaseService


class UsersWbService(BaseService):

    async def get_users(self, limit: int = 100, offset: int = 0, invite_only: bool = False) -> UsersResponse:
        async with UsersCollector() as c:
            return await c.get_users(limit=limit, offset=offset, invite_only=invite_only)

    async def invite_user(self, payload: dict) -> InviteResponse:
        async with UsersCollector() as c:
            return await c.invite_user(payload)

    async def update_users_access(self, users_accesses: list[dict]) -> None:
        async with UsersCollector() as c:
            await c.update_users_access(users_accesses)

    async def delete_user(self, user_id: int) -> None:
        async with UsersCollector() as c:
            await c.delete_user(user_id)
