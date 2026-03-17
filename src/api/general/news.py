"""
Контроллер: General / Новости
WB API: common-api.wildberries.ru
"""
from litestar import Controller, get
from litestar.params import Parameter

from src.schemas.general.news import NewsResponse
from src.services.general.news import NewsService


class NewsController(Controller):
    path = "/news"
    tags = ["General — Новости"]

    @get(
        "/",
        summary="Новости портала продавцов",
        description=(
            "Возвращает список новостей портала продавцов WB.\n\n"
            "По умолчанию (без параметров) отдаёт новости за последние **90 дней**.\n\n"
            "Можно фильтровать по дате начала (`from_date`) "
            "или начать с конкретной новости (`from_id`).\n\n"
            "**WB endpoint:** `GET common-api.wildberries.ru/api/v1/news`"
        ),
    )
    async def get_news(
        self,
        from_date: str | None = Parameter(
            None,
            query="from_date",
            description=(
                "Дата начала выборки в формате ISO 8601 (напр. `2024-01-01`).\n"
                "Если не указана — возвращаются новости за последние 90 дней."
            ),
        ),
        from_id: int | None = Parameter(
            None,
            query="from_id",
            description=(
                "ID новости, начиная с которой вернуть список.\n"
                "Удобно для пагинации: передайте ID последней полученной новости."
            ),
        ),
    ) -> NewsResponse:
        return await NewsService().get_news(from_date=from_date, from_id=from_id)
