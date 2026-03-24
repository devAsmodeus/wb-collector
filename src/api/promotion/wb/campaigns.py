"""
Контроллер: Маркетинг / Кампании
WB API: advert-api.wildberries.ru
Tags: Кампании, Управление кампаниями, Создание кампаний (15 endpoints)
"""
from litestar import Controller, delete, get, patch, post, put
from litestar.params import Parameter

from src.schemas.promotion.campaigns import (
    CreateCampaignRequest, MinBidRequest, RenameRequest,
    UpdateBidsRequest, UpdateNmsRequest, UpdatePlacementsRequest,
)
from src.services.promotion.wb.campaigns import CampaignsService


class CampaignsController(Controller):
    path = "/"
    tags = ["Кампании"]

    @get(
        "/promotion/count",
        summary="Количество кампаний",
        description=(
            "Возвращает количество рекламных кампаний продавца по типам и статусам.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/adv/v1/promotion/count`"
        ),
    )
    async def get_count(self) -> dict:
        return await CampaignsService().get_count()

    @get(
        "/adverts",
        tags=["Кампании"],
        summary="Список кампаний",
        description=(
            "Возвращает список рекламных кампаний с фильтрацией по ID, статусу и типу оплаты.\n\n"
            "Статусы: `-1` — удалена, `4` — готова, `7` — завершена, `8` — отказ, `9` — идут показы, `11` — пауза.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/api/advert/v2/adverts`"
        ),
    )
    async def get_adverts(
        self,
        ids: str | None = Parameter(None, query="ids", description="ID кампаний через запятую. Максимум 50."),
        statuses: str | None = Parameter(None, query="statuses", description="Статусы через запятую."),
        payment_type: str | None = Parameter(None, query="payment_type", description="`cpm` или `cpc`."),
    ) -> dict:
        return await CampaignsService().get_adverts(ids, statuses, payment_type)

    @post(
        "/bids/min",
        tags=["Кампании"],
        summary="Минимальные ставки",
        description=(
            "Возвращает минимальные ставки для артикулов в кампании.\n\n"
            "**WB endpoint:** `POST advert-api.wildberries.ru/api/advert/v1/bids/min`"
        ),
    )
    async def get_min_bids(self, data: MinBidRequest) -> dict:
        return await CampaignsService().get_min_bids(data)

    @get(
        "/bids/recommendations",
        tags=["Кампании"],
        summary="Рекомендации по ставкам",
        description=(
            "Возвращает рекомендуемые ставки для артикула или кампании.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/api/advert/v0/bids/recommendations`"
        ),
    )
    async def get_bid_recommendations(
        self,
        nm_id: int | None = Parameter(None, query="nmId", description="Артикул WB."),
        advert_id: int | None = Parameter(None, query="advertId", description="ID кампании."),
    ) -> dict:
        return await CampaignsService().get_bid_recommendations(nm_id, advert_id)

    @get(
        "/subjects",
        tags=["Создание кампаний"],
        summary="Предметы для кампаний",
        description=(
            "Возвращает список доступных предметов для создания рекламных кампаний.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/adv/v1/supplier/subjects`"
        ),
    )
    async def get_subjects(
        self,
        payment_type: str | None = Parameter(None, query="payment_type", description="`cpm` или `cpc`."),
    ) -> dict:
        return await CampaignsService().get_subjects(payment_type)

    @post(
        "/nms",
        tags=["Создание кампаний"],
        summary="Доступные артикулы для кампаний",
        description=(
            "Возвращает артикулы продавца, доступные для добавления в рекламные кампании.\n\n"
            "**WB endpoint:** `POST advert-api.wildberries.ru/adv/v2/supplier/nms`"
        ),
    )
    async def get_nms(self, data: list[int]) -> dict:
        return await CampaignsService().get_nms(data)

    @post(
        "/campaign",
        tags=["Создание кампаний"],
        summary="Создать кампанию",
        description=(
            "Создаёт новую рекламную кампанию типа «Поиск + Рекомендации».\n\n"
            "**WB endpoint:** `POST advert-api.wildberries.ru/adv/v2/seacat/save-ad`"
        ),
    )
    async def create_campaign(self, data: CreateCampaignRequest) -> dict:
        return await CampaignsService().create_campaign(data)

    @get(
        "/campaign/delete",
        tags=["Управление кампаниями"],
        summary="Удалить кампанию",
        description=(
            "Удаляет рекламную кампанию по её ID.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/adv/v0/delete`"
        ),
    )
    async def delete_campaign(
        self,
        advert_id: int = Parameter(query="id", description="ID кампании для удаления"),
    ) -> dict:
        return await CampaignsService().delete_campaign(advert_id)

    @post(
        "/campaign/rename",
        tags=["Управление кампаниями"],
        summary="Переименовать кампанию",
        description=(
            "Изменяет название рекламной кампании (максимум 100 символов).\n\n"
            "**WB endpoint:** `POST advert-api.wildberries.ru/adv/v0/rename`"
        ),
    )
    async def rename_campaign(self, data: RenameRequest) -> dict:
        return await CampaignsService().rename_campaign(data)

    @get(
        "/campaign/start",
        tags=["Управление кампаниями"],
        summary="Запустить кампанию",
        description=(
            "Запускает рекламную кампанию в статусе «Готова к запуску».\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/adv/v0/start`"
        ),
    )
    async def start_campaign(
        self,
        advert_id: int = Parameter(query="id", description="ID кампании"),
    ) -> dict:
        return await CampaignsService().start_campaign(advert_id)

    @get(
        "/campaign/pause",
        tags=["Управление кампаниями"],
        summary="Поставить кампанию на паузу",
        description=(
            "Приостанавливает активную кампанию.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/adv/v0/pause`"
        ),
    )
    async def pause_campaign(
        self,
        advert_id: int = Parameter(query="id", description="ID кампании"),
    ) -> dict:
        return await CampaignsService().pause_campaign(advert_id)

    @get(
        "/campaign/stop",
        tags=["Управление кампаниями"],
        summary="Завершить кампанию",
        description=(
            "Завершает рекламную кампанию.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/adv/v0/stop`"
        ),
    )
    async def stop_campaign(
        self,
        advert_id: int = Parameter(query="id", description="ID кампании"),
    ) -> dict:
        return await CampaignsService().stop_campaign(advert_id)

    @put(
        "/auction/placements",
        tags=["Управление кампаниями"],
        summary="Обновить места размещения",
        description=(
            "Обновляет места размещения в рекламных кампаниях.\n\n"
            "**WB endpoint:** `PUT advert-api.wildberries.ru/adv/v0/auction/placements`"
        ),
    )
    async def update_placements(self, data: UpdatePlacementsRequest) -> dict:
        return await CampaignsService().update_placements(data)

    @patch(
        "/bids",
        tags=["Управление кампаниями"],
        summary="Обновить ставки",
        description=(
            "Обновляет ставки в рекламных кампаниях.\n\n"
            "**WB endpoint:** `PATCH advert-api.wildberries.ru/api/advert/v1/bids`"
        ),
    )
    async def update_bids(self, data: UpdateBidsRequest) -> dict:
        return await CampaignsService().update_bids(data)

    @patch(
        "/auction/nms",
        tags=["Управление кампаниями"],
        summary="Обновить артикулы в кампаниях",
        description=(
            "Обновляет список артикулов в рекламных кампаниях.\n\n"
            "**WB endpoint:** `PATCH advert-api.wildberries.ru/adv/v0/auction/nms`"
        ),
    )
    async def update_nms(self, data: UpdateNmsRequest) -> dict:
        return await CampaignsService().update_nms(data)
