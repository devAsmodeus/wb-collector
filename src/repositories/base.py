import logging

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from pydantic import BaseModel

from src.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, db_session):
        self.db_session = db_session

    async def get_filtered(self, *filter_, **filter_by):
        query = select(self.model).filter(*filter_).filter_by(**filter_by)
        result = await self.db_session.execute(query)
        return [self.mapper.map_to_domain_entity(m) for m in result.scalars().all()]

    async def get_all(self):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.db_session.execute(query)
        m = result.scalars().one_or_none()
        return self.mapper.map_to_domain_entity(m) if m else None

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.db_session.execute(query)
        try:
            m = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(m)

    async def add(self, data: BaseModel):
        try:
            stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.db_session.execute(stmt)
            return self.mapper.map_to_domain_entity(result.scalars().one())
        except IntegrityError as ex:
            logging.exception(f"Insert failed: {data=}")
            raise ObjectAlreadyExistsException from ex

    async def add_bulk(self, data: list[BaseModel]):
        stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.db_session.execute(stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .filter_by(**filter_by)
        )
        await self.db_session.execute(stmt)

    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by)
        await self.db_session.execute(stmt)
