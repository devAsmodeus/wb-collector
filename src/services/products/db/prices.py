"""Сервис DB: Товары — Чтение цен из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.products.prices import PricesRepository
from src.services.base import BaseService


class PricesDbService(BaseService):

    async def get_prices(self, session: AsyncSession, limit: int = 100, offset: int = 0) -> dict:
        """Возвращает цены товаров из БД."""
        repo = PricesRepository(session)
        items = await repo.get_all(limit=limit, offset=offset)
        return {
            "data": [
                {
                    "nm_id": p.nm_id,
                    "vendor_code": p.vendor_code,
                    "price": float(p.price) if p.price else None,
                    "discount": p.discount,
                    "discounted_price": float(p.discounted_price) if p.discounted_price else None,
                    "club_price": float(p.club_price) if p.club_price else None,
                    "currency_iso_code": p.currency_iso_code,
                    "fetched_at": p.fetched_at.isoformat() if p.fetched_at else None,
                }
                for p in items
            ],
            "count": len(items),
        }

    async def get_price(self, session: AsyncSession, nm_id: int) -> dict | None:
        """Возвращает цену товара по nm_id."""
        repo = PricesRepository(session)
        p = await repo.get_by_nm_id(nm_id)
        if not p:
            return None
        return {
            "nm_id": p.nm_id,
            "vendor_code": p.vendor_code,
            "price": float(p.price) if p.price else None,
            "discount": p.discount,
            "discounted_price": float(p.discounted_price) if p.discounted_price else None,
            "club_price": float(p.club_price) if p.club_price else None,
            "currency_iso_code": p.currency_iso_code,
            "editable": p.editable,
            "fetched_at": p.fetched_at.isoformat() if p.fetched_at else None,
        }
