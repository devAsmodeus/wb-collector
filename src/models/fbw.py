"""ORM модели: FBW (07) — Поставки FBW (Fulfillment by Wildberries)."""
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class FbwWarehouse(Base):
    """Склад WB для поставок FBW."""
    __tablename__ = "fbw_warehouses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="ID склада WB")
    name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Название склада")
    address: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="Адрес склада")
    work_time: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Режим работы")
    accepts_qr: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="Принимает QR-поставки")
    raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True, comment="Исходные данные WB (JSON)")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class FbwTransitTariff(Base):
    """Тариф транзитной доставки между складами WB."""
    __tablename__ = "fbw_transit_tariffs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    transit_warehouse_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="Транзитный склад")
    destination_warehouse_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="Склад назначения")
    active_from: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Дата начала действия (ISO 8601)")
    box_tariff: Mapped[dict | None] = mapped_column(JSONB, nullable=True, comment="Тарифы за транзит коробов (JSON)")
    pallet_tariff: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Тариф за паллету, руб.")
    raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True, comment="Исходные данные WB (JSON)")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")

    __table_args__ = (
        UniqueConstraint("transit_warehouse_name", "destination_warehouse_name", name="uq_fbw_transit_tariff_route"),
    )


class FbwSupply(Base):
    """Поставка FBW."""
    __tablename__ = "fbw_supplies"

    supply_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="ID поставки WB (supplyID)")
    preorder_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="ID заказа (preorderID)")
    status_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="ID статуса (1-5)")
    box_type_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="ID типа поставки (0-5)")
    is_box_on_pallet: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="Поштучная паллета")
    create_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата создания")
    supply_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Плановая дата отгрузки")
    fact_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата фактической отгрузки")
    updated_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="Дата последнего изменения")
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Телефон")
    raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True, comment="Исходные данные WB (JSON)")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class FbwSupplyGood(Base):
    """Товар в поставке FBW."""
    __tablename__ = "fbw_supply_goods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    supply_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="ID поставки FBW")
    barcode: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Баркод товара")
    vendor_code: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Артикул продавца")
    name: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="Наименование товара")
    quantity: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Количество в поставке")
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Бренд товара")
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Предмет товара")
    raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True, comment="Исходные данные WB (JSON)")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")

    __table_args__ = (
        UniqueConstraint("supply_id", "barcode", name="uq_fbw_supply_good"),
    )
