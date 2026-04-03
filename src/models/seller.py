from datetime import datetime

from sqlalchemy import String, DateTime, Float, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class WbSellerRating(Base):
    """Рейтинг продавца. Хранится одна актуальная запись (id=1)."""
    __tablename__ = "wb_seller_rating"

    id: Mapped[int] = mapped_column(primary_key=True)
    feedback_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    valuation: Mapped[float | None] = mapped_column(Float, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Псевдонимы для совместимости с Pydantic схемой
    @property
    def feedbackCount(self) -> int | None:
        return self.feedback_count


class WbSellerSubscription(Base):
    """Подписка Джем продавца. Хранится одна актуальная запись (id=1)."""
    __tablename__ = "wb_seller_subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    state: Mapped[str | None] = mapped_column(String(20), nullable=True)         # active | inactive
    activation_source: Mapped[str | None] = mapped_column(String(20), nullable=True)  # constructor | jam
    level: Mapped[str | None] = mapped_column(String(20), nullable=True)         # standard | advanced | premium
    since: Mapped[str | None] = mapped_column(String(50), nullable=True)         # ISO 8601 datetime
    till: Mapped[str | None] = mapped_column(String(50), nullable=True)          # ISO 8601 datetime
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    @property
    def activationSource(self) -> str | None:
        return self.activation_source


class SellerOrm(Base):
    """Информация о продавце. Хранится при каждом запросе."""
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
