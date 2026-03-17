"""
Контроллер: Коммуникации / Закреплённые отзывы
WB API: feedbacks-api.wildberries.ru
Tag: Закреплённые отзывы (5 endpoints)
"""
from litestar import Controller, delete, get, post
from litestar.params import Parameter

from src.schemas.communications.pins import PinFeedbackRequest, UnpinFeedbackRequest
from src.services.communications.pins import PinsService


class PinsController(Controller):
    path = "/pins"
    tags = ["Закреплённые отзывы"]

    @get(
        "/",
        summary="Список закреплённых отзывов",
        description=(
            "Возвращает список закреплённых отзывов продавца с опциональной фильтрацией по артикулу.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/feedbacks/v1/pins`"
        ),
    )
    async def get_list(
        self,
        nm_id: int | None = Parameter(None, query="nmId", description="Фильтр по артикулу WB."),
    ) -> dict:
        return await PinsService().get_list(nm_id)

    @post(
        "/",
        summary="Закрепить отзыв",
        description=(
            "Закрепляет отзыв к указанному артикулу WB.\n\n"
            "**WB endpoint:** `POST feedbacks-api.wildberries.ru/api/feedbacks/v1/pins`"
        ),
    )
    async def pin(self, data: PinFeedbackRequest) -> dict:
        return await PinsService().pin(data)

    @delete(
        "/",
        status_code=200,
        summary="Открепить отзыв",
        description=(
            "Открепляет закреплённый отзыв.\n\n"
            "**WB endpoint:** `DELETE feedbacks-api.wildberries.ru/api/feedbacks/v1/pins`"
        ),
    )
    async def unpin(self, data: UnpinFeedbackRequest) -> dict:
        return await PinsService().unpin(data)

    @get(
        "/count",
        summary="Количество закреплённых отзывов",
        description=(
            "Возвращает текущее количество закреплённых отзывов.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/feedbacks/v1/pins/count`"
        ),
    )
    async def get_count(self) -> dict:
        return await PinsService().get_count()

    @get(
        "/limits",
        summary="Лимиты закреплённых отзывов",
        description=(
            "Возвращает лимиты и использованные слоты для закреплённых отзывов.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/feedbacks/v1/pins/limits`"
        ),
    )
    async def get_limits(self) -> dict:
        return await PinsService().get_limits()
