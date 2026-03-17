"""Схемы: Отчёты — Доля бренда, продажи по регионам, скрытые товары, возвраты."""
from pydantic import BaseModel, Field


class RegionSaleItem(BaseModel):
    """Продажи по регионам."""
    regionName: str | None = Field(None, description="Название региона")
    quantity: int | None = Field(None, description="Количество продаж")
    sum: float | None = Field(None, description="Сумма продаж, руб.")


class BrandItem(BaseModel):
    """Бренд продавца."""
    brandName: str | None = Field(None, description="Название бренда")
    brandId: int | None = Field(None, description="ID бренда")


class BrandParentSubjectItem(BaseModel):
    """Родительская категория для доли бренда."""
    parentId: int | None = Field(None, description="ID родительской категории")
    parentName: str | None = Field(None, description="Название родительской категории")


class BrandShareItem(BaseModel):
    """Доля бренда в продажах по категории."""
    subjectId: int | None = Field(None, description="ID предмета")
    subjectName: str | None = Field(None, description="Название предмета")
    brandShare: float | None = Field(None, description="Доля бренда в продажах, %")
    brandCount: int | None = Field(None, description="Количество товаров бренда")
    totalCount: int | None = Field(None, description="Общее количество товаров в категории")


class BannedProductItem(BaseModel):
    """Скрытый товар."""
    nmId: int | None = Field(None, description="Артикул WB (nmID)")
    vendorCode: str | None = Field(None, description="Артикул продавца")
    subjectName: str | None = Field(None, description="Предмет")
    reason: str | None = Field(None, description="Причина скрытия")


class GoodsReturnItem(BaseModel):
    """Отчёт о возврате товаров."""
    date: str | None = Field(None, description="Дата возврата (ISO 8601)")
    nmId: int | None = Field(None, description="Артикул WB (nmID)")
    vendorCode: str | None = Field(None, description="Артикул продавца")
    quantity: int | None = Field(None, description="Количество возвращённых единиц")
    warehouseName: str | None = Field(None, description="Склад возврата")
