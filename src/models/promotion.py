"""ORM модели: Маркетинг (Promotion)."""
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Float, Integer, Numeric, String, DateTime, JSON, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class WbCampaign(Base):
    """Рекламная кампания WB."""
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    advert_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True, comment="ID кампании")
    name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Название кампании")
    status: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True, comment="-1=удалена,4=готова,7=завершена,8=отказ,9=показы,11=пауза")
    type: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="4=каталог,5=карточка,6=поиск,7=рекомендации,9=авто")
    payment_type: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="cpm или cpc")
    create_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата создания")
    change_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата изменения")
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата запуска")
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата завершения")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbCampaignStat(Base):
    """Статистика рекламной кампании."""
    __tablename__ = "campaign_stats"
    __table_args__ = (
        UniqueConstraint("advert_id", "date", name="uq_campaign_stats_advert_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    advert_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="ID кампании")
    date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="Дата")
    views: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="Показы")
    clicks: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Клики")
    ctr: Mapped[float | None] = mapped_column(Numeric(8, 4), nullable=True, comment="CTR, %")
    cpc: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="CPC, руб.")
    sum_: Mapped[float | None] = mapped_column(Numeric(12, 2), name="sum", nullable=True, comment="Расходы, руб.")
    atbs: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Добавления в корзину")
    orders: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Заказы")
    cr: Mapped[float | None] = mapped_column(Numeric(8, 4), nullable=True, comment="CR (конверсия в заказ), %")
    shks: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Заказано товаров, шт.")
    sum_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Заказано на сумму, руб.")
    raw_data: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="Полные данные (JSON)")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbPromotion(Base):
    """Акция WB (календарь акций)."""
    __tablename__ = "promotions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    promotion_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True, comment="ID акции")
    name: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="Название акции")
    start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата начала")
    end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата окончания")
    type: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Тип акции")
    in_action: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="Участвует ли продавец")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")
