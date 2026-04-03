from datetime import datetime

from sqlalchemy import String, DateTime, Float, Integer, Boolean, JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class WbSellerRating(Base):
    """Рейтинг продавца. Хранится одна актуальная запись (id=1)."""
    __tablename__ = "seller_rating"

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
    __tablename__ = "seller_subscriptions"

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


class WbUser(Base):
    """Пользователь (сотрудник) продавца. GET /api/v1/users."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)  # WB user id
    role: Mapped[str | None] = mapped_column(String(100), nullable=True)
    position: Mapped[str | None] = mapped_column(String(200), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    is_owner: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    second_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    patronymic: Mapped[str | None] = mapped_column(String(200), nullable=True)
    goods_return: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    is_invitee: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    invitee_info: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    access: Mapped[list | None] = mapped_column(JSON, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Псевдонимы для Pydantic (camelCase)
    @property
    def isOwner(self) -> bool | None:
        return self.is_owner

    @property
    def firstName(self) -> str | None:
        return self.first_name

    @property
    def secondName(self) -> str | None:
        return self.second_name

    @property
    def goodsReturn(self) -> bool | None:
        return self.goods_return

    @property
    def isInvitee(self) -> bool | None:
        return self.is_invitee

    @property
    def inviteeInfo(self) -> dict | None:
        return self.invitee_info


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

    tin: Mapped[str | None] = mapped_column(String(20), nullable=True)   # ИНН — поле tin в WB API
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
