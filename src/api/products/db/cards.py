"""DB: Products / Карточки товаров."""
from litestar import Controller, get
from litestar.params import Parameter
from src.services.products.db.cards import CardsDbService
from src.utils.db_manager import DBManager


class DbCardsController(Controller):
    path = "/cards"
    tags = ["DB / Products"]

    @get(
        "/",
        summary="Карточки товаров из БД",
        description=(
            "Возвращает карточки товаров из таблицы `wb_cards` с фильтрацией.\n\n"
            "Перед первым вызовом выполните `POST /products/sync/cards/full`."
        ),
    )
    async def get_cards(
        self,
        nm_ids: list[int] | None = Parameter(default=None, query="nm_ids", description="Фильтр по nm_id (список)"),
        subject_id: int | None = Parameter(default=None, query="subject_id", description="Фильтр по subject_id"),
        brand: str | None = Parameter(default=None, query="brand", description="Фильтр по бренду"),
        vendor_code: str | None = Parameter(default=None, query="vendor_code", description="Фильтр по артикулу продавца"),
        limit: int = Parameter(default=100, query="limit", description="Кол-во записей (макс. 1000)"),
        offset: int = Parameter(default=0, query="offset", description="Смещение"),
    ) -> dict:
        async with DBManager() as db:
            return await CardsDbService().get_cards(
                db.session,
                nm_ids=nm_ids,
                subject_id=subject_id,
                brand=brand,
                vendor_code=vendor_code,
                limit=limit,
                offset=offset,
            )

    @get(
        "/{nm_id:int}",
        summary="Карточка товара по nm_id из БД",
        description="Возвращает одну карточку товара по nm_id из таблицы `wb_cards`.",
    )
    async def get_card(self, nm_id: int) -> dict:
        async with DBManager() as db:
            result = await CardsDbService().get_card(db.session, nm_id)
            if result is None:
                return {"error": f"Card with nm_id={nm_id} not found"}
            return result
