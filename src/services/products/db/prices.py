"""Сервис DB: Товары — Чтение цен из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.products.prices import PricesRepository
from src.services.base import BaseService


def _price_to_dict(p) -> dict:
    return {
        "nm_id": p.nm_id,
        "vendor_code": p.vendor_code,
        "sizes": p.sizes,
        "currency_iso_code": p.currency_iso_code,
        "discount": p.discount,
        "club_discount": p.club_discount,
        "editable_size_price": p.editable_size_price,
        "is_bad_turnover": p.is_bad_turnover,
        "fetched_at": p.fetched_at.isoformat() if p.fetched_at else None,
    }


class PricesDbService(BaseService):

    async def get_prices(self, session: AsyncSession, limit: int = 100, offset: int = 0) -> dict:
        repo = PricesRepository(session)
        total = await repo.count()
        items = await repo.get_all(limit=limit, offset=offset)
        return {"data": [_price_to_dict(p) for p in items], "total": total, "limit": limit, "offset": offset}

    async def get_price(self, session: AsyncSession, nm_id: int) -> dict | None:
        repo = PricesRepository(session)
        p = await repo.get_by_nm_id(nm_id)
        return _price_to_dict(p) if p else None
