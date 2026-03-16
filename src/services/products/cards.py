"""Сервис: Работа с товарами — Карточки товаров."""
from src.collectors.products import ProductsCollector
from src.schemas.products.cards import CardsListRequest
from src.services.base import BaseService


class CardsService(BaseService):

    async def get_cards(self, request: CardsListRequest | None = None, locale: str = "ru") -> dict:
        async with ProductsCollector() as c:
            return await c.cards.get_cards_list(request=request, locale=locale)

    async def get_cards_errors(self) -> dict:
        async with ProductsCollector() as c:
            return await c.cards.get_cards_errors()

    async def get_trash_cards(self, locale: str = "ru") -> dict:
        async with ProductsCollector() as c:
            return await c.cards.get_trash_cards(locale=locale)

    async def get_cards_limits(self) -> dict:
        async with ProductsCollector() as c:
            return await c.cards.get_cards_limits()

    async def generate_barcodes(self, count: int) -> dict:
        async with ProductsCollector() as c:
            return await c.cards.generate_barcodes(count)
