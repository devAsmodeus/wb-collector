"""Сервис: Работа с товарами — Категории, предметы, характеристики."""
from src.collectors.products import ProductsCollector
from src.services.base import BaseService


class DirectoriesService(BaseService):

    async def get_parent_categories(self, locale: str = "ru") -> dict:
        async with ProductsCollector() as c:
            return await c.directories.get_parent_categories(locale=locale)

    async def get_subjects(self, name: str | None = None, limit: int = 1000) -> dict:
        async with ProductsCollector() as c:
            return await c.directories.get_subjects(name=name, limit=limit)

    async def get_subject_charcs(self, subject_id: int) -> dict:
        async with ProductsCollector() as c:
            return await c.directories.get_subject_charcs(subject_id)

    async def get_brands(self, subject_id: int) -> dict:
        async with ProductsCollector() as c:
            return await c.directories.get_brands(subject_id)

    async def get_directory(self, kind: str) -> dict:
        """kind: colors | kinds | countries | seasons | vat"""
        async with ProductsCollector() as c:
            method = getattr(c.directories, f"get_{kind}", None)
            if method is None:
                raise ValueError(f"Unknown directory: {kind}")
            return await method()
