"""ORM модели: Заказы FBS / DBW / DBS / Самовывоз."""
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Float, Integer, Numeric, String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class FbsOrder(Base):
    """Сборочное задание FBS."""
    __tablename__ = "fbs_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True, comment="ID сборочного задания")
    order_uid: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True, comment="UUID заказа")
    rid: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Уникальный ID позиции заказа")
    date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="Дата создания заказа")
    last_change_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата последнего изменения статуса")
    warehouse_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Склад WB отгрузки")
    country_name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Страна доставки")
    oblast_okrug_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Федеральный округ")
    region_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Регион доставки")
    article: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Артикул продавца")
    nm_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="Артикул WB (nmID)")
    chrt_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="ID характеристики размера")
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Предмет")
    category: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Категория")
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Бренд")
    name: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="Наименование товара")
    tech_size: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Технический размер")
    color_code: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Код цвета")
    total_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Цена без скидок, руб.")
    discount_percent: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Скидка продавца, %")
    spp: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Скидка по программе WB (СПП), %")
    finished_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Итоговая цена, руб.")
    price_with_disc: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Цена со скидкой продавца, руб.")
    is_cancel: Mapped[bool] = mapped_column(Boolean, default=False, comment="Отменён")
    cancel_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата отмены")
    order_type: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Тип заказа")
    supplier_status: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Статус продавца")
    wb_status: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Статус WB")
    skus: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="Баркоды товара (JSON)")
    is_zero_order: Mapped[bool] = mapped_column(Boolean, default=False, comment="Нулевой заказ")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class DbwOrder(Base):
    """Сборочное задание DBW (Доставка WB)."""
    __tablename__ = "dbw_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True, comment="ID заказа")
    order_uid: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True, comment="UUID заказа")
    rid: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="ID позиции заказа")
    date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="Дата создания")
    last_change_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата изменения статуса")
    warehouse_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Склад WB")
    country_name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Страна")
    region_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Регион")
    article: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Артикул продавца")
    nm_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="Артикул WB (nmID)")
    chrt_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="ID размера")
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Предмет")
    category: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Категория")
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Бренд")
    name: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="Наименование")
    tech_size: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Размер")
    total_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Цена, руб.")
    discount_percent: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Скидка, %")
    finished_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Итоговая цена, руб.")
    is_cancel: Mapped[bool] = mapped_column(Boolean, default=False, comment="Отменён")
    cancel_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата отмены")
    order_type: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Тип заказа")
    supplier_status: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Статус продавца")
    wb_status: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Статус WB")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class DbsOrder(Base):
    """Сборочное задание DBS (Доставка продавцом)."""
    __tablename__ = "dbs_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True, comment="ID заказа")
    order_uid: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True, comment="UUID заказа")
    rid: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="ID позиции")
    date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="Дата создания")
    last_change_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата изменения")
    warehouse_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Склад WB")
    country_name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Страна")
    region_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Регион")
    article: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Артикул продавца")
    nm_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="Артикул WB (nmID)")
    chrt_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="ID размера")
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Предмет")
    category: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Категория")
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Бренд")
    name: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="Наименование")
    tech_size: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Размер")
    total_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Цена, руб.")
    discount_percent: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Скидка, %")
    finished_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Итоговая цена, руб.")
    is_cancel: Mapped[bool] = mapped_column(Boolean, default=False, comment="Отменён")
    cancel_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата отмены")
    order_type: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Тип заказа")
    supplier_status: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Статус продавца")
    wb_status: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Статус WB")
    delivery_address: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="Адрес доставки (JSON)")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class PickupOrder(Base):
    """Заказ самовывоза (Click & Collect)."""
    __tablename__ = "pickup_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True, comment="ID заказа")
    order_uid: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True, comment="UUID заказа")
    rid: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="ID позиции")
    date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="Дата создания")
    last_change_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата изменения")
    warehouse_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Склад WB")
    article: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Артикул продавца")
    nm_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="Артикул WB (nmID)")
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Предмет")
    category: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Категория")
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Бренд")
    name: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="Наименование")
    tech_size: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Размер")
    total_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Цена, руб.")
    discount_percent: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Скидка, %")
    finished_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Итоговая цена, руб.")
    is_cancel: Mapped[bool] = mapped_column(Boolean, default=False, comment="Отменён")
    cancel_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата отмены")
    supplier_status: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Статус продавца")
    wb_status: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Статус WB")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")
