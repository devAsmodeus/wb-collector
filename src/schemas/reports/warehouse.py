"""Схемы: Отчёты — Склады и платное хранение."""
from pydantic import BaseModel, Field


class TaskStatusResponse(BaseModel):
    """Статус задачи отчёта."""
    taskId: str | None = Field(None, description="ID задачи")
    status: str | None = Field(None, description="Статус: `pending`, `processing`, `done`, `error`")
    createdAt: str | None = Field(None, description="Дата создания задачи (ISO 8601)")
    updatedAt: str | None = Field(None, description="Дата последнего обновления (ISO 8601)")


class WarehouseRemainsItem(BaseModel):
    """Строка отчёта об остатках на складах."""
    brand: str | None = Field(None, description="Бренд")
    subjectName: str | None = Field(None, description="Предмет")
    vendorCode: str | None = Field(None, description="Артикул продавца")
    nmId: int | None = Field(None, description="Артикул WB (nmID)")
    barcode: str | None = Field(None, description="Баркод")
    techSize: str | None = Field(None, description="Размер")
    volume: float | None = Field(None, description="Объём, л")
    inWayToClient: int | None = Field(None, description="В пути к покупателю")
    inWayFromClient: int | None = Field(None, description="В пути от покупателя")
    quantityWarehousesFull: int | None = Field(None, description="Итого остаток на всех складах WB")


class PaidStorageItem(BaseModel):
    """Строка отчёта о платном хранении."""
    date: str | None = Field(None, description="Дата (ISO 8601)")
    logWarehouseCoef: float | None = Field(None, description="Логистический коэффициент склада")
    officeId: int | None = Field(None, description="ID склада")
    warehouse: str | None = Field(None, description="Название склада")
    nmId: int | None = Field(None, description="Артикул WB (nmID)")
    vendorCode: str | None = Field(None, description="Артикул продавца")
    volume: float | None = Field(None, description="Объём товара, л")
    calcType: str | None = Field(None, description="Тип расчёта")
    warehousePrice: float | None = Field(None, description="Тариф хранения склада, руб.")
    barcodesCount: int | None = Field(None, description="Количество баркодов")
    palletPlaceCode: int | None = Field(None, description="Код паллетоместа")
    palletCount: float | None = Field(None, description="Количество паллет")
    originalDate: str | None = Field(None, description="Исходная дата расчёта (ISO 8601)")
    loyaltyDiscount: float | None = Field(None, description="Скидка по программе лояльности, %")
    tariffFixDate: str | None = Field(None, description="Дата фиксации тарифа (ISO 8601)")
    tariffLowerDate: str | None = Field(None, description="Дата применения пониженного тарифа (ISO 8601)")
