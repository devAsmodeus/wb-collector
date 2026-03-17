"""
Контроллер: Маркетинг / Финансы
WB API: advert-api.wildberries.ru
Tag: Финансы (5 endpoints)
"""
from litestar import Controller, get, post
from litestar.params import Parameter

from src.schemas.promotion.finance import DepositRequest
from src.services.promotion.finance import FinanceService


class FinanceController(Controller):
    path = "/"
    tags = ["Финансы"]

    @get(
        "/balance",
        summary="Баланс рекламного кабинета",
        description=(
            "Возвращает текущий баланс рекламного кабинета: счёт, баланс, бонусы и промо-бонусы.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/adv/v1/balance`"
        ),
    )
    async def get_balance(self) -> dict:
        return await FinanceService().get_balance()

    @get(
        "/budget",
        summary="Бюджет кампании",
        description=(
            "Возвращает текущий бюджет рекламной кампании.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/adv/v1/budget`"
        ),
    )
    async def get_budget(
        self,
        advert_id: int = Parameter(query="id", description="ID рекламной кампании"),
    ) -> dict:
        return await FinanceService().get_budget(advert_id)

    @post(
        "/budget/deposit",
        summary="Пополнить бюджет кампании",
        description=(
            "Пополняет бюджет рекламной кампании из счёта, баланса или бонусов.\n\n"
            "Источники: `0` — счёт, `1` — баланс, `3` — бонусы.\n\n"
            "**WB endpoint:** `POST advert-api.wildberries.ru/adv/v1/budget/deposit`"
        ),
    )
    async def deposit_budget(
        self,
        data: DepositRequest,
        advert_id: int = Parameter(query="id", description="ID рекламной кампании"),
    ) -> dict:
        return await FinanceService().deposit_budget(advert_id, data)

    @get(
        "/upd",
        summary="УПД (универсальный передаточный документ)",
        description=(
            "Возвращает список УПД по рекламным кампаниям за указанный период.\n\n"
            "Минимальный интервал: 1 день. Максимальный: 31 день.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/adv/v1/upd`"
        ),
    )
    async def get_upd(
        self,
        date_from: str = Parameter(query="from", description="Начало периода в формате `YYYY-MM-DD`."),
        date_to: str = Parameter(query="to", description="Конец периода в формате `YYYY-MM-DD`. Макс. интервал — 31 день."),
    ) -> dict:
        return await FinanceService().get_upd(date_from, date_to)

    @get(
        "/payments",
        summary="История платежей",
        description=(
            "Возвращает историю платежей по рекламным кампаниям за период.\n\n"
            "Минимальный интервал: 1 день. Максимальный: 31 день.\n\n"
            "**WB endpoint:** `GET advert-api.wildberries.ru/adv/v1/payments`"
        ),
    )
    async def get_payments(
        self,
        date_from: str = Parameter(query="from", description="Начало периода в формате `YYYY-MM-DD`."),
        date_to: str = Parameter(query="to", description="Конец периода в формате `YYYY-MM-DD`. Макс. интервал — 31 день."),
    ) -> dict:
        return await FinanceService().get_payments(date_from, date_to)
