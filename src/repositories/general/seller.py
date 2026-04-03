from sqlalchemy.dialects.postgresql import insert

from src.models.seller import SellerOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import SellerMapper
from src.schemas.general.seller import SellerInfo


class SellerRepository(BaseRepository):
    model = SellerOrm
    mapper = SellerMapper

    async def upsert(self, data: SellerInfo) -> SellerInfo:
        """Вставить или обновить запись по sid."""
        stmt = (
            insert(SellerOrm)
            .values(
                sid=data.sid,
                name=data.name,
                trade_mark=data.tradeMark,
                tin=data.tin,
            )
            .on_conflict_do_update(
                index_elements=["sid"],
                set_=dict(
                    name=data.name,
                    trade_mark=data.tradeMark,
                    tin=data.tin,
                ),
            )
            .returning(SellerOrm)
        )
        result = await self.db_session.execute(stmt)
        return self.mapper.map_to_domain_entity(result.scalars().one())
