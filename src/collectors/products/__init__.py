"""
Коллекторы: 02-products — Работа с товарами.
Хосты:
  content-api.wildberries.ru          — справочники, ярлыки, карточки, медиа
  discounts-prices-api.wildberries.ru — цены и скидки
  marketplace-api.wildberries.ru      — остатки и склады
"""
from src.collectors.base import WBApiClient
from src.config import settings
from src.collectors.products.directories import DirectoriesCollector
from src.collectors.products.tags import TagsCollector
from src.collectors.products.cards import CardsCollector
from src.collectors.products.media import MediaCollector
from src.collectors.products.prices import PricesCollector
from src.collectors.products.warehouses import WarehousesCollector


class ProductsCollector:
    """Агрегатор всех коллекторов 02-products."""

    def __init__(self):
        self._content_client = WBApiClient(base_url=settings.WB_CONTENT_URL)
        self._prices_client = WBApiClient(base_url=settings.WB_PRICES_URL)
        self._market_client = WBApiClient(base_url=settings.WB_MARKETPLACE_URL)

    async def __aenter__(self):
        await self._content_client.__aenter__()
        await self._prices_client.__aenter__()
        await self._market_client.__aenter__()
        self.directories = DirectoriesCollector(self._content_client)
        self.tags = TagsCollector(self._content_client)
        self.cards = CardsCollector(self._content_client)
        self.media = MediaCollector(self._content_client)
        self.prices = PricesCollector(self._prices_client)
        self.warehouses = WarehousesCollector(self._market_client)
        return self

    async def __aexit__(self, *args):
        await self._content_client.__aexit__(*args)
        await self._prices_client.__aexit__(*args)
        await self._market_client.__aexit__(*args)


__all__ = [
    "ProductsCollector",
    "DirectoriesCollector",
    "TagsCollector",
    "CardsCollector",
    "MediaCollector",
    "PricesCollector",
    "WarehousesCollector",
]
