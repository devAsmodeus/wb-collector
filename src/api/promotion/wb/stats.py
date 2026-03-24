"""
Контроллер: Маркетинг / Статистика + Медиа
WB API: advert-api.wildberries.ru
Tags: Статистика (4 ep), Медиа (3 ep)
"""
from litestar import Controller, get, post
from litestar.params import Parameter

from src.schemas.promotion.stats import CampaignStatsRequest
from src.services.promotion.wb.stats import StatsService


class StatsController(Controller):
    path = "/"
    tags = ["Статистика"]

    @get(
        "/fullstats",
        summary="Полная статистика кампаний",
        description=(
            "Возвращает детальную статистику по кампаниям за период.\n\n"
            "Максимум **50 кампаний** за запрос.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/adv/v3/fullstats`"
        ),
    )
    async def get_fullstats(
        self,
        ids: str = Parameter(query="ids", description="ID кампаний через запятую. Максимум 50."),
        begin_date: str | None = Parameter(None, query="beginDate", description="Дата начала в формате `YYYY-MM-DD`."),
        end_date: str | None = Parameter(None, query="endDate", description="Дата окончания в формате `YYYY-MM-DD`."),
    ) -> dict:
        return await StatsService().get_fullstats(ids, begin_date, end_date)

    @post(
        "/stats",
        summary="Статистика кампаний (детализированная)",
        description=(
            "Возвращает детализированную статистику кампаний с разбивкой по интервалам.\n\n"
            "**WB endpoint:** `POST advert-api.wildberries.ru/adv/v1/stats`"
        ),
    )
    async def get_stats(self, data: CampaignStatsRequest) -> dict:
        return await StatsService().get_stats(data)

    @get(
        "/media/count",
        tags=["Медиа"],
        summary="Количество медиакампаний",
        description=(
            "Возвращает количество медиакампаний продавца по статусам и типам.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/adv/v1/count`"
        ),
    )
    async def get_media_count(self) -> dict:
        return await StatsService().get_media_count()

    @get(
        "/media/adverts",
        tags=["Медиа"],
        summary="Список медиакампаний",
        description=(
            "Возвращает список медиакампаний с фильтрацией по статусу и типу.\n\n"
            "Типы: `1` — по дням, `2` — по просмотрам.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/adv/v1/adverts`"
        ),
    )
    async def get_media_adverts(
        self,
        status: int | None = Parameter(None, query="status", description="Статус: `1`-черновик, `2`-модерация, `3`-отклонена, `4`-активна, `5`-завершена."),
        type_: int | None = Parameter(None, query="type", description="Тип: `1`-по дням, `2`-по просмотрам."),
        limit: int = Parameter(50, query="limit", description="Количество кампаний. По умолчанию: 50."),
        offset: int = Parameter(0, query="offset", description="Смещение. По умолчанию: 0."),
        order: str | None = Parameter(None, query="order", description="`create` — по дате создания, `change` — по дате изменения."),
        direction: str | None = Parameter(None, query="direction", description="`asc` или `desc`."),
    ) -> dict:
        return await StatsService().get_media_adverts(status, type_, limit, offset, order, direction)

    @get(
        "/media/advert",
        tags=["Медиа"],
        summary="Информация о медиакампании",
        description=(
            "Возвращает детальную информацию о медиакампании.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/adv/v1/advert`"
        ),
    )
    async def get_media_advert(
        self,
        advert_id: int = Parameter(query="id", description="ID медиакампании"),
    ) -> dict:
        return await StatsService().get_media_advert(advert_id)
