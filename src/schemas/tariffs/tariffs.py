"""Схемы: Тарифы WB."""
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


def _parse_wb_decimal(v) -> Decimal | None:
    """WB возвращает числа как строки: '0,07', '48', '-', ''."""
    if v is None or v == "-" or v == "":
        return None
    return Decimal(str(v).replace(",", "."))


class CommissionCategory(BaseModel):
    """Комиссия по категории товаров."""
    parentName: str | None = Field(None, description="Родительская категория")
    subjectName: str | None = Field(None, description="Название категории (предмет)")
    subjectId: int | None = Field(None, description="ID категории")
    kgvpMarketplace: float | None = Field(None, description="Комиссия за продажу (маркетплейс)")
    kgvpSupplier: float | None = Field(None, description="Комиссия за продажу (поставщик)")
    kgvpSupplierExpress: float | None = Field(None, description="Комиссия за продажу (экспресс)")
    paidStorageKgvp: float | None = Field(None, description="Комиссия за платное хранение")
    returnCost: float | None = Field(None, description="Стоимость возврата покупателя")
    createDto: str | None = Field(None, description="Дата обновления комиссии (ISO 8601)")


class CommissionsResponse(BaseModel):
    """Список комиссий по категориям."""
    report: list[CommissionCategory] | None = Field(None, description="Комиссии по категориям")


class ReturnCostItem(BaseModel):
    """Стоимость возврата продавцу."""
    warehouseId: int | None = Field(None, description="ID склада WB")
    warehouseName: str | None = Field(None, description="Название склада WB")
    backDeliveryBase: Decimal | None = Field(None, description="Базовая стоимость возврата, руб.")
    backDeliveryLiter: Decimal | None = Field(None, description="Стоимость возврата за литр, руб.")
    backDeliveryAdditionalLiter: Decimal | None = Field(None, description="Дополнительная стоимость за каждый следующий литр, руб.")

    @field_validator("backDeliveryBase", "backDeliveryLiter", "backDeliveryAdditionalLiter", mode="before")
    @classmethod
    def parse_decimal(cls, v):
        return _parse_wb_decimal(v)


class ReturnCostResponse(BaseModel):
    """Стоимость возврата продавцу со складов WB."""
    dtNextBox: str | None = Field(None, description="Дата следующего пересчёта тарифов (ISO 8601)")
    dtTillMax: str | None = Field(None, description="Дата окончания действия максимального тарифа (ISO 8601)")
    warehouseList: list[ReturnCostItem] | None = Field(None, description="Тарифы возврата по складам")


class BoxTariffItem(BaseModel):
    """Тариф на поставку коробами. WB возвращает числа как строки!"""
    warehouseId: int | None = Field(None, description="ID склада WB")
    warehouseName: str | None = Field(None, description="Название склада")
    boxDeliveryAndStorageExpr: str | None = Field(None, description="Выражение для расчёта тарифа")
    boxDeliveryBase: Decimal | None = Field(None, description="Логистика, первый литр, руб.")
    boxDeliveryLiter: Decimal | None = Field(None, description="Логистика, дополнительный литр, руб.")
    boxDeliveryCoefExpr: str | None = Field(None, description="Коэффициент логистики, %")
    boxDeliveryMarketplaceBase: Decimal | None = Field(None, description="Логистика FBS, первый литр, руб.")
    boxDeliveryMarketplaceLiter: Decimal | None = Field(None, description="Логистика FBS, дополнительный литр, руб.")
    boxDeliveryMarketplaceCoefExpr: str | None = Field(None, description="Коэффициент FBS, %")
    boxStorageBase: Decimal | None = Field(None, description="Хранение в день, первый литр, руб.")
    boxStorageLiter: Decimal | None = Field(None, description="Хранение в день, дополнительный литр, руб.")
    boxStorageCoefExpr: str | None = Field(None, description="Коэффициент хранения, %")

    _decimal_fields = [
        "boxDeliveryBase", "boxDeliveryLiter",
        "boxDeliveryMarketplaceBase", "boxDeliveryMarketplaceLiter",
        "boxStorageBase", "boxStorageLiter",
    ]

    @field_validator(*_decimal_fields, mode="before")
    @classmethod
    def parse_decimal(cls, v):
        return _parse_wb_decimal(v)


