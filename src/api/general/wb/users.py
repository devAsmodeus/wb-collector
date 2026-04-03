"""WB API proxy: Общее — Пользователи."""
from litestar import Controller, get, post, put, delete
from litestar.params import Parameter

from src.collectors.general.users import UsersCollector
from src.schemas.general.users import GetUsersResponse, InviteRequest, InviteResponse, UpdateAccessRequest


class WbUsersController(Controller):
    path = "/users"
    tags = ["01. API Wildberries"]

    @get(summary="Получить список пользователей (WB API)")
    async def get_users(
        self,
        limit: int = Parameter(default=100, query="limit"),
        offset: int = Parameter(default=0, query="offset"),
        is_invite_only: bool | None = Parameter(default=None, query="isInviteOnly"),
    ) -> GetUsersResponse:
        async with UsersCollector() as c:
            return await c.get_users(limit=limit, offset=offset, is_invite_only=is_invite_only)

    @post("/invite", summary="Создать приглашение для нового пользователя (WB API)")
    async def invite_user(self, data: InviteRequest) -> InviteResponse:
        async with UsersCollector() as c:
            return await c.invite_user(data)

    @put("/access", summary="Изменить доступы пользователей (WB API)")
    async def update_access(self, data: UpdateAccessRequest) -> dict:
        async with UsersCollector() as c:
            await c.update_access(data)
        return {"status": "ok"}

    @delete(
        "/{user_id:int}",
        summary="Удалить пользователя (WB API)",
        status_code=200,
    )
    async def delete_user(self, user_id: int) -> dict:
        async with UsersCollector() as c:
            await c.delete_user(user_id)
        return {"status": "ok"}
