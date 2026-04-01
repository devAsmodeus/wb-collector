"""ORM модели: Аналитика (Analytics) — воронка продаж, поисковые запросы, остатки."""
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Integer, Numeric, String, Date, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class AnalyticsFunnelProduct(Base):
    """Воронка продаж по артикулам (seller-analytics-api)."""
    __tablename__ = "analytics_funnel_products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nm_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="Артикул WB (nmID)")
    vendor_code: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Артикул продавца")
    brand_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Бренд")
    subject_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Название предмета")
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True, comment="Дата периода")
    opens_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Переходы в карточку, шт.")
    add_to_cart_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Добавили в корзину, шт.")
    orders_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Заказали, шт.")
    orders_sum_rub: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Заказали на сумму, руб.")
    buyouts_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Выкупили, шт.")
    buyouts_sum_rub: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Выкупили на сумму, руб.")
    cancel_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Отменили и вернули, шт.")
    cancel_sum_rub: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Отменили на сумму, руб.")
    avg_price_rub: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Средняя цена, руб.")
    avg_orders_count_per_day: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="Среднее заказов в день")
    conversions: Mapped[dict | None] = mapped_column(JSONB, nullable=True, comment="Конверсии (JSON)")
    raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True, comment="Сырые данные от WB (JSON)")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")

    __table_args__ = (
        UniqueConstraint("nm_id", "date", name="uq_funnel_nm_id_date"),
    )


class AnalyticsSearchQuery(Base):
    """Поисковые запросы по товарам (seller-analytics-api)."""
    __tablename__ = "analytics_search_queries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nm_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="Артикул WB (nmID)")
    text: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="Текст поискового запроса")
    frequency: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Количество обращений с запросом")
    avg_position: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="Средняя позиция в поиске")
    median_position: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True, comment="Медианная позиция в поиске")
    opens_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Переходы в карточку, шт.")
    add_to_cart_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Добавили в корзину, шт.")
    orders_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Заказали, шт.")
    orders_sum_rub: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Заказали на сумму, руб.")
    period_start: Mapped[date] = mapped_column(Date, nullable=False, comment="Начало периода")
    period_end: Mapped[date] = mapped_column(Date, nullable=False, comment="Конец периода")
    raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True, comment="Сырые данные от WB (JSON)")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")

    __table_args__ = (
        UniqueConstraint("nm_id", "text", "period_start", name="uq_search_nm_text_period"),
    )


class AnalyticsStocksGroup(Base):
    """Аналитика остатков по группам (seller-analytics-api)."""
    __tablename__ = "analytics_stocks_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nm_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="Артикул WB (nmID)")
    vendor_code: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Артикул продавца")
    brand_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Бренд")
    subject_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Название предмета")
    orders_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Заказы, шт.")
    orders_sum: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Заказы, сумма")
    avg_orders: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Среднее заказов в день")
    buyout_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Выкупы, шт.")
    buyout_sum: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Выкупы, сумма")
    buyout_percent: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Процент выкупа")
    stock_count: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Остатки, шт.")
    stock_sum: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Стоимость остатков")
    days_on_site: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Дней на сайте")
    period_start: Mapped[date] = mapped_column(Date, nullable=False, comment="Начало периода")
    period_end: Mapped[date] = mapped_column(Date, nullable=False, comment="Конец периода")
    raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True, comment="Сырые данные от WB (JSON)")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")

    __table_args__ = (
        UniqueConstraint("nm_id", "period_start", name="uq_stocks_nm_id_period"),
    )
