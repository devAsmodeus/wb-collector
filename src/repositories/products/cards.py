"""Репозиторий: Карточки товаров."""
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.products import WbCard
from src.schemas.products.cards import ProductCard


class CardsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, cards: list[ProductCard]) -> int:
        """Вставляет или обновляет карточки товаров. Возвращает кол-во обработанных записей."""
        if not cards:
            return 0
        rows = [
            {
                "nm_id": card.nmID,
                "imt_id": card.imtID,
                "nm_uuid": card.nmUUID,
                "subject_id": card.subjectID,
                "subject_name": card.subjectName,
                "vendor_code": card.vendorCode,
                "brand": card.brand,
                "title": card.title,
                "description": card.description,
                "length": int(card.dimensions.length) if card.dimensions and card.dimensions.length is not None else None,
                "width": int(card.dimensions.width) if card.dimensions and card.dimensions.width is not None else None,
                "height": int(card.dimensions.height) if card.dimensions and card.dimensions.height is not None else None,
                "weight_brutto": card.dimensions.weightBrutto if card.dimensions else None,
                "dimensions_valid": card.dimensions.isValid if card.dimensions and hasattr(card.dimensions, 'isValid') else None,
                "sizes": [s.model_dump() for s in card.sizes] if card.sizes else None,
                "characteristics": [c.model_dump() for c in card.characteristics] if card.characteristics else None,
                "photos": [p.model_dump() for p in card.photos] if card.photos else None,
                "tags": [t.model_dump() for t in card.tags] if card.tags else None,
                "created_at": datetime.fromisoformat(card.createdAt) if card.createdAt else None,
                "updated_at": datetime.fromisoformat(card.updatedAt) if card.updatedAt else None,
                "fetched_at": datetime.utcnow(),
            }
            for card in cards
        ]
        stmt = insert(WbCard).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["nm_id"],
            set_={
                "imt_id": stmt.excluded.imt_id,
                "nm_uuid": stmt.excluded.nm_uuid,
                "subject_id": stmt.excluded.subject_id,
                "subject_name": stmt.excluded.subject_name,
                "vendor_code": stmt.excluded.vendor_code,
                "brand": stmt.excluded.brand,
                "title": stmt.excluded.title,
                "description": stmt.excluded.description,
                "length": stmt.excluded.length,
                "width": stmt.excluded.width,
                "height": stmt.excluded.height,
                "weight_brutto": stmt.excluded.weight_brutto,
                "sizes": stmt.excluded.sizes,
                "characteristics": stmt.excluded.characteristics,
                "photos": stmt.excluded.photos,
                "tags": stmt.excluded.tags,
                "created_at": stmt.excluded.created_at,
                "updated_at": stmt.excluded.updated_at,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_max_updated_at(self) -> datetime | None:
        """Возвращает максимальную дату обновления карточки из БД для инкрементальной синхронизации."""
        result = await self._session.execute(select(func.max(WbCard.updated_at)))
        return result.scalar_one_or_none()

    async def count(self) -> int:
        """Возвращает общее количество карточек товаров в БД."""
        result = await self._session.execute(select(func.count()).select_from(WbCard))
        return result.scalar_one()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[WbCard]:
        """Возвращает карточки товаров с пагинацией."""
        result = await self._session.execute(
            select(WbCard).order_by(WbCard.nm_id).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_by_nm_id(self, nm_id: int) -> WbCard | None:
        """Возвращает карточку по nm_id."""
        result = await self._session.execute(
            select(WbCard).where(WbCard.nm_id == nm_id)
        )
        return result.scalars().one_or_none()

    async def get_filtered(
        self,
        nm_ids: list[int] | None = None,
        subject_id: int | None = None,
        brand: str | None = None,
        vendor_code: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[WbCard]:
        """Возвращает карточки с фильтрацией по параметрам."""
        query = select(WbCard)
        if nm_ids:
            query = query.where(WbCard.nm_id.in_(nm_ids))
        if subject_id is not None:
            query = query.where(WbCard.subject_id == subject_id)
        if brand is not None:
            query = query.where(WbCard.brand == brand)
        if vendor_code is not None:
            query = query.where(WbCard.vendor_code == vendor_code)
        query = query.order_by(WbCard.nm_id).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())
