"""DB: General / Рейтинг продавца."""
from litestar import Controller, get
from src.schemas.general.rating import SupplierRatingModel
from src.services.general.db.rating import RatingDbService
from src.utils.db_manager import DBManager


class DbRatingController(Controller):
    path = "/rating"
    tags = ["01. База данных"]

    @get(
        "/",
        summary="Рейтинг продавца из БД",
        description=(
            "Возвращает рейтинг продавца из таблицы `wb_seller_rating`.\n\n"
            "Перед первым вызовом выполните `POST /general/sync/rating/full`."
        ),
    )
    async def get_rating(self) -> SupplierRatingModel | None:
        async with DBManager() as db:
            return await RatingDbService().get_rating(db.session)
