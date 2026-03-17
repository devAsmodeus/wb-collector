"""
Контроллер: General / Пользователи
WB API: user-management-api.wildberries.ru

⚠️  Требует токен с разрешением «Управление пользователями» (WB_PERSONAL_TOKEN).
"""
from litestar import Controller, delete, get, post, put
from litestar.params import Parameter
from litestar.status_codes import HTTP_204_NO_CONTENT

from src.schemas.general.users import (
    InviteResponse,
    InviteUserRequest,
    UpdateAccessRequest,
    UsersResponse,
)
from src.services.general.users import UsersService


class UsersController(Controller):
    path = "/users"
    tags = ["General — Пользователи"]

    @get(
        "/",
        summary="Список пользователей кабинета",
        description=(
            "Возвращает список пользователей кабинета продавца с их ролями и статусами.\n\n"
            "Поддерживает пагинацию через `limit` / `offset` "
            "и фильтрацию по приглашённым (`invite_only`).\n\n"
            "⚠️ **Требует** токен `WB_PERSONAL_TOKEN` с разрешением «Управление пользователями».\n\n"
            "**WB endpoint:** `GET user-management-api.wildberries.ru/api/v1/users`"
        ),
    )
    async def get_users(
        self,
        limit: int = Parameter(
            100,
            query="limit",
            ge=1,
            le=1000,
            description="Количество пользователей в ответе. Диапазон: 1–1000. По умолчанию: 100.",
        ),
        offset: int = Parameter(
            0,
            query="offset",
            ge=0,
            description="Смещение для пагинации (сколько записей пропустить). По умолчанию: 0.",
        ),
        invite_only: bool = Parameter(
            False,
            query="invite_only",
            description="Если `true` — вернуть только приглашённых пользователей, ещё не принявших инвайт.",
        ),
    ) -> UsersResponse:
        return await UsersService().get_users(
            limit=limit,
            offset=offset,
            invite_only=invite_only,
        )

    @post(
        "/invite",
        summary="Создать приглашение для нового пользователя",
        description=(
            "Создаёт ссылку-приглашение для добавления нового пользователя в кабинет продавца.\n\n"
            "Укажите `phone` **или** `email` — хотя бы одно поле обязательно.\n\n"
            "⚠️ **Требует** токен `WB_PERSONAL_TOKEN` с разрешением «Управление пользователями».\n\n"
            "**WB endpoint:** `POST user-management-api.wildberries.ru/api/v1/invite`"
        ),
    )
    async def invite_user(self, data: InviteUserRequest) -> InviteResponse:
        return await UsersService().invite_user(data.model_dump(exclude_none=True))

    @put(
        "/access",
        status_code=HTTP_204_NO_CONTENT,
        summary="Изменить права доступа пользователей",
        description=(
            "Обновляет роли и статусы доступа для одного или нескольких пользователей.\n\n"
            "Максимум **100 записей** за один запрос.\n\n"
            "⚠️ **Требует** токен `WB_PERSONAL_TOKEN` с разрешением «Управление пользователями».\n\n"
            "**WB endpoint:** `PUT user-management-api.wildberries.ru/api/v1/users/access`"
        ),
    )
    async def update_users_access(self, data: UpdateAccessRequest) -> None:
        await UsersService().update_users_access(
            [a.model_dump() for a in data.usersAccesses]
        )

    @delete(
        "/{user_id:int}",
        status_code=HTTP_204_NO_CONTENT,
        summary="Удалить пользователя из кабинета",
        description=(
            "Удаляет пользователя по его ID из кабинета продавца.\n\n"
            "Операция необратима. Владельца кабинета удалить нельзя.\n\n"
            "⚠️ **Требует** токен `WB_PERSONAL_TOKEN` с разрешением «Управление пользователями».\n\n"
            "**WB endpoint:** `DELETE user-management-api.wildberries.ru/api/v1/user`"
        ),
    )
    async def delete_user(
        self,
        user_id: int = Parameter(description="ID пользователя, которого нужно удалить"),
    ) -> None:
        await UsersService().delete_user(user_id)
