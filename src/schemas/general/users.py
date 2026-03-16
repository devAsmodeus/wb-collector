"""Схемы: Общее — Управление пользователями."""
from pydantic import BaseModel


class UserInviteeInfo(BaseModel):
    inviteID: str | None = None
    expiredAt: str | None = None
    inviteUrl: str | None = None


class User(BaseModel):
    id: int
    role: str | None = None
    position: str | None = None
    phone: str | None = None
    email: str | None = None
    isOwner: bool = False
    firstName: str | None = None
    secondName: str | None = None
    patronymic: str | None = None
    goodsReturn: bool = False
    isInvitee: bool = False
    inviteeInfo: UserInviteeInfo | None = None


class UsersResponse(BaseModel):
    total: int
    countInResponse: int
    users: list[User] = []


class InviteResponse(BaseModel):
    inviteID: str
    expiredAt: str
    isSuccess: bool
    inviteUrl: str
