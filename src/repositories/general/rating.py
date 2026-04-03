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
        """Обновить или создать запись рейтинга (всегда id=1)."""
        stmt = (
            insert(WbSellerRating)
            .values(
                id=1,
                feedback_count=data.feedbackCount,
                valuation=data.valuation,
                fetched_at=datetime.utcnow(),
            )
            .on_conflict_do_update(
                index_elements=["id"],
                set_=dict(
                    feedback_count=data.feedbackCount,
                    valuation=data.valuation,
                    fetched_at=datetime.utcnow(),
                ),
            )
            .returning(WbSellerRating)
        )
        result = await self._session.execute(stmt)
        row = result.scalars().one()
        await self._session.commit()
        return SupplierRatingModel.model_validate(row, from_attributes=True)

    async def get_one_or_none(self) -> SupplierRatingModel | None:
        """Получить текущий рейтинг из БД."""
        result = await self._session.execute(
            select(WbSellerRating).where(WbSellerRating.id == 1)
        )
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return SupplierRatingModel.model_validate(row, from_attributes=True)
