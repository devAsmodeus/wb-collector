"""Схемы: Общее — Пользователи (user-management-api)."""
from pydantic import BaseModel


class UserInviteeInfo(BaseModel):
    """Информация о приглашении пользователя."""
    inviteID: str | None = None
    expiredAt: str | None = None


class User(BaseModel):
    """Пользователь из GET /api/v1/users."""
    id: int | None = None
    role: str | None = None
    position: str | None = None
    phone: str | None = None
    email: str | None = None
    isOwner: bool | None = None
    firstName: str | None = None
    secondName: str | None = None
    patronymic: str | None = None
    goodsReturn: bool | None = None
    isInvitee: bool | None = None
    inviteeInfo: UserInviteeInfo | None = None
    access: list | None = None


# Алиас для единообразия
UserItem = User


class UsersResponse(BaseModel):
    """Ответ GET /api/v1/users."""
    total: int
    countInResponse: int
    users: list[User]


# Алиас
GetUsersResponse = UsersResponse


class InviteRequest(BaseModel):
    """Тело POST /api/v1/invite."""
    access: list | None = None
    invite: dict


class InviteResponse(BaseModel):
    """Ответ POST /api/v1/invite."""
    inviteID: str
    expiredAt: str
    isSuccess: bool
    inviteUrl: str


class UpdateAccessRequest(BaseModel):
    """Тело PUT /api/v1/users/access."""
    usersAccesses: list[dict]
