"""Схемы: Тарифы WB."""
from pydantic import BaseModel, Field


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
    backDeliveryBase: float | None = Field(None, description="Базовая стоимость возврата, руб.")
    backDeliveryLiter: float | None = Field(None, description="Стоимость возврата за литр, руб.")
    backDeliveryAdditionalLiter: float | None = Field(None, description="Дополнительная стоимость за каждый следующий литр, руб.")


class ReturnCostResponse(BaseModel):
    """Стоимость возврата продавцу со складов WB."""
    dtNextBox: str | None = Field(None, description="Дата следующего пересчёта тарифов (ISO 8601)")
    dtTillMax: str | None = Field(None, description="Дата окончания действия максимального тарифа (ISO 8601)")
    warehouseList: list[ReturnCostItem] | None = Field(None, description="Тарифы возврата по складам")


class BoxTariffItem(BaseModel):
    """Тариф на поставку коробами."""
    warehouseId: int | None = Field(None, description="ID склада WB")
    warehouseName: str | None = Field(None, description="Название склада")
    boxDeliveryAndStorageExpr: str | None = Field(None, description="Выражение для расчёта тарифа")
    boxDeliveryBase: float | None = Field(None, description="Базовый тариф доставки, руб.")
    boxDeliveryLiter: float | None = Field(None, description="Тариф доставки за литр, руб.")
    boxDeliveryAdditionalLiter: float | None = Field(None, description="Тариф доставки за каждый дополнительный литр, руб.")
    boxStorageBase: float | None = Field(None, description="Базовый тариф хранения, руб./день")
    boxStorageLiter: float | None = Field(None, description="Тариф хранения за литр, руб./день")
    boxStorageAdditionalLiter: float | None = Field(None, description="Тариф хранения за каждый доп. литр, руб./день")


class BoxTariffsResponse(BaseModel):
    """Тарифы на поставку коробами."""
    dtNextBox: str | None = Field(None, description="Дата следующего пересчёта тарифов (ISO 8601)")
    dtTillMax: str | None = Field(None, description="Дата окончания действия тарифа (ISO 8601)")
    warehouseList: list[BoxTariffItem] | None = Field(None, description="Тарифы по складам")


class PalletTariffItem(BaseModel):
    """Тариф на поставку паллетами."""
    warehouseId: int | None = Field(None, description="ID склада WB")
    warehouseName: str | None = Field(None, description="Название склада")
    isSuperSafe: bool | None = Field(None, description="Склад с повышенной безопасностью хранения")
    palletDeliveryExpr: str | None = Field(None, description="Выражение для расчёта тарифа паллетной поставки")
    palletDeliveryValueBase: float | None = Field(None, description="Базовый тариф доставки паллеты, руб.")
    palletDeliveryValueLiter: float | None = Field(None, description="Тариф доставки паллеты за литр, руб.")
    palletStorageExpr: str | None = Field(None, description="Выражение расчёта хранения паллеты")
    palletStorageValueExpr: float | None = Field(None, description="Тариф хранения паллеты, руб./день")


class PalletTariffsResponse(BaseModel):
    """Тарифы на поставку паллетами."""
    dtNextBox: str | None = Field(None, description="Дата следующего пересчёта тарифов (ISO 8601)")
    dtTillMax: str | None = Field(None, description="Дата окончания действия тарифа (ISO 8601)")
    warehouseList: list[PalletTariffItem] | None = Field(None, description="Тарифы по складам")


class SupplyTariffItem(BaseModel):
    """Тариф на поставку."""
    warehouseId: int | None = Field(None, description="ID склада WB")
    warehouseName: str | None = Field(None, description="Название склада")
    coefficient: int | None = Field(None, description="Коэффициент склада (0 — бесплатно, -1 — склад закрыт)")


class SupplyTariffsResponse(BaseModel):
    """Тарифы на поставку (коэффициенты складов)."""
    dtNextBox: str | None = Field(None, description="Дата следующего пересчёта тарифов (ISO 8601)")
    dtTillMax: str | None = Field(None, description="Дата окончания действия тарифа (ISO 8601)")
    warehouseList: list[SupplyTariffItem] | None = Field(None, description="Коэффициенты складов")
