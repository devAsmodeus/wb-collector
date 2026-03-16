"""Роутер: Общее — Управление пользователями."""
from fastapi import APIRouter, Query
from src.schemas.general.users import UsersResponse, InviteResponse
from src.services.general.users import UsersService

router = APIRouter()


@router.get("/users", response_model=UsersResponse, summary="Список пользователей продавца")
async def get_users(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    invite_only: bool = Query(False),
):
    return await UsersService().get_users(limit=limit, offset=offset, invite_only=invite_only)


@router.post("/users/invite", response_model=InviteResponse, summary="Создать приглашение")
async def invite_user(payload: dict):
    return await UsersService().invite_user(payload)


@router.put("/users/access", status_code=204, summary="Изменить права доступа")
async def update_users_access(body: dict):
    await UsersService().update_users_access(body.get("usersAccesses", []))


@router.delete("/users/{user_id}", status_code=204, summary="Удалить пользователя")
async def delete_user(user_id: int):
    await UsersService().delete_user(user_id)
