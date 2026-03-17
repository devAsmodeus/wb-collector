"""Схемы: Самовывоз — Метаданные сборочных заданий."""
from pydantic import BaseModel, Field


class PickupMetaInfoRequest(BaseModel):
    """Запрос метаданных заданий Самовывоз (bulk)."""
    orders: list[int] = Field(description="Список ID сборочных заданий")


class PickupMetaDeleteRequest(BaseModel):
    """Удаление метаданных заданий Самовывоз (bulk)."""
    orders: list[int] = Field(description="Список ID сборочных заданий")
    key: str = Field(description="Тип метаданных: `sgtin`, `uin`, `imei`, `gtin`.")


class PickupSgtinItem(BaseModel):
    orderId: int = Field(description="ID сборочного задания")
    sgtins: list[str] = Field(description="Коды маркировки (16–135 символов каждый)")


class PickupSetSgtinRequest(BaseModel):
    orders: list[PickupSgtinItem] = Field(description="Задания с кодами маркировки")


class PickupUinItem(BaseModel):
    orderId: int = Field(description="ID сборочного задания")
    uin: str = Field(description="УИН ювелирного изделия")


class PickupSetUinRequest(BaseModel):
    orders: list[PickupUinItem] = Field(description="Задания с УИН")


class PickupImeiItem(BaseModel):
    orderId: int = Field(description="ID сборочного задания")
    imei: str = Field(description="IMEI мобильного устройства")


class PickupSetImeiRequest(BaseModel):
    orders: list[PickupImeiItem] = Field(description="Задания с IMEI")


class PickupGtinItem(BaseModel):
    orderId: int = Field(description="ID сборочного задания")
    gtin: str = Field(description="GTIN товара")


class PickupSetGtinRequest(BaseModel):
    orders: list[PickupGtinItem] = Field(description="Задания с GTIN")


# --- Deprecated (одиночные) ---

class PickupSetSgtinSingleRequest(BaseModel):
    sgtins: list[str] = Field(description="Массив кодов маркировки")


class PickupSetUinSingleRequest(BaseModel):
    uin: str = Field(description="УИН ювелирного изделия")


class PickupSetImeiSingleRequest(BaseModel):
    imei: str = Field(description="IMEI мобильного устройства")


class PickupSetGtinSingleRequest(BaseModel):
    gtin: str = Field(description="GTIN товара")
