"""Роутер: Работа с товарами — Ярлыки."""
from fastapi import APIRouter
from src.services.products.tags import TagsService

router = APIRouter()
svc = TagsService()


@router.get("/tags", summary="Список ярлыков")
async def get_tags():
    return await svc.get_tags()


@router.post("/tags", summary="Создать ярлык")
async def create_tag(name: str, color: str):
    return await svc.create_tag(name=name, color=color)


@router.patch("/tags/{tag_id}", summary="Изменить ярлык")
async def update_tag(tag_id: int, name: str | None = None, color: str | None = None):
    return await svc.update_tag(tag_id=tag_id, name=name, color=color)


@router.delete("/tags/{tag_id}", summary="Удалить ярлык")
async def delete_tag(tag_id: int):
    return await svc.delete_tag(tag_id)


@router.post("/tags/link", summary="Привязать ярлыки к карточке")
async def link_tags(nm_id: int, tag_ids: list[int]):
    return await svc.link_tags(nm_id=nm_id, tag_ids=tag_ids)
