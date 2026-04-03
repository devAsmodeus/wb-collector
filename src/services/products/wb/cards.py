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

    async def update_cards(self, cards: list) -> dict:
        async with ProductsCollector() as c:
            return await c.cards.update_cards(cards)

    async def move_cards(self, target_imt: int, nm_ids: list) -> dict:
        async with ProductsCollector() as c:
            return await c.cards.move_cards(target_imt_id=target_imt, nm_ids=nm_ids)

    async def delete_cards_to_trash(self, nm_ids: list) -> dict:
        async with ProductsCollector() as c:
            return await c.cards.delete_cards_to_trash(nm_ids)

    async def recover_cards(self, nm_ids: list) -> dict:
        async with ProductsCollector() as c:
            return await c.cards.recover_cards(nm_ids)

    async def upload_cards(self, cards: list) -> dict:
        async with ProductsCollector() as c:
            return await c.cards.create_cards(cards)

    async def upload_add_cards(self, cards: list) -> dict:
        async with ProductsCollector() as c:
            return await c.cards.create_cards_with_attach(imt_id=0, cards_to_add=cards)
