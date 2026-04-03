"""Репозиторий: Подписки Джем."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.seller import WbSellerSubscription
from src.schemas.general.subscriptions import SubscriptionsJamInfo


class SubscriptionsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert(self, data: SubscriptionsJamInfo) -> SubscriptionsJamInfo:
        """Обновить или создать запись подписки (всегда id=1)."""
        stmt = (
            insert(WbSellerSubscription)
            .values(
                id=1,
                state=data.state,
                activation_source=data.activationSource,
                level=data.level,
                since=data.since,
                till=data.till,
                fetched_at=datetime.utcnow(),
            )
            .on_conflict_do_update(
                index_elements=["id"],
                set_=dict(
                    state=data.state,
                    activation_source=data.activationSource,
                    level=data.level,
                    since=data.since,
                    till=data.till,
                    fetched_at=datetime.utcnow(),
                ),
            )
            .returning(WbSellerSubscription)
        )
        result = await self._session.execute(stmt)
        row = result.scalars().one()
        await self._session.commit()
        return SubscriptionsJamInfo.model_validate(row, from_attributes=True)

    async def get_one_or_none(self) -> SubscriptionsJamInfo | None:
        """Получить текущую подписку из БД."""
        result = await self._session.execute(
            select(WbSellerSubscription).where(WbSellerSubscription.id == 1)
        )
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return SubscriptionsJamInfo.model_validate(row, from_attributes=True)
