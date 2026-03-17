"""
Контроллер: Маркетинг / Поисковые кластеры
WB API: advert-api.wildberries.ru
Tag: Поисковые кластеры (6 endpoints + 2 = 8 total по разным версиям, но в YAML 6)
"""
from litestar import Controller, delete, post
from src.schemas.promotion.search import (
    NormQueryGetBidsRequest, NormQueryGetMinusRequest,
    NormQueryListRequest, NormQuerySetBidsRequest,
    NormQuerySetMinusRequest, NormQueryStatsRequest, NormQueryStatsV1Request,
)
from src.services.promotion.search import SearchService


class SearchController(Controller):
    path = "/normquery"
    tags = ["Поисковые кластеры"]

    @post(
        "/stats",
        summary="Статистика поисковых кластеров (v0)",
        description=(
            "Возвращает статистику по поисковым кластерам кампаний за период.\n\n"
            "**WB endpoint:** `POST advert-api.wildberries.ru/adv/v0/normquery/stats`"
        ),
    )
    async def get_stats(self, data: NormQueryStatsRequest) -> dict:
        return await SearchService().get_stats(data)

    @post(
        "/bids/get",
        summary="Ставки по поисковым кластерам",
        description=(
            "Возвращает текущие ставки по поисковым кластерам.\n\n"
            "**WB endpoint:** `POST advert-api.wildberries.ru/adv/v0/normquery/get-bids`"
        ),
    )
    async def get_bids(self, data: NormQueryGetBidsRequest) -> dict:
        return await SearchService().get_bids(data)

    @post(
        "/bids",
        summary="Установить ставки по поисковым кластерам",
        description=(
            "Устанавливает ставки по поисковым кластерам.\n\n"
            "**WB endpoint:** `POST advert-api.wildberries.ru/adv/v0/normquery/bids`"
        ),
    )
    async def set_bids(self, data: NormQuerySetBidsRequest) -> dict:
        return await SearchService().set_bids(data)

    @delete(
        "/bids",
        status_code=200,
        summary="Удалить ставки по поисковым кластерам",
        description=(
            "Удаляет ставки по поисковым кластерам.\n\n"
            "**WB endpoint:** `DELETE advert-api.wildberries.ru/adv/v0/normquery/bids`"
        ),
    )
    async def delete_bids(self, data: NormQuerySetBidsRequest) -> dict:
        return await SearchService().delete_bids(data)

    @post(
        "/minus/get",
        summary="Минус-слова по поисковым кластерам",
        description=(
            "Возвращает минус-слова по поисковым кластерам.\n\n"
            "**WB endpoint:** `POST advert-api.wildberries.ru/adv/v0/normquery/get-minus`"
        ),
    )
    async def get_minus(self, data: NormQueryGetMinusRequest) -> dict:
        return await SearchService().get_minus(data)

    @post(
        "/minus",
        summary="Установить минус-слова по поисковым кластерам",
        description=(
            "Добавляет поисковые запросы в минус-слова кампании.\n\n"
            "**WB endpoint:** `POST advert-api.wildberries.ru/adv/v0/normquery/set-minus`"
        ),
    )
    async def set_minus(self, data: NormQuerySetMinusRequest) -> dict:
        return await SearchService().set_minus(data)

    @post(
        "/list",
        summary="Список поисковых кластеров",
        description=(
            "Возвращает список поисковых кластеров для кампаний и артикулов.\n\n"
            "**WB endpoint:** `POST advert-api.wildberries.ru/adv/v0/normquery/list`"
        ),
    )
    async def get_list(self, data: NormQueryListRequest) -> dict:
        return await SearchService().get_list(data)

    @post(
        "/stats/v1",
        summary="Статистика поисковых кластеров (v1)",
        description=(
            "Возвращает расширенную статистику по поисковым кластерам (v1 API).\n\n"
            "**WB endpoint:** `POST advert-api.wildberries.ru/adv/v1/normquery/stats`"
        ),
    )
    async def get_stats_v1(self, data: NormQueryStatsV1Request) -> dict:
        return await SearchService().get_stats_v1(data)
