from fastapi import APIRouter, Query

from src.schemas.seller import SellerInfo, NewsResponse, UsersResponse, InviteResponse
from src.services.general import GeneralService
from src.utils.db_manager import DBManager

router = APIRouter(prefix="/general", tags=["01 — General"])


# ─── Ping ────────────────────────────────────────────────────────────────────

@router.get("/ping", summary="Проверить подключение к WB API")
async def ping():
    svc = GeneralService()
    return await svc.ping()


# ─── Seller info ─────────────────────────────────────────────────────────────

@router.post(
    "/seller-info/sync",
    response_model=SellerInfo,
    summary="Получить инфо о продавце из WB и сохранить в БД",
)
async def sync_seller_info():
    svc = GeneralService(db=DBManager())
    return await svc.sync_seller_info()


@router.get(
    "/seller-info",
    response_model=SellerInfo,
    summary="Получить сохранённую инфо о продавце из БД",
)
async def get_seller_info():
    async with DBManager() as db:
        return await db.seller.get_one()


# ─── Новости ─────────────────────────────────────────────────────────────────

@router.get(
    "/news",
    response_model=NewsResponse,
    summary="Новости портала продавцов",
)
async def get_news(
    from_date: str | None = Query(None, description="Дата от (ISO 8601), напр. 2024-01-01"),
    from_id: int | None = Query(None, description="ID новости, начиная с которой выдать список"),
):
    svc = GeneralService()
    return await svc.get_news(from_date=from_date, from_id=from_id)


# ─── Пользователи ────────────────────────────────────────────────────────────

@router.get(
    "/users",
    response_model=UsersResponse,
    summary="Список пользователей продавца",
)
async def get_users(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    invite_only: bool = Query(False, description="Только приглашённые (не активировавшие доступ)"),
):
    svc = GeneralService()
    return await svc.get_users(limit=limit, offset=offset, invite_only=invite_only)


@router.post(
    "/users/invite",
    response_model=InviteResponse,
    summary="Создать приглашение для нового пользователя",
)
async def invite_user(payload: dict):
    svc = GeneralService()
    return await svc.invite_user(payload)


@router.put(
    "/users/access",
    status_code=204,
    summary="Изменить права доступа пользователей",
)
async def update_users_access(body: dict):
    svc = GeneralService()
    await svc.update_users_access(body.get("usersAccesses", []))


@router.delete(
    "/users/{user_id}",
    status_code=204,
    summary="Удалить пользователя",
)
async def delete_user(user_id: int):
    svc = GeneralService()
    await svc.delete_user(user_id)
