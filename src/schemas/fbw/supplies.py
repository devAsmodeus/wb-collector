"""Схемы: FBW — Информация о поставках."""
from pydantic import BaseModel, Field


class FBWSuppliesFiltersRequest(BaseModel):
    """Фильтры для получения списка поставок FBW."""
    dates: list[str] | None = Field(
        None,
        description="Фильтр по датам поставки в формате `YYYY-MM-DD`. Максимум 2 даты (диапазон).",
    )
    statusIDs: list[int] | None = Field(
        None,
        description=(
            "Фильтр по статусам поставки:\n"
            "- `1` — Не запланировано\n"
            "- `2` — Запланировано\n"
            "- `3` — В пути\n"
            "- `4` — Принято\n"
            "- `5` — Отклонено"
        ),
    )


class FBWSupply(BaseModel):
    """Поставка FBW."""
    phone: str | None = Field(None, description="Телефон пользователя, создавшего поставку")
    supplyID: int | None = Field(
        None,
        description="ID поставки. Если `null` — это незапланированный заказ (используйте `preorderID`).",
    )
    preorderID: int | None = Field(
        None,
        description="ID заказа (незапланированная поставка). Для виртуальных поставок используется вместо `supplyID`.",
    )
    createDate: str | None = Field(None, description="Дата и время создания поставки (ISO 8601)")
    supplyDate: str | None = Field(None, description="Плановая дата отгрузки поставки (ISO 8601)")
    factDate: str | None = Field(None, description="Дата фактической отгрузки поставки (ISO 8601)")
    updatedDate: str | None = Field(None, description="Дата последнего изменения поставки (ISO 8601)")
    statusID: int | None = Field(
        None,
        description=(
            "ID статуса поставки:\n"
            "- `1` — Не запланировано\n"
            "- `2` — Запланировано\n"
            "- `3` — В пути\n"
            "- `4` — Принято\n"
            "- `5` — Отклонено"
        ),
    )
    boxTypeID: int | None = Field(
        None,
        description=(
            "ID типа поставки:\n"
            "- `0` — Без коробов (виртуальная поставка)\n"
            "- `1` — Монопаллета\n"
            "- `2` — Суперсейф\n"
            "- `3` — QR-поставка\n"
            "- `4` — Короба\n"
            "- `5` — Поштучная паллета"
        ),
    )
    isBoxOnPallet: bool | None = Field(
        None,
        description="Тип поставки **Поштучная паллета**: `true` — да, `false` — нет.",
    )


class FBWSuppliesResponse(BaseModel):
    """Список поставок FBW."""
    supplies: list[FBWSupply] = Field(default=[], description="Поставки FBW")


class FBWSupplyGood(BaseModel):
    """Товар в составе поставки FBW."""
    barcode: str | None = Field(None, description="Баркод товара")
    article: str | None = Field(None, description="Артикул продавца")
    name: str | None = Field(None, description="Наименование товара")
    quantity: int | None = Field(None, description="Количество единиц в поставке")
    brand: str | None = Field(None, description="Бренд товара")
    subject: str | None = Field(None, description="Предмет товара")


class FBWSupplyGoodsResponse(BaseModel):
    """Товары в составе поставки FBW."""
    goods: list[FBWSupplyGood] = Field(default=[], description="Список товаров в поставке")


class FBWPackageQRItem(BaseModel):
    """Один QR-код в упаковке поставки FBW."""
    file: str | None = Field(None, description="QR-код в формате base64")
    type: str | None = Field(None, description="Формат QR-кода: svg или zplLabel")


class FBWPackageQR(BaseModel):
    """QR-коды для упаковки поставки FBW. WB возвращает массив или пустой список."""
    items: list[FBWPackageQRItem] = Field(default=[], description="Список QR-кодов")

    @classmethod
    def model_validate(cls, obj, **kwargs):
        # WB returns [] or [{file, type}, ...]
        if isinstance(obj, list):
            return cls(items=[FBWPackageQRItem(**i) if isinstance(i, dict) else i for i in obj])
        if isinstance(obj, dict):
            if "file" in obj or "type" in obj:
                return cls(items=[FBWPackageQRItem(**obj)])
        return super().model_validate(obj, **kwargs)
