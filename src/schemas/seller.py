from pydantic import BaseModel


class SellerInfo(BaseModel):
    """Информация о продавце (GET /api/v1/seller-info)."""
    name: str           # Наименование продавца
    sid: str            # Уникальный ID продавца на WB
    tradeMark: str      # Торговое наименование
    itn: str | None = None  # ИНН (есть в реальном ответе)
