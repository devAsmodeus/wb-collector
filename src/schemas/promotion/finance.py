"""Схемы: Маркетинг — Финансы."""
from pydantic import BaseModel, Field


class BalanceCashback(BaseModel):
    """Промо-бонус."""
    id: int | None = Field(None, description="ID промо-бонуса")
    amount: int | None = Field(None, description="Сумма промо-бонуса, руб.")
    deadline: str | None = Field(None, description="Срок действия промо-бонуса (ISO 8601)")


class BalanceResponse(BaseModel):
    """Баланс рекламного кабинета."""
    balance: int | None = Field(None, description="Счёт, руб.")
    net: int | None = Field(None, description="Баланс, руб.")
    bonus: int | None = Field(None, description="Бонусы, руб.")
    cashbacks: list[BalanceCashback] | None = Field(None, description="Промо-бонусы")


class BudgetResponse(BaseModel):
    """Бюджет кампании."""
    cash: int | None = Field(None, description="Не используется. Всегда 0.")
    netting: int | None = Field(None, description="Не используется. Всегда 0.")
    total: int | None = Field(None, description="Бюджет кампании, руб.")


class DepositRequest(BaseModel):
    """Пополнение бюджета кампании."""
    sum: int = Field(description="Общая сумма пополнения бюджета, руб.")
    cashback_sum: int | None = Field(
        None, description="Сумма пополнения промо-бонусами, руб."
    )
    cashback_percent: int | None = Field(
        None, description="Процент от суммы пополнения, доступный для промо-бонусов."
    )
    type: int = Field(
        description="Источник пополнения: `0` — счёт, `1` — баланс, `3` — бонусы"
    )
    return_: bool | None = Field(
        None,
        alias="return",
        description="`true` — вернуть обновлённый размер бюджета в ответе",
    )

    model_config = {"populate_by_name": True}


class UPDItem(BaseModel):
    """Строка УПД (универсальный передаточный документ)."""
    date: str | None = Field(None, description="Дата документа")
    docNum: str | None = Field(None, description="Номер документа")
    amount: float | None = Field(None, description="Сумма, руб.")


class UPDResponse(BaseModel):
    """Список УПД за период."""
    upd: list[UPDItem] = Field(default=[], description="УПД за выбранный период")


class PaymentItem(BaseModel):
    """Платёж по рекламным кампаниям."""
    date: str | None = Field(None, description="Дата платежа (ISO 8601)")
    sum: float | None = Field(None, description="Сумма платежа, руб.")
    type: str | None = Field(None, description="Тип платежа")


class PaymentsResponse(BaseModel):
    """История платежей по рекламным кампаниям."""
    payments: list[PaymentItem] = Field(default=[], description="Платежи за выбранный период")
