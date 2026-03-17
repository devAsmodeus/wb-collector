"""Схемы: Отчёты — Основные отчёты."""
from pydantic import BaseModel, Field


class StockItem(BaseModel):
    """Остаток товара на складе."""
    lastChangeDate: str | None = Field(None, description="Дата последнего изменения остатка")
    supplierArticle: str | None = Field(None, description="Артикул поставщика")
    techSize: str | None = Field(None, description="Размер товара")
    barcode: str | None = Field(None, description="Баркод")
    quantity: int | None = Field(None, description="Количество на складе WB")
    isSupply: bool | None = Field(None, description="Признак поставки (для FBO)")
    isRealization: bool | None = Field(None, description="Признак реализации")
    quantityFull: int | None = Field(None, description="Полное количество (с учётом брака)")
    inWayToClient: int | None = Field(None, description="В пути к покупателю")
    inWayFromClient: int | None = Field(None, description="В пути от покупателя")
    nmId: int | None = Field(None, description="Артикул WB (nmID)")
    subject: str | None = Field(None, description="Предмет")
    category: str | None = Field(None, description="Категория")
    brand: str | None = Field(None, description="Бренд")
    SCCode: str | None = Field(None, description="Код WB склада")
    Price: float | None = Field(None, description="Цена товара")
    Discount: float | None = Field(None, description="Скидка, %")
    warehouseName: str | None = Field(None, description="Название склада")


class OrderReportItem(BaseModel):
    """Заказ из отчёта."""
    date: str | None = Field(None, description="Дата заказа")
    lastChangeDate: str | None = Field(None, description="Дата последнего изменения")
    supplierArticle: str | None = Field(None, description="Артикул поставщика")
    techSize: str | None = Field(None, description="Размер")
    barcode: str | None = Field(None, description="Баркод")
    totalPrice: float | None = Field(None, description="Цена до скидки, руб.")
    discountPercent: float | None = Field(None, description="Скидка продавца, %")
    warehouseName: str | None = Field(None, description="Склад WB")
    oblast: str | None = Field(None, description="Регион доставки")
    incomeID: int | None = Field(None, description="ID поставки")
    odid: int | None = Field(None, description="ID уникальной позиции заказа")
    nmId: int | None = Field(None, description="Артикул WB (nmID)")
    subject: str | None = Field(None, description="Предмет")
    category: str | None = Field(None, description="Категория")
    brand: str | None = Field(None, description="Бренд")
    isCancel: bool | None = Field(None, description="Статус отмены: `true` — отменён")
    cancelDate: str | None = Field(None, description="Дата отмены заказа (ISO 8601)")


class SaleReportItem(BaseModel):
    """Продажа / возврат из отчёта."""
    date: str | None = Field(None, description="Дата продажи/возврата")
    lastChangeDate: str | None = Field(None, description="Дата последнего изменения")
    supplierArticle: str | None = Field(None, description="Артикул поставщика")
    techSize: str | None = Field(None, description="Размер")
    barcode: str | None = Field(None, description="Баркод")
    totalPrice: float | None = Field(None, description="Цена до скидки, руб.")
    discountPercent: float | None = Field(None, description="Скидка продавца, %")
    isSupply: bool | None = Field(None, description="Тип операции: поставка")
    isRealization: bool | None = Field(None, description="Тип операции: реализация")
    warehouseName: str | None = Field(None, description="Склад WB")
    oblast: str | None = Field(None, description="Регион")
    incomeID: int | None = Field(None, description="ID поставки")
    odid: int | None = Field(None, description="ID уникальной позиции заказа")
    srid: str | None = Field(None, description="Уникальный ID продажи/возврата")
    nmId: int | None = Field(None, description="Артикул WB (nmID)")
    subject: str | None = Field(None, description="Предмет")
    category: str | None = Field(None, description="Категория")
    brand: str | None = Field(None, description="Бренд")
    saleID: str | None = Field(None, description="Идентификатор продажи: `S` — продажа, `R` — возврат")


class ExciseReportRequest(BaseModel):
    """Запрос отчёта по маркированным товарам."""
    dateFrom: str = Field(description="Дата начала периода в формате `YYYY-MM-DD`")
    dateTo: str = Field(description="Дата окончания периода в формате `YYYY-MM-DD`")
