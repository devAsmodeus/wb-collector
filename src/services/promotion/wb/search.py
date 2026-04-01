"""Сервис: Маркетинг — Поисковые кластеры."""
from src.collectors.promotion.search import SearchCollector
from src.schemas.promotion.search import (
    NormQueryStatsRequest, NormQueryGetBidsRequest, NormQuerySetBidsRequest,
    NormQueryGetMinusRequest, NormQuerySetMinusRequest,
    NormQueryListRequest, NormQueryStatsV1Request,
)
from src.services.base import BaseService


class SearchService(BaseService):
    async def get_stats(self, data: NormQueryStatsRequest) -> dict:
        async with SearchCollector() as c:
            return await c.get_normquery_stats(data.model_dump(by_alias=True))

    async def get_bids(self, data: NormQueryGetBidsRequest) -> dict:
        async with SearchCollector() as c: return await c.get_normquery_bids(data.model_dump())

    async def set_bids(self, data: NormQuerySetBidsRequest) -> dict:
        async with SearchCollector() as c: return await c.set_normquery_bids(data.model_dump())

    async def delete_bids(self, data: NormQuerySetBidsRequest) -> dict:
        async with SearchCollector() as c: return await c.delete_normquery_bids(data.model_dump())

    async def get_minus(self, data: NormQueryGetMinusRequest) -> dict:
        async with SearchCollector() as c: return await c.get_normquery_minus(data.model_dump())

    async def set_minus(self, data: NormQuerySetMinusRequest) -> dict:
        async with SearchCollector() as c: return await c.set_normquery_minus(data.model_dump())

    async def get_list(self, data: NormQueryListRequest) -> dict:
        async with SearchCollector() as c: return await c.get_normquery_list(data.model_dump())

    async def get_stats_v1(self, data: NormQueryStatsV1Request) -> dict:
        async with SearchCollector() as c:
            return await c.get_normquery_stats_v1(data.model_dump(by_alias=True))
