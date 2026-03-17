"""ORM модели: Товары (Products)."""
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Float, Integer, Numeric, String, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class WbCard(Base):
    """Карточка товара WB."""
    __tablename__ = "wb_cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nm_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True, comment="Артикул WB (nmID)")
    imt_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="ID предмета (группа карточек одного товара)")
    nm_uuid: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="UUID карточки")
    subject_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="ID подкатегории")
    subject_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Название подкатегории")
    vendor_code: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True, comment="Артикул продавца")
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Бренд")
    title: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="Наименование товара")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Описание товара")
    in_trash: Mapped[bool] = mapped_column(Boolean, default=False, comment="В корзине")
    length: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Длина упаковки, см")
    width: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Ширина упаковки, см")
    height: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Высота упаковки, см")
    weight_brutto: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Вес брутто, кг")
    sizes: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="Размеры и SKU (JSON)")
    characteristics: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="Характеристики карточки (JSON)")
    photos: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="Фотографии карточки (JSON)")
    tags: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="Теги карточки (JSON)")
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата создания карточки")
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата обновления карточки")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbPrice(Base):
    """Цена и скидка товара WB."""
    __tablename__ = "wb_prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nm_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="Артикул WB (nmID)")
    vendor_code: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Артикул продавца")
    price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Цена до скидки, руб.")
    discount: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="Скидка продавца, %")
    discounted_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Цена со скидкой, руб.")
    club_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Цена клуба WB, руб.")
    currency_iso_code: Mapped[str | None] = mapped_column(String(10), nullable=True, comment="Код валюты ISO")
    editable: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="Доступна ли цена для изменения")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbTag(Base):
    """Тег товаров продавца."""
    __tablename__ = "wb_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tag_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, comment="ID тега WB")
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="Название тега")
    color: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="Цвет тега (HEX)")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbWarehouse(Base):
    """Склад продавца (Products)."""
    __tablename__ = "wb_seller_warehouses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    warehouse_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, comment="ID склада")
    name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Название склада")
    address: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="Адрес склада")
    work_time: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Режим работы")
    selected_coefficient: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Коэффициент склада")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")
