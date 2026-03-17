"""Схемы: DBW — Метаданные сборочных заданий."""
from pydantic import BaseModel, Field


class DBWOrderMetaResponse(BaseModel):
    """Метаданные сборочного задания DBW."""
    meta: dict | None = Field(None, description="Метаданные задания (коды маркировки, IMEI, GTIN и др.)")


class DBWSetSgtinRequest(BaseModel):
    """Коды маркировки (честный знак) для задания DBW.

    Отличие от FBS: DBW принимает массив кодов (`sgtins`), а не один код.
    """
    sgtins: list[str] = Field(
        description="Массив кодов маркировки КИЗ/честный знак. "
                    "Допускается от 16 до 135 символов для каждого кода.",
    )


class DBWSetUinRequest(BaseModel):
    """УИН ювелирного изделия для задания DBW."""
    uin: str = Field(description="УИН — уникальный идентификационный номер ювелирного изделия")


class DBWSetImeiRequest(BaseModel):
    """IMEI мобильного устройства для задания DBW."""
    imei: str = Field(description="IMEI — международный идентификатор мобильного оборудования (15 цифр)")


class DBWSetGtinRequest(BaseModel):
    """GTIN товара для задания DBW."""
    gtin: str = Field(description="GTIN — глобальный идентификатор торговой единицы (8, 12, 13 или 14 цифр)")
