"""Схемы: Общее — Информация о продавце."""
from pydantic import BaseModel


class SellerInfo(BaseModel):
    """Информация о продавце (GET /api/v1/seller-info).

    Поля точно соответствуют WB API:
      name, sid, tradeMark, tin
    """
    name: str
    sid: str
    tradeMark: str
    tin: str | None = None   # ИНН (в API поле называется tin, не itn)
