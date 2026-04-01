"""Репозиторий: Цены и скидки товаров."""
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.products import WbPrice
from src.schemas.products.prices import GoodsItem


class PricesRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, prices: list[GoodsItem]) -> int:
        """Вставляет или обновляет цены товаров. Возвращает кол-во обработанных записей."""
        if not prices:
            return 0
        rows = [
            {
                "nm_id": item.nmID,
                "vendor_code": item.vendorCode,
                "price": item.sizes[0].price / 100 if item.sizes and item.sizes[0].price else None,
                "discount": item.discount,
                "discounted_price": item.sizes[0].discountedPrice / 100 if item.sizes and item.sizes[0].discountedPrice else None,
                "club_price": item.sizes[0].clubDiscountedPrice / 100 if item.sizes and item.sizes[0].clubDiscountedPrice else None,
                "currency_iso_code": item.currencyIsoCode4217,
                "editable": item.editableSizePrice,
                "fetched_at": datetime.utcnow(),
            }
            for item in prices
        ]
        stmt = insert(WbPrice).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["nm_id"],
            set_={
                "vendor_code": stmt.excluded.vendor_code,
                "price": stmt.excluded.price,
                "discount": stmt.excluded.discount,
                "discounted_price": stmt.excluded.discounted_price,
                "club_price": stmt.excluded.club_price,
                "currency_iso_code": stmt.excluded.currency_iso_code,
                "editable": stmt.excluded.editable,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_max_fetched_at(self) -> datetime | None:
        """Возвращает максимальную дату синхронизации цен из БД."""
        result = await self._session.execute(select(func.max(WbPrice.fetched_at)))
        return result.scalar_one_or_none()

    async def count(self) -> int:
        """Возвращает общее количество цен в БД."""
        result = await self._session.execute(select(func.count()).select_from(WbPrice))
        return result.scalar_one()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[WbPrice]:
        """Возвращает цены товаров с пагинацией."""
        result = await self._session.execute(
            select(WbPrice).order_by(WbPrice.nm_id).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_by_nm_id(self, nm_id: int) -> WbPrice | None:
        """Возвращает цену по nm_id."""
        result = await self._session.execute(
            select(WbPrice).where(WbPrice.nm_id == nm_id)
        )
        return result.scalars().one_or_none()
