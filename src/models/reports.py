"""ORM модели: Отчёты (Statistics API) — stocks, orders, sales, financial report."""
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Float, Integer, Numeric, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class WbStock(Base):
    """Остаток товара на складе WB (statistics-api)."""
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    last_change_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="Дата последнего изменения")
    supplier_article: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Артикул поставщика")
    tech_size: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Размер")
    barcode: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True, comment="Баркод")
    quantity: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Количество на складе WB")
    is_supply: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="Признак поставки FBO")
    is_realization: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="Признак реализации")
    quantity_full: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Полное количество (с браком)")
    in_way_to_client: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="В пути к покупателю")
    in_way_from_client: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="В пути от покупателя")
    nm_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="Артикул WB (nmID)")
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Предмет")
    category: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Категория")
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Бренд")
    sc_code: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Код WB склада")
    price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Цена товара, руб.")
    discount: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="Скидка, %")
    warehouse_name: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True, comment="Название склада")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbOrderReport(Base):
    """Заказ из отчёта (statistics-api /api/v1/supplier/orders)."""
    __tablename__ = "orders_report"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    odid: Mapped[int | None] = mapped_column(BigInteger, unique=True, nullable=True, index=True, comment="ID уникальной позиции заказа")
    date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="Дата заказа")
    last_change_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата последнего изменения")
    supplier_article: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Артикул поставщика")
    tech_size: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Размер")
    barcode: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True, comment="Баркод")
    total_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Цена до скидки, руб.")
    discount_percent: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="Скидка продавца, %")
    warehouse_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Склад WB")
    oblast: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Регион доставки")
    income_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="ID поставки")
    nm_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="Артикул WB (nmID)")
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Предмет")
    category: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Категория")
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Бренд")
    is_cancel: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="Отменён")
    cancel_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата отмены")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbSaleReport(Base):
    """Продажа / возврат из отчёта (statistics-api /api/v1/supplier/sales)."""
    __tablename__ = "sales_report"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    srid: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True, index=True, comment="Уникальный ID продажи/возврата")
    sale_id: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True, comment="S = продажа, R = возврат")
    date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="Дата продажи/возврата")
    last_change_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата изменения")
    supplier_article: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Артикул поставщика")
    tech_size: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Размер")
    barcode: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True, comment="Баркод")
    total_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Цена до скидки, руб.")
    discount_percent: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="Скидка, %")
    is_supply: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="Тип операции: поставка")
    is_realization: Mapped[bool | None] = mapped_column(Boolean, nullable=True, comment="Тип операции: реализация")
    warehouse_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Склад WB")
    oblast: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Регион")
    income_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="ID поставки")
    odid: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="ID позиции заказа")
    nm_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="Артикул WB (nmID)")
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Предмет")
    category: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Категория")
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Бренд")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")


class WbFinancialReport(Base):
    """Детальный финансовый отчёт (reportDetailByPeriod)."""
    __tablename__ = "financial_report"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rrd_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True, comment="ID строки отчёта")
    realizationreport_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="ID отчёта о реализации")
    date_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата начала периода")
    date_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата окончания периода")
    create_dt: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата формирования отчёта")
    supplier_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Наименование поставщика")
    nm_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True, comment="Артикул WB (nmID)")
    brand_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Бренд")
    sa_name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Артикул продавца")
    ts_name: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Размер")
    barcode: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True, comment="Баркод")
    subject_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Предмет")
    doc_type_name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Тип документа")
    quantity: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Количество")
    retail_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Розничная цена, руб.")
    retail_amount: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Сумма продаж, руб.")
    sale_percent: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="Согласованная скидка, %")
    commission_percent: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="Комиссия WB, %")
    office_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Офис/склад доставки")
    supplier_oper_name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Обоснование для оплаты")
    order_dt: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="Дата заказа")
    sale_dt: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True, comment="Дата продажи")
    rr_dt: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="Дата операции")
    retail_price_withdisc_rub: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Цена с согласованной скидкой, руб.")
    delivery_amount: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Количество доставок")
    return_amount: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Количество возвратов")
    delivery_rub: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Стоимость логистики, руб.")
    ppvz_for_pay: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="К перечислению продавцу, руб.")
    ppvz_reward: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Вознаграждение WB, руб.")
    ppvz_sales_commission: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Вознаграждение с продаж, руб.")
    ppvz_vw: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Вознаграждение WB без НДС, руб.")
    ppvz_vw_nds: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="НДС с вознаграждения WB, руб.")
    acquiring_fee: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Расходы на эквайринг, руб.")
    penalty: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Штрафы, руб.")
    additional_payment: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Доплаты, руб.")
    storage_fee: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Стоимость хранения, руб.")
    deduction: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Прочие удержания, руб.")
    acceptance: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Стоимость платной приёмки, руб.")
    rebill_logistic_cost: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True, comment="Возвратная логистика, руб.")
    site_country: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Страна продажи")
    srid: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True, comment="Уникальный ID заказа")
    gi_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="ID поставки")
    rid: Mapped[int | None] = mapped_column(BigInteger, nullable=True, comment="ID заказа")
    kiz: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="КИЗ маркировки")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, comment="Дата синхронизации")
