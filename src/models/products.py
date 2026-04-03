"""ORM модели: Товары (Products)."""
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Float, Integer, Numeric, String, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class WbCard(Base):
    """Карточка товара WB. POST /content/v2/get/cards/list"""
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nm_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True, comment="nmID — Артикул WB")
    imt_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="imtID — ID группы карточек")
    nm_uuid: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="nmUUID — UUID карточки")
    subject_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="subjectId — ID подкатегории")
    subject_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="subjectName — Название подкатегории")
    vendor_code: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True, comment="vendorCode — Артикул продавца")
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="brand — Бренд")
    title: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="title — Наименование товара")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="description — Описание товара")
    in_trash: Mapped[bool] = mapped_column(Boolean, default=False, comment="inTrash — В корзине")
    # dimensions (объект в API разбит на поля)
    length: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="dimensions.length — Длина упаковки, см")
    width: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="dimensions.width — Ширина упаковки, см")
    height: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="dimensions.height — Высота упаковки, см")
    weight_brutto: Mapped[float | None] = mapped_column(Float, nullable=True, comment="dimensions.weightBrutto — Вес брутто, кг")
    dimensions_valid: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="dimensions.isValid — Корректность габаритов")
    sizes: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="sizes — Размеры и SKU (JSON)")
    characteristics: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="characteristics — Характеристики (JSON)")
    photos: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="photos — Фотографии (JSON)")
    tags: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="tags — Теги карточки (JSON)")
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="createdAt — Дата создания")
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="updatedAt — Дата обновления")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbPrice(Base):
    """Цена и скидка товара WB. GET /api/v2/list/goods/filter (GoodsList)"""
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nm_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True, comment="nmID — Артикул WB")
    vendor_code: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="vendorCode — Артикул продавца")
    sizes: Mapped[list | None] = mapped_column(JSON, nullable=True, comment="sizes — Цены по размерам (JSON)")
    currency_iso_code: Mapped[str | None] = mapped_column(String(10), nullable=True, comment="currencyIsoCode4217 — Код валюты ISO")
    discount: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="discount — Скидка продавца, %")
    club_discount: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="clubDiscount — Скидка клуба WB, %")
    editable_size_price: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="editableSizePrice — Редактируемая цена по размеру")
    is_bad_turnover: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="isBadTurnover — Плохая оборачиваемость")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbTag(Base):
    """Тег товаров продавца. GET /content/v2/tags"""
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tag_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, comment="id — ID тега WB")
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="name — Название тега")
    color: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="color — Цвет тега (HEX)")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbWarehouse(Base):
    """Склад продавца. GET /api/v3/warehouses (Warehouse schema)"""
    __tablename__ = "seller_warehouses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    warehouse_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, comment="id — ID склада WB")
    name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="name — Название склада")
    office_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="officeId — ID офиса")
    cargo_type: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="cargoType — Тип груза")
    delivery_type: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="deliveryType — Тип доставки")
    is_deleting: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="isDeleting — В процессе удаления")
    is_processing: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="isProcessing — В процессе создания")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbCategory(Base):
    """Родительская категория WB. GET /content/v2/object/parent/all"""
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True, comment="ID родительской категории")
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="Название категории")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbSubject(Base):
    """Предмет (подкатегория) WB. GET /content/v2/object/all"""
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True, comment="subjectID — ID предмета")
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="subjectName — Название предмета")
    parent_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="parentID — ID родительской категории")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")
