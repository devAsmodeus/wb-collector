"""WB API proxy: General / Рейтинг продавца."""
from litestar import Controller, get
from src.schemas.general.rating import SupplierRatingModel
from src.services.general.wb.rating import RatingWbService


class WbRatingController(Controller):
    path = "/rating"
    tags = ["01. API Wildberries"]

    @get(
        "/",
        summary="Рейтинг продавца (WB API)",
        description="**WB:** `GET feedbacks-api.wildberries.ru/api/common/v1/rating`",
    )
    async def get_rating(self) -> SupplierRatingModel:
        return await RatingWbService().get_rating()
