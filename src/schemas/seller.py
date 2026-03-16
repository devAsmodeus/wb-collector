from datetime import datetime
from pydantic import BaseModel


class SellerInfo(BaseModel):
    """Информация о продавце (GET /api/v1/seller-info)."""
    name: str
    sid: str
    tradeMark: str
    itn: str | None = None


# ─── Новости ─────────────────────────────────────────────────────────────────

class NewsTag(BaseModel):
    id: int
    name: str


class NewsItem(BaseModel):
    id: int
    header: str
    content: str
    date: str
    types: list[NewsTag] = []


class NewsResponse(BaseModel):
    data: list[NewsItem] = []


# ─── Пользователи ────────────────────────────────────────────────────────────

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


# ─── Приглашение ─────────────────────────────────────────────────────────────

class InviteResponse(BaseModel):
    inviteID: str
    expiredAt: str
    isSuccess: bool
    inviteUrl: str
