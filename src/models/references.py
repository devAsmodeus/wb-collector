"""ORM модели: Справочники — тарифы, склады WB, комиссии."""
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Float, Integer, Numeric, String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class WbTariffCommission(Base):
    """Комиссия WB по категории товаров."""
    __tablename__ = "wb_tariffs_commission"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True, comment="ID категории")
    subject_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Название категории (предмет)")
    parent_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Родительская категория")
    kgvp_marketplace: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="Комиссия маркетплейс, %")
    kgvp_supplier: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="Комиссия поставщик, %")
    kgvp_supplier_express: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="Комиссия экспресс, %")
    return_cost: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="Стоимость возврата покупателя")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbTariffBox(Base):
    """Тариф на доставку и хранение коробами."""
    __tablename__ = "wb_tariffs_box"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    warehouse_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="ID склада WB")
    warehouse_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Название склада")
    dt_next_box: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата пересчёта")
    box_delivery_base: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="Базовый тариф доставки, руб.")
    box_delivery_liter: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="Тариф доставки за литр, руб.")
    box_delivery_additional_liter: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="Доп. литр доставки, руб.")
    box_storage_base: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True, comment="Базовый тариф хранения, руб./день")
    box_storage_liter: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True, comment="Тариф хранения за литр, руб./день")
    box_storage_additional_liter: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True, comment="Доп. литр хранения, руб./день")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbTariffPallet(Base):
    """Тариф на доставку и хранение паллетами."""
    __tablename__ = "wb_tariffs_pallet"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    warehouse_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="ID склада WB")
    warehouse_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Название склада")
    is_super_safe: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="Повышенная безопасность хранения")
    pallet_delivery_value_base: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="Базовый тариф доставки паллеты, руб.")
    pallet_delivery_value_liter: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True, comment="Тариф за литр, руб.")
    pallet_storage_value: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True, comment="Тариф хранения паллеты, руб./день")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbTariffSupply(Base):
    """Коэффициент склада для поставок."""
    __tablename__ = "wb_tariffs_supply"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    warehouse_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="ID склада WB")
    warehouse_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Название склада")
    coefficient: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Коэффициент: 0=бесплатно, -1=закрыт")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbSyncState(Base):
    """Состояние синхронизации по модулям."""
    __tablename__ = "wb_sync_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    module: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True, comment="Название модуля синхронизации")
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата последней успешной синхронизации")
    last_cursor: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Курсор пагинации (rrdid, offset и т.д.)")
    records_total: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="Всего записей в БД")
    status: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="ok / error / running")
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="Сообщение об ошибке")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, comment="Дата обновления записи")
