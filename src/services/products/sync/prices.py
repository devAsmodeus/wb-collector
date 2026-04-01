"""Сервис Sync: Товары — Синхронизация цен и скидок."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.collectors.products import ProductsCollector
from src.repositories.products.prices import PricesRepository
from src.services.base import BaseService

logger = logging.getLogger(__name__)


class PricesSyncService(BaseService):

    async def sync_prices(self, session: AsyncSession) -> dict:
        """
        Полная выгрузка всех цен товаров.
        Использует offset-based пагинацию: запрашиваем по limit записей,
        увеличивая offset, пока API возвращает данные.
        """
        repo = PricesRepository(session)
        all_prices = []
        limit = 100
        offset = 0

        async with ProductsCollector() as collector:
            while True:
                response = await collector.prices.get_goods_list(limit=limit, offset=offset)
                items = response.data.listGoods if response.data else []

                if not items:
                    break

                all_prices.extend(items)
                offset += limit

        saved = await repo.upsert_many(all_prices)
        logger.info(f"Prices synced: {saved} prices saved")
        return {"synced": saved, "source": "full"}

    async def sync_prices_incremental(self, session: AsyncSession) -> dict:
        """
        Инкрементальная синхронизация цен.
        Цены — справочные данные без фильтрации по дате в API.
        Incremental = full sync (upsert обновит изменённые цены).
        """
        result = await self.sync_prices(session)
        result["source"] = "incremental"
        return result
