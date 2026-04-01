"""Сервис: Работа с товарами — Ярлыки."""
from src.collectors.products import ProductsCollector
from src.services.base import BaseService


class TagsService(BaseService):

    async def get_tags(self) -> dict:
        async with ProductsCollector() as c:
            return await c.tags.get_tags()

    async def create_tag(self, name: str, color: str) -> dict:
        async with ProductsCollector() as c:
            return await c.tags.create_tag(name=name, color=color)

    async def update_tag(self, tag_id: int, name: str | None = None, color: str | None = None) -> dict:
        async with ProductsCollector() as c:
            return await c.tags.update_tag(tag_id=tag_id, name=name, color=color)

    async def delete_tag(self, tag_id: int) -> dict:
        async with ProductsCollector() as c:
            return await c.tags.delete_tag(tag_id)

    async def link_tags(self, nm_id: int, tag_ids: list[int]) -> dict:
        async with ProductsCollector() as c:
            return await c.tags.link_tags_to_card(nm_id=nm_id, tag_ids=tag_ids)
