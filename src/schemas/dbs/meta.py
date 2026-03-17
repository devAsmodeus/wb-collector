"""Схемы: DBS — Метаданные сборочных заданий."""
from pydantic import BaseModel, Field


class DBSMetaOrderItem(BaseModel):
    """Пара orderId + значение метаданных для массовых операций DBS."""
    orderId: int = Field(description="ID сборочного задания")


class DBSMetaInfoRequest(BaseModel):
    """Запрос метаданных сборочных заданий DBS (bulk)."""
    orders: list[int] = Field(description="Список ID сборочных заданий")


class DBSMetaDeleteRequest(BaseModel):
    """Удаление метаданных сборочных заданий DBS (bulk)."""
    orders: list[int] = Field(description="Список ID сборочных заданий")
    key: str = Field(
        description="Тип метаданных для удаления: `sgtin`, `uin`, `imei`, `gtin`, `customsDeclarationNumber`.",
    )


class DBSSgtinItem(BaseModel):
    """Коды маркировки для одного задания."""
    orderId: int = Field(description="ID сборочного задания")
    sgtins: list[str] = Field(description="Массив кодов маркировки КИЗ/честный знак (16–135 символов каждый)")


class DBSSetSgtinRequest(BaseModel):
    """Массовое закрепление кодов маркировки за заданиями DBS."""
    orders: list[DBSSgtinItem] = Field(description="Задания с кодами маркировки")


class DBSUinItem(BaseModel):
    """УИН для одного задания."""
    orderId: int = Field(description="ID сборочного задания")
    uin: str = Field(description="УИН ювелирного изделия")


class DBSSetUinRequest(BaseModel):
    """Массовое закрепление УИН за заданиями DBS."""
    orders: list[DBSUinItem] = Field(description="Задания с УИН")


class DBSImeiItem(BaseModel):
    """IMEI для одного задания."""
    orderId: int = Field(description="ID сборочного задания")
    imei: str = Field(description="IMEI мобильного устройства (15 цифр)")


class DBSSetImeiRequest(BaseModel):
    """Массовое закрепление IMEI за заданиями DBS."""
    orders: list[DBSImeiItem] = Field(description="Задания с IMEI")


class DBSGtinItem(BaseModel):
    """GTIN для одного задания."""
    orderId: int = Field(description="ID сборочного задания")
    gtin: str = Field(description="GTIN товара (8, 12, 13 или 14 цифр)")


class DBSSetGtinRequest(BaseModel):
    """Массовое закрепление GTIN за заданиями DBS."""
    orders: list[DBSGtinItem] = Field(description="Задания с GTIN")


class DBSCustomsItem(BaseModel):
    """Номер ГТД для одного задания."""
    orderId: int = Field(description="ID сборочного задания")
    customsDeclarationNumber: str = Field(description="Номер грузовой таможенной декларации (ГТД)")


class DBSSetCustomsRequest(BaseModel):
    """Массовое закрепление номеров ГТД за заданиями DBS."""
    orders: list[DBSCustomsItem] = Field(description="Задания с номерами ГТД")


# --- Deprecated (одиночные операции, заменены bulk-методами) ---

class DBSSetSgtinSingleRequest(BaseModel):
    """[DEPRECATED] Код маркировки для одного задания."""
    sgtins: list[str] = Field(description="Массив кодов маркировки (16–135 символов каждый)")


class DBSSetUinSingleRequest(BaseModel):
    """[DEPRECATED] УИН для одного задания."""
    uin: str = Field(description="УИН ювелирного изделия")


class DBSSetImeiSingleRequest(BaseModel):
    """[DEPRECATED] IMEI для одного задания."""
    imei: str = Field(description="IMEI мобильного устройства")


class DBSSetGtinSingleRequest(BaseModel):
    """[DEPRECATED] GTIN для одного задания."""
    gtin: str = Field(description="GTIN товара")
