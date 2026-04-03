"""Репозиторий: Рейтинг продавца."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.seller import WbSellerRating
from src.schemas.general.rating import SupplierRatingModel


class RatingRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert(self, data: SupplierRatingModel) -> SupplierRatingModel:
        """Вставить или обновить запись рейтинга (всегда id=1)."""
        stmt = (
            insert(WbSellerRating)
            .values(
                id=1,
                current=data.current,
                wb_rating=data.wbRating,
                delivery_speed=data.deliverySpeed,
                quality_goods=data.qualityGoods,
                service_review=data.serviceReview,
                fetched_at=datetime.utcnow(),
            )
            .on_conflict_do_update(
                index_elements=["id"],
                set_=dict(
                    current=data.current,
                    wb_rating=data.wbRating,
                    delivery_speed=data.deliverySpeed,
                    quality_goods=data.qualityGoods,
                    service_review=data.serviceReview,
                    fetched_at=datetime.utcnow(),
                ),
            )
            .returning(WbSellerRating)
        )
        result = await self._session.execute(stmt)
        row = result.scalars().one()
        return SupplierRatingModel.model_validate(row, from_attributes=True)

    async def get_one_or_none(self) -> SupplierRatingModel | None:
        """Возвращает текущий рейтинг из БД (или None если пусто)."""
        result = await self._session.execute(
            select(WbSellerRating).where(WbSellerRating.id == 1)
        )
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return SupplierRatingModel.model_validate(row, from_attributes=True)
