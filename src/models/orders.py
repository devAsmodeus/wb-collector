"""ORM модели: Заказы FBS / DBW / DBS / Самовывоз.

Все таблицы строго по схемам WB API v3 (marketplace-api.wildberries.ru).
НЕ смешивать с полями из Statistics/Reports API.
"""
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class FbsOrder(Base):
    """Сборочное задание FBS. GET /api/v3/orders → Order schema."""
    __tablename__ = "fbs_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True, comment="id — ID сборочного задания")
    order_uid: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True, comment="orderUid — UUID заказа")
    rid: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="rid — уникальный ID позиции")
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="createdAt — дата создания")
    article: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="article — артикул продавца")
    color_code: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="colorCode — код цвета")
    nm_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="nmId — артикул WB")
    chrt_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="chrtId — ID размера")
    price: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="price — цена в копейках × 100")
    converted_price: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="convertedPrice — цена в валюте продавца")
    currency_code: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="currencyCode — код валюты ISO 4217")
    converted_currency_code: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="convertedCurrencyCode")
    delivery_type: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="deliveryType — тип доставки (fbs/dbs/...)")
    supply_id: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="supplyId — ID поставки")
    warehouse_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="warehouseId — ID склада продавца")
    office_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="officeId — ID офиса WB")
    cargo_type: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="cargoType — тип груза")
    cross_border_type: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="crossBorderType — кроссбордер тип")
    scan_price: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="scanPrice — цена при сканировании")
    is_zero_order: Mapped[bool] = mapped_column(Boolean, default=False, comment="isZeroOrder — нулевой заказ")
    comment: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="comment — комментарий")
    skus: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="skus — баркоды")
    offices: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="offices — офисы доставки")
    address: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="address — адрес доставки")
    options: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="options — доп. опции")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class DbwOrder(Base):
    """Сборочное задание DBW (Доставка WB). GET /api/v3/orders?deliveryType=dbw — Order schema из YAML."""
    __tablename__ = "dbw_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True, comment="id — ID заказа")
    order_uid: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True, comment="orderUid — UUID заказа")
    group_id: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="groupId — ID группы заказов")
    rid: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="rid — ID позиции")
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="createdAt — дата создания")
    article: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="article — артикул продавца")
    color_code: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="colorCode — код цвета")
    nm_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="nmId — артикул WB")
    chrt_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="chrtId — ID размера")
    price: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="price — цена")
    converted_price: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="convertedPrice")
    currency_code: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="currencyCode — ISO 4217")
    converted_currency_code: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="convertedCurrencyCode")
    delivery_type: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="deliveryType")
    supply_id: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="supplyId")
    warehouse_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="warehouseId")
    office_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="officeId")
    cargo_type: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="cargoType")
    comment: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="comment — комментарий")
    is_zero_order: Mapped[bool] = mapped_column(Boolean, default=False, comment="isZeroOrder")
    skus: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="skus")
    offices: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="offices")
    address: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="address")
    options: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="options")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class DbsOrder(Base):
    """Сборочное задание DBS (Доставка продавцом). GET /api/v3/orders?deliveryType=dbs"""
    __tablename__ = "dbs_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True, comment="id — ID заказа")
    order_uid: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True, comment="orderUid — UUID заказа")
    group_id: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="groupId")
    rid: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="rid — ID позиции")
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="createdAt — дата создания")
    article: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="article — артикул продавца")
    color_code: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="colorCode — код цвета")
    nm_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="nmId — артикул WB")
    chrt_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="chrtId — ID размера")
    price: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="price — цена")
    converted_price: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="convertedPrice")
    currency_code: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="currencyCode")
    converted_currency_code: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="convertedCurrencyCode")
    delivery_type: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="deliveryType")
    supply_id: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="supplyId")
    warehouse_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="warehouseId")
    office_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="officeId")
    cargo_type: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="cargoType")
    comment: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="comment")
    is_zero_order: Mapped[bool] = mapped_column(Boolean, default=False, comment="isZeroOrder")
    skus: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="skus")
    offices: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="offices")
    address: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="address — адрес доставки")
    options: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="options")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class PickupOrder(Base):
    """Заказ самовывоза (Click & Collect). GET /api/v3/orders?deliveryType=pickup"""
    __tablename__ = "pickup_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True, comment="id — ID заказа")
    order_uid: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True, comment="orderUid — UUID заказа")
    group_id: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="groupId")
    rid: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="rid — ID позиции")
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="createdAt — дата создания")
    article: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="article — артикул продавца")
    nm_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="nmId — артикул WB")
    chrt_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="chrtId — ID размера")
    price: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="price — цена")
    converted_price: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="convertedPrice")
    currency_code: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="currencyCode")
    converted_currency_code: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="convertedCurrencyCode")
    delivery_type: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="deliveryType")
    warehouse_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="warehouseId")
    office_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="officeId")
    cargo_type: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="cargoType")
    comment: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="comment")
    is_zero_order: Mapped[bool] = mapped_column(Boolean, default=False, comment="isZeroOrder")
    skus: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="skus")
    address: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="address")
    options: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="options")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")

class FbsPass(Base):
    """??????? ?? ????? WB. GET /api/v3/passes"""
    __tablename__ = "fbs_passes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pass_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, nullable=True, comment="passId")
    warehouse_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="warehouseId")
    warehouse_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="warehouseName")
    status: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="status")
    date_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="dateStart")
    date_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="dateEnd")
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="firstName")
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="lastName")
    car_model: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="carModel")
    car_number: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="carNumber")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class FbsSupply(Base):
    """???????? FBS. GET /api/v3/supplies � Supply schema ?? YAML."""
    __tablename__ = "fbs_supplies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    supply_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True, comment="id � WB-GI-...")
    name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="name")
    is_b2b: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="isB2b")
    done: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="done")
    cargo_type: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="cargoType")
    cross_border_type: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="crossBorderType")
    destination_office_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="destinationOfficeId")
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="createdAt")
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="closedAt")
    scan_dt: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="scanDt")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
