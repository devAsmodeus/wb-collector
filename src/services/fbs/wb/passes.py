"""Сервис WB: FBS — Пропуска."""
from src.collectors.fbs.passes import PassesCollector
from src.schemas.fbs.passes import PassOfficesResponse, PassesResponse, Pass, CreatePassRequest, UpdatePassRequest
from src.services.base import BaseService


class PassesService(BaseService):

    async def get_pass_offices(self) -> PassOfficesResponse:
        async with PassesCollector() as c:
            return await c.get_pass_offices()

    async def get_passes(self) -> PassesResponse:
        async with PassesCollector() as c:
            return await c.get_passes()

    async def create_pass(self, data: CreatePassRequest) -> Pass:
        async with PassesCollector() as c:
            return await c.create_pass(data.model_dump())

    async def update_pass(self, pass_id: int, data: UpdatePassRequest) -> dict:
        async with PassesCollector() as c:
            return await c.update_pass(pass_id, data.model_dump(exclude_none=True))

    async def delete_pass(self, pass_id: int) -> None:
        async with PassesCollector() as c:
            await c.delete_pass(pass_id)
