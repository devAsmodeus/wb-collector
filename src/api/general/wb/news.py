"""WB API proxy: General / Новости."""
from litestar import Controller, get
from litestar.params import Parameter
from src.schemas.general.news import NewsResponse
from src.services.general.wb.news import NewsWbService


class WbNewsController(Controller):
    path = "/news"
    tags = ["WB / General"]

    @get(
        "/",
        summary="Новости портала продавцов (WB API)",
        description=(
            "**WB:** `GET common-api.wildberries.ru/api/communications/v2/news`\n\n"
            "По умолчанию — последние 90 дней."
        ),
    )
    async def get_news(
        self,
        from_date: str | None = Parameter(None, query="from_date", description="Дата начала ISO 8601"),
        from_id: int | None = Parameter(None, query="from_id", description="ID новости (пагинация)"),
    ) -> NewsResponse:
        return await NewsWbService().get_news(from_date=from_date, from_id=from_id)
