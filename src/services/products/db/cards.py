"""Сервис DB: Товары — Чтение карточек товаров из БД."""
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.products.cards import CardsRepository
from src.services.base import BaseService


class CardsDbService(BaseService):

    async def get_cards(
        self,
        session: AsyncSession,
        nm_ids: list[int] | None = None,
        subject_id: int | None = None,
        brand: str | None = None,
        vendor_code: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Возвращает карточки товаров из БД с фильтрацией."""
        repo = CardsRepository(session)
        items = await repo.get_filtered(
            nm_ids=nm_ids,
            subject_id=subject_id,
            brand=brand,
            vendor_code=vendor_code,
            limit=limit,
            offset=offset,
        )
        return {
            "data": [
                {
                    "nm_id": c.nm_id,
                    "imt_id": c.imt_id,
                    "vendor_code": c.vendor_code,
                    "brand": c.brand,
                    "title": c.title,
                    "subject_id": c.subject_id,
                    "subject_name": c.subject_name,
                    "created_at": c.created_at.isoformat() if c.created_at else None,
                    "updated_at": c.updated_at.isoformat() if c.updated_at else None,
                }
                for c in items
            ],
            "count": len(items),
        }

    async def get_card(self, session: AsyncSession, nm_id: int) -> dict | None:
        """Возвращает одну карточку товара по nm_id."""
        repo = CardsRepository(session)
        card = await repo.get_by_nm_id(nm_id)
        if not card:
            return None
        return {
            "nm_id": card.nm_id,
            "imt_id": card.imt_id,
            "nm_uuid": card.nm_uuid,
            "vendor_code": card.vendor_code,
            "brand": card.brand,
            "title": card.title,
            "description": card.description,
            "subject_id": card.subject_id,
            "subject_name": card.subject_name,
            "sizes": card.sizes,
            "characteristics": card.characteristics,
            "photos": card.photos,
            "tags": card.tags,
            "created_at": card.created_at.isoformat() if card.created_at else None,
            "updated_at": card.updated_at.isoformat() if card.updated_at else None,
            "fetched_at": card.fetched_at.isoformat() if card.fetched_at else None,
        }
