"""Схемы: Общее — Управление пользователями продавца."""
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Вложенные схемы
# ---------------------------------------------------------------------------

class UserInviteeInfo(BaseModel):
    """Информация о приглашении пользователя."""

    inviteID: str | None = Field(None, description="Уникальный ID приглашения")
    expiredAt: str | None = Field(None, description="Дата истечения приглашения (ISO 8601)")
    inviteUrl: str | None = Field(None, description="Ссылка-приглашение для отправки пользователю")


class UserAccess(BaseModel):
    """Права доступа одного пользователя."""

    userID: int = Field(description="ID пользователя")
    role: str = Field(
        description=(
            "Роль пользователя. Возможные значения: "
            "`admin` — полный доступ, "
            "`manager` — управление товарами, "
            "`analyst` — только просмотр аналитики."
        )
    )
    isActive: bool = Field(default=True, description="Активен ли доступ пользователя")


# ---------------------------------------------------------------------------
# Response схемы
# ---------------------------------------------------------------------------

class User(BaseModel):
    """Пользователь кабинета продавца."""

    id: int = Field(description="Уникальный ID пользователя")
    role: str | None = Field(None, description="Роль в кабинете (admin, manager, analyst и др.)")
    position: str | None = Field(None, description="Должность пользователя")
    phone: str | None = Field(None, description="Номер телефона")
    email: str | None = Field(None, description="Email адрес")
    isOwner: bool = Field(default=False, description="Является ли пользователь владельцем кабинета")
    firstName: str | None = Field(None, description="Имя")
    secondName: str | None = Field(None, description="Фамилия")
    patronymic: str | None = Field(None, description="Отчество")
    goodsReturn: bool = Field(default=False, description="Разрешён ли возврат товаров")
    isInvitee: bool = Field(default=False, description="Приглашённый пользователь (ещё не принял инвайт)")
    inviteeInfo: UserInviteeInfo | None = Field(
        None,
        description="Данные приглашения — заполнены только если isInvitee=true"
    )


class UsersResponse(BaseModel):
    """Ответ на запрос списка пользователей."""

    total: int = Field(description="Общее количество пользователей в кабинете")
    countInResponse: int = Field(description="Количество пользователей в текущем ответе (с учётом limit/offset)")
    users: list[User] = Field(default=[], description="Список пользователей")


class InviteResponse(BaseModel):
    """Ответ на создание приглашения."""

    inviteID: str = Field(description="Уникальный ID созданного приглашения")
    expiredAt: str = Field(description="Срок действия приглашения (ISO 8601)")
    isSuccess: bool = Field(description="Успешно ли создано приглашение")
    inviteUrl: str = Field(description="Ссылка-приглашение для отправки новому пользователю")


# ---------------------------------------------------------------------------
# Request схемы
# ---------------------------------------------------------------------------

class InviteUserRequest(BaseModel):
    """Тело запроса для создания приглашения нового пользователя."""

    phone: str | None = Field(
        None,
        description="Номер телефона приглашаемого (формат +7XXXXXXXXXX). Обязателен если не указан email.",
    )
    email: str | None = Field(
        None,
        description="Email приглашаемого. Обязателен если не указан phone.",
    )
    role: str = Field(
        description=(
            "Роль нового пользователя: "
            "`admin` — полный доступ, "
            "`manager` — управление товарами, "
            "`analyst` — только просмотр."
        )
    )


class UpdateAccessRequest(BaseModel):
    """Тело запроса для изменения прав доступа пользователей."""

    usersAccesses: list[UserAccess] = Field(
        description="Список пользователей с новыми правами. Максимум 100 записей за запрос.",
        min_length=1,
        max_length=100,
    )
