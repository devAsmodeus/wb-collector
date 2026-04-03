"""Коллектор: Общее — Пользователи (user-management-api)."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.general.users import GetUsersResponse, InviteRequest, InviteResponse, UpdateAccessRequest


class UsersCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_USER_MGMT_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_users(self, limit: int = 100, offset: int = 0, is_invite_only: bool | None = None) -> GetUsersResponse:
        """GET /api/v1/users — список пользователей."""
        params = {"limit": limit, "offset": offset}
        if is_invite_only is not None:
            params["isInviteOnly"] = is_invite_only
        data = await self._client.get("/api/v1/users", params=params)
        return GetUsersResponse.model_validate(data if isinstance(data, dict) else {})

    async def invite_user(self, body: InviteRequest) -> InviteResponse:
        """POST /api/v1/invite — создать приглашение."""
        data = await self._client.post("/api/v1/invite", json=body.model_dump(exclude_none=True))
        return InviteResponse.model_validate(data if isinstance(data, dict) else {})

    async def update_access(self, body: UpdateAccessRequest) -> None:
        """PUT /api/v1/users/access — изменить доступы пользователей."""
        await self._client.put("/api/v1/users/access", json=body.model_dump())

    async def delete_user(self, deleted_user_id: int) -> None:
        """DELETE /api/v1/user — удалить пользователя."""
        await self._client.delete("/api/v1/user", params={"deletedUserID": deleted_user_id})
