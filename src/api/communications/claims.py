"""
Контроллер: Коммуникации / Претензии
WB API: feedbacks-api.wildberries.ru
Tag: Возвраты покупателями (2 endpoints)
"""
from litestar import Controller, get, patch
from litestar.params import Parameter

from src.schemas.communications.claims import UpdateClaimRequest
from src.services.communications.claims import ClaimsService


class ClaimsController(Controller):
    path = "/claims"
    tags = ["Возвраты покупателями"]

    @get(
        "/",
        summary="Список претензий",
        description=(
            "Возвращает список претензий покупателей к продавцу.\n\n"
            "**WB endpoint:** `GET feedbacks-api.wildberries.ru/api/v1/claims`"
        ),
    )
    async def get_claims(
        self,
        limit: int = Parameter(10, query="take", description="Количество претензий. По умолчанию: 10."),
        offset: int = Parameter(0, query="skip", description="Смещение. По умолчанию: 0."),
    ) -> dict:
        return await ClaimsService().get_claims(limit, offset)

    @patch(
        "/",
        summary="Обработать претензию",
        description=(
            "Отвечает на претензию покупателя или отмечает её как просмотренную.\n\n"
            "**WB endpoint:** `PATCH feedbacks-api.wildberries.ru/api/v1/claim`"
        ),
    )
    async def update_claim(self, data: UpdateClaimRequest) -> dict:
        return await ClaimsService().update_claim(data)
