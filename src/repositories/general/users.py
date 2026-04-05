"""Репозиторий: Пользователи продавца."""
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.seller import WbUser
from src.schemas.general.users import UserItem


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_many(self, users: list[UserItem]) -> int:
        """Вставить или обновить пользователей."""
        if not users:
            return 0
        rows = [
            {
                "id": u.id,
                "role": u.role,
                "position": u.position,
                "phone": u.phone,
                "email": u.email,
                "is_owner": u.isOwner,
                "first_name": u.firstName,
                "second_name": u.secondName,
                "patronymic": u.patronymic,
                "goods_return": u.goodsReturn,
                "is_invitee": u.isInvitee,
                "invitee_info": u.inviteeInfo.model_dump() if u.inviteeInfo and hasattr(u.inviteeInfo, 'model_dump') else u.inviteeInfo,
                "access": [a.model_dump() if hasattr(a, 'model_dump') else a for a in u.access] if u.access else None,
                "fetched_at": datetime.utcnow(),
            }
            for u in users if u.id is not None
        ]
        if not rows:
            return 0
        stmt = (
            insert(WbUser)
            .values(rows)
            .on_conflict_do_update(
                index_elements=["id"],
                set_={k: getattr(insert(WbUser).excluded, k) for k in rows[0] if k != "id"},
            )
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return len(rows)

    async def get_many(self, limit: int = 100, offset: int = 0) -> list[UserItem]:
        result = await self._session.execute(
            select(WbUser).order_by(WbUser.id).limit(limit).offset(offset)
        )
        return [UserItem.model_validate(row, from_attributes=True) for row in result.scalars().all()]

    async def count(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(WbUser))
        return result.scalar_one()
