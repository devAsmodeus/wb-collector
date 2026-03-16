"""
Коллектор: 01-general
Эндпоинты:
  GET    /ping                      — проверка подключения
  GET    /api/v1/seller-info        — информация о продавце
  GET    /api/communications/v2/news — новости портала продавцов
  GET    /api/v1/users              — список пользователей продавца
  POST   /api/v1/invite             — создать приглашение
  PUT    /api/v1/users/access       — изменить права доступа
  DELETE /api/v1/user               — удалить пользователя
"""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.seller import (
    SellerInfo,
    NewsResponse,
    UsersResponse,
    InviteResponse,
)


class GeneralCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_API_BASE_URL)
        # Управление пользователями — отдельный хост + персональный токен если задан
        self._user_client = WBApiClient(
            base_url=settings.WB_USER_MGMT_URL,
            token=settings.wb_user_mgmt_token,
        )

    async def __aenter__(self):
        await self._client.__aenter__()
        await self._user_client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)
        await self._user_client.__aexit__(*args)

    async def ping(self) -> dict:
        """Проверка связи с WB API."""
        return await self._client.get("/ping")

    async def get_seller_info(self) -> SellerInfo:
        """Получить информацию о продавце."""
        data = await self._client.get("/api/v1/seller-info")
        return SellerInfo.model_validate(data)

    async def get_news(
        self,
        from_date: str | None = None,
        from_id: int | None = None,
    ) -> NewsResponse:
        """
        Получить новости портала продавцов.
        WB требует хотя бы один из параметров.
        :param from_date: дата от которой выдавать новости (ISO 8601, напр. "2024-01-01")
        :param from_id:   ID новости, начиная с которой выдавать список
        """
        params = {}
        if from_date:
            params["from"] = from_date
        if from_id is not None:
            params["fromID"] = from_id
        if not params:
            # По умолчанию — новости за последние 90 дней
            from datetime import datetime, timedelta
            params["from"] = (datetime.utcnow() - timedelta(days=90)).strftime("%Y-%m-%d")
        data = await self._client.get("/api/communications/v2/news", params=params)
        return NewsResponse.model_validate(data)

    async def get_users(
        self,
        limit: int = 100,
        offset: int = 0,
        invite_only: bool = False,
    ) -> UsersResponse:
        """
        Получить список пользователей продавца.
        Хост: user-management-api.wildberries.ru
        Примечание: требует токен с правами управления пользователями (bit 4096).
        """
        params = {"limit": limit, "offset": offset}
        if invite_only:
            params["isInviteOnly"] = "true"
        data = await self._user_client.get("/api/v1/users", params=params)
        return UsersResponse.model_validate(data)

    async def invite_user(self, payload: dict) -> InviteResponse:
        """
        Создать приглашение для нового пользователя.
        Хост: user-management-api.wildberries.ru
        """
        data = await self._user_client.post("/api/v1/invite", json=payload)
        return InviteResponse.model_validate(data)

    async def update_users_access(self, users_accesses: list[dict]) -> None:
        """
        Изменить права доступа пользователей.
        Хост: user-management-api.wildberries.ru
        """
        await self._user_client.put(
            "/api/v1/users/access",
            json={"usersAccesses": users_accesses},
        )

    async def delete_user(self, user_id: int) -> None:
        """
        Удалить пользователя по ID.
        Хост: user-management-api.wildberries.ru
        """
        await self._user_client.get("/api/v1/user", params={"deletedUserID": user_id})
