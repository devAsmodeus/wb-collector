"""WB API proxy: General / Подписки Джем."""
from litestar import Controller, get
from src.schemas.general.subscriptions import SubscriptionsJamInfo
from src.services.general.wb.subscriptions import SubscriptionsWbService


class WbSubscriptionsController(Controller):
    path = "/subscriptions"
    tags = ["01. API Wildberries"]

    @get(
        "/",
        summary="Подписки Джем (WB API)",
        description="**WB:** `GET common-api.wildberries.ru/api/common/v1/subscriptions`",
    )
    async def get_subscriptions(self) -> SubscriptionsJamInfo:
        return await SubscriptionsWbService().get_subscriptions()