class BoxTariffsResponse(BaseModel):
    """Тарифы на поставку коробами."""
    dtNextBox: str | None = Field(None, description="Дата следующего пересчёта тарифов (ISO 8601)")
    dtTillMax: str | None = Field(None, description="Дата окончания действия тарифа (ISO 8601)")
    warehouseList: list[BoxTariffItem] | None = Field(None, description="Тарифы по складам")


class PalletTariffItem(BaseModel):
    """Тариф на поставку паллетами. WB возвращает числа как строки!"""
    warehouseId: int | None = Field(None, description="ID склада WB")
    warehouseName: str | None = Field(None, description="Название склада")
    isSuperSafe: bool | None = Field(None, description="Склад с повышенной безопасностью хранения")
    palletDeliveryExpr: str | None = Field(None, description="Выражение для расчёта тарифа паллетной поставки")
    palletDeliveryValueBase: Decimal | None = Field(None, description="Базовый тариф доставки паллеты, руб.")
    palletDeliveryValueLiter: Decimal | None = Field(None, description="Тариф доставки паллеты за литр, руб.")
    palletStorageExpr: str | None = Field(None, description="Выражение расчёта хранения паллеты")
    palletStorageValueExpr: Decimal | None = Field(None, description="Тариф хранения паллеты, руб./день")

    @field_validator("palletDeliveryValueBase", "palletDeliveryValueLiter", "palletStorageValueExpr", mode="before")
    @classmethod
    def parse_decimal(cls, v):
        return _parse_wb_decimal(v)


class PalletTariffsResponse(BaseModel):
    """Тарифы на поставку паллетами."""
    dtNextBox: str | None = Field(None, description="Дата следующего пересчёта тарифов (ISO 8601)")
    dtTillMax: str | None = Field(None, description="Дата окончания действия тарифа (ISO 8601)")
    warehouseList: list[PalletTariffItem] | None = Field(None, description="Тарифы по складам")


class SupplyTariffItem(BaseModel):
    """Коэффициент приёмки на складе WB (acceptance coefficient).

    YAML: /api/tariffs/v1/acceptance/coefficients
    Response: массив объектов AcceptanceCoefficient.
    """
    date: str | None = Field(None, description="Дата начала действия коэффициента")
    coefficient: int | None = Field(None, description="Коэффициент приёмки: -1=недоступна, 0=бесплатно, >=1=множитель")
    warehouseID: int | None = Field(None, description="ID склада WB")
    warehouseName: str | None = Field(None, description="Название склада")
    allowUnload: bool | None = Field(None, description="Доступность приёмки для данного типа поставки")
    boxTypeID: int | None = Field(None, description="ID типа поставки: 2=Короба, 5=Паллеты, 6=Суперсейф")
    storageCoef: Decimal | None = Field(None, description="Коэффициент хранения")
    deliveryCoef: Decimal | None = Field(None, description="Коэффициент доставки")
    deliveryBaseLiter: Decimal | None = Field(None, description="Доставка, первый литр")
    deliveryAdditionalLiter: Decimal | None = Field(None, description="Доставка, дополнительный литр")
    storageBaseLiter: Decimal | None = Field(None, description="Хранение, первый литр")
    storageAdditionalLiter: Decimal | None = Field(None, description="Хранение, дополнительный литр")
    isSortingCenter: bool | None = Field(None, description="Является сортировочным центром")

    @field_validator(
        "storageCoef", "deliveryCoef",
        "deliveryBaseLiter", "deliveryAdditionalLiter",
        "storageBaseLiter", "storageAdditionalLiter",
        mode="before",
    )
    @classmethod
    def parse_decimal(cls, v):
        return _parse_wb_decimal(v)
