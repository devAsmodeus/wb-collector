"""
Контроллер: Маркетинг / Календарь акций
WB API: advert-api.wildberries.ru
Tag: Календарь акций (4 endpoints)
"""
from litestar import Controller, get, post

from src.schemas.promotion.calendar import UploadPromotionNomenclaturesRequest
from src.services.promotion.calendar import CalendarService


class CalendarController(Controller):
    path = "/promotions"
    tags = ["Календарь акций"]

    @get(
        "/",
        summary="Список акций",
        description=(
            "Возвращает список акций WB из календаря промоакций.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/api/v1/calendar/promotions`"
        ),
    )
    async def get_promotions(self) -> dict:
        return await CalendarService().get_promotions()

    @get(
        "/details",
        summary="Детали акции",
        description=(
            "Возвращает подробную информацию об акции: описание, условия, даты.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/api/v1/calendar/promotions/details`"
        ),
    )
    async def get_promotion_details(self) -> dict:
        return await CalendarService().get_promotion_details()

    @get(
        "/nomenclatures",
        summary="Товары для участия в акции",
        description=(
            "Возвращает список товаров продавца, которые можно добавить в акцию.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/api/v1/calendar/promotions/nomenclatures`"
        ),
    )
    async def get_promotion_nomenclatures(self) -> dict:
        return await CalendarService().get_promotion_nomenclatures()

    @post(
        "/upload",
        summary="Загрузить товары в акцию",
        description=(
            "Добавляет товары продавца в акцию с указанием акционных цен.\n\n"
            "**WB endpoint:** `POST advert-api.wildberries.ru/api/v1/calendar/promotions/upload`"
        ),
    )
    async def upload_promotion_nomenclatures(self, data: UploadPromotionNomenclaturesRequest) -> dict:
        return await CalendarService().upload_promotion_nomenclatures(data)
