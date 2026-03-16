"""Схемы: Общее — Информация о продавце."""
from pydantic import BaseModel, Field, ConfigDict, AliasChoices


class SellerInfo(BaseModel):
    """Информация о продавце (GET /api/v1/seller-info)."""
    model_config = ConfigDict(populate_by_name=True)

    name: str
    sid: str
    # WB API возвращает tradeMark, ORM хранит trade_mark
    tradeMark: str = Field(validation_alias=AliasChoices("tradeMark", "trade_mark"))
    itn: str | None = None
