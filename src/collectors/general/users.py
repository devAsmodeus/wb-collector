"""Коллектор: Общее — Управление пользователями."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.general.users import UsersResponse, InviteResponse


class UsersCollector:
    def __init__(self):
        self._client = WBApiClient(
            base_url=settings.WB_USER_MGMT_URL,
            token=settings.wb_user_mgmt_token,
        )

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_users(
        self,
        limit: int = 100,
        offset: int = 0,
        invite_only: bool = False,
    ) -> UsersResponse:
        """
        GET /api/v1/users — список пользователей продавца.
        Хост: user-management-api.wildberries.ru
        ⚠️ Требует токен с правами управления пользователями.
        """
        params = {"limit": limit, "offset": offset}
        if invite_only:
            params["isInviteOnly"] = "true"
        data = await self._client.get("/api/v1/users", params=params)
        return UsersResponse.model_validate(data)

    async def invite_user(self, payload: dict) -> InviteResponse:
        """
        POST /api/v1/invite — создать приглашение.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        data = await self._client.post("/api/v1/invite", json=payload)
        return InviteResponse.model_validate(data)

    async def update_users_access(self, users_accesses: list[dict]) -> None:
        """
        PUT /api/v1/users/access — изменить права доступа.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        await self._client.put(
            "/api/v1/users/access",
            json={"usersAccesses": users_accesses},
        )

    async def delete_user(self, user_id: int) -> None:
        """
        DELETE /api/v1/user — удалить пользователя.
        ⚠️ ИЗМЕНЯЕТ РЕАЛЬНЫЕ ДАННЫЕ.
        """
        await self._client.delete("/api/v1/user", params={"deletedUserID": user_id})
