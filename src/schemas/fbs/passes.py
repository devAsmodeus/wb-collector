"""Схемы: FBS — Пропуска на склад WB."""
from pydantic import BaseModel, Field


class PassOffice(BaseModel):
    """Склад WB, для которого требуется пропуск."""
    id: int = Field(description="ID склада WB")
    name: str = Field(description="Название склада (напр. 'Коледино', 'Электросталь')")
    address: str | None = Field(None, description="Адрес склада")


class PassOfficesResponse(BaseModel):
    """Склады, требующие оформление пропуска."""
    offices: list[PassOffice] = Field(default=[], description="Список складов, требующих пропуск")


class Pass(BaseModel):
    """Пропуск на склад WB."""
    id: int | None = Field(None, description="Внутренний ID пропуска")
    passId: int | None = Field(None, description="Номер пропуска (отображается на КПП)")
    warehouseId: int | None = Field(None, description="ID склада WB")
    warehouseName: str | None = Field(None, description="Название склада WB")
    status: str | None = Field(
        None,
        description="Статус пропуска: `active` — действующий, `expired` — истёк, `cancelled` — отменён",
    )
    validFrom: str | None = Field(None, description="Дата начала действия пропуска (ISO 8601)")
    validTo: str | None = Field(None, description="Дата окончания действия пропуска (ISO 8601)")
    createdAt: str | None = Field(None, description="Дата создания пропуска (ISO 8601)")


class PassesResponse(BaseModel):
    """Список пропусков продавца."""
    passes: list[Pass] = Field(default=[], description="Пропуска на склады WB")


class CreatePassRequest(BaseModel):
    """Тело запроса для создания пропуска на склад."""
    warehouseId: int = Field(description="ID склада WB, для которого оформляется пропуск")
    dateFrom: str = Field(description="Дата начала действия пропуска (ISO 8601, напр. `2024-03-01`)")
    dateTo: str = Field(description="Дата окончания действия пропуска (ISO 8601)")
    carNumber: str = Field(description="Государственный регистрационный номер автомобиля (напр. `А001АА77`)")
    fullName: str = Field(description="ФИО водителя полностью")


class UpdatePassRequest(BaseModel):
    """Тело запроса для обновления пропуска. Передавать только изменяемые поля."""
    warehouseId: int | None = Field(None, description="Новый ID склада WB")
    dateFrom: str | None = Field(None, description="Новая дата начала (ISO 8601)")
    dateTo: str | None = Field(None, description="Новая дата окончания (ISO 8601)")
    carNumber: str | None = Field(None, description="Новый номер автомобиля")
    fullName: str | None = Field(None, description="Новое ФИО водителя")
