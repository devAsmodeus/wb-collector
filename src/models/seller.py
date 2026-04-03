from datetime import datetime

from sqlalchemy import String, DateTime, Float, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class WbSellerRating(Base):
    """Рейтинг продавца. Хранится одна актуальная запись (id=1)."""
    __tablename__ = "wb_seller_rating"

    id: Mapped[int] = mapped_column(primary_key=True)
    current: Mapped[float | None] = mapped_column(Float, nullable=True)
    wb_rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    delivery_speed: Mapped[float | None] = mapped_column(Float, nullable=True)
    quality_goods: Mapped[float | None] = mapped_column(Float, nullable=True)
    service_review: Mapped[float | None] = mapped_column(Float, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    @property
    def wbRating(self) -> float | None:
        return self.wb_rating

    @property
    def deliverySpeed(self) -> float | None:
        return self.delivery_speed

    @property
    def qualityGoods(self) -> float | None:
        return self.quality_goods

    @property
    def serviceReview(self) -> float | None:
        return self.service_review


class WbSellerSubscription(Base):
    """Подписка Джем продавца. Хранится одна актуальная запись (id=1)."""
    __tablename__ = "wb_seller_subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    since: Mapped[str | None] = mapped_column(String(50), nullable=True)
    till: Mapped[str | None] = mapped_column(String(50), nullable=True)
    tariff: Mapped[str | None] = mapped_column(String(200), nullable=True)
    is_active: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    @property
    def isActive(self) -> bool | None:
        return self.is_active


class SellerOrm(Base):
    """Информация о продавце. Обновляется при каждом сборе."""
    __tablename__ = "sellers"

    id: Mapped[int] = mapped_column(primary_key=True)
    sid: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(500))
    trade_mark: Mapped[str] = mapped_column(String(500))

    @property
    def tradeMark(self) -> str:
        return self.trade_mark
    itn: Mapped[str | None] = mapped_column(String(20), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
