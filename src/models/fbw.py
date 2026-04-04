"""ORM модели: FBW (07) — Поставки FBW (Fulfillment by Wildberries).

Все таблицы строго по схемам supplies-api.wildberries.ru (07-orders-fbw.yaml).
"""
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class FbwWarehouse(Base):
    """Склад WB. GET /api/v1/warehouses — models.WarehousesResultItems из YAML."""
    __tablename__ = "fbw_warehouses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="ID")
    name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="name")
    address: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="address")
    work_time: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="workTime")
    is_active: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="isActive")
    is_transit_active: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="isTransitActive")
    raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class FbwTransitTariff(Base):
    """Тариф транзита. GET /api/v1/transit-tariffs — models.TransitTariff из YAML."""
    __tablename__ = "fbw_transit_tariffs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    transit_warehouse_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="transitWarehouseName")
    destination_warehouse_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="destinationWarehouseName")
    active_from: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="activeFrom")
    box_tariff: Mapped[dict | None] = mapped_column(JSONB, nullable=True, comment="boxTariff")
    pallet_tariff: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="palletTariff")
    raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("transit_warehouse_name", "destination_warehouse_name", name="uq_fbw_transit_tariff_route"),
    )


class FbwSupply(Base):
    """Поставка FBW. POST /api/v1/supplies — models.Supply из YAML."""
    __tablename__ = "fbw_supplies"

    supply_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="supplyID")
    preorder_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="preorderID")
    status_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="statusID")
    box_type_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="boxTypeID")
    is_box_on_pallet: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="isBoxOnPallet")
    create_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="createDate")
    supply_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="supplyDate")
    fact_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="factDate")
    updated_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="updatedDate")
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="phone")
    raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class FbwSupplyGood(Base):
    """Товар в поставке FBW. GET /api/v1/supplies/{ID}/goods — models.GoodInSupply из YAML."""
    __tablename__ = "fbw_supply_goods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    supply_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="supplyID")
    barcode: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="barcode")
    vendor_code: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="vendorCode")
    nm_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="nmID")
    need_kiz: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="needKiz")
    tnved: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="tnved")
    tech_size: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="techSize")
    color: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="color")
    supplier_box_amount: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="supplierBoxAmount")
    quantity: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="quantity")
    ready_for_sale_quantity: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="readyForSaleQuantity")
    accepted_quantity: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="acceptedQuantity")
    unloading_quantity: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="unloadingQuantity")
    raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("supply_id", "barcode", name="uq_fbw_supply_good"),
    )
