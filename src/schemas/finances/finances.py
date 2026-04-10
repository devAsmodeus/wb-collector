"""Схемы: Финансы WB."""
from pydantic import BaseModel, Field


class BalanceResponse(BaseModel):
    """Баланс продавца."""
    balance: float | None = Field(None, description="Баланс, руб.")


class FinancialReportItem(BaseModel):
    """Строка детального финансового отчёта."""
    realizationreport_id: int | None = Field(None, description="ID отчёта о реализации")
    date_from: str | None = Field(None, description="Дата начала отчётного периода (ISO 8601)")
    date_to: str | None = Field(None, description="Дата окончания отчётного периода (ISO 8601)")
    create_dt: str | None = Field(None, description="Дата формирования отчёта (ISO 8601)")
    supplier_name: str | None = Field(None, description="Наименование поставщика")
    rrd_id: int | None = Field(None, description="ID строки отчёта")
    gi_id: int | None = Field(None, description="ID поставки")
    subject_name: str | None = Field(None, description="Предмет")
    nm_id: int | None = Field(None, description="Артикул WB (nmID)")
    brand_name: str | None = Field(None, description="Бренд")
    sa_name: str | None = Field(None, description="Артикул продавца")
    ts_name: str | None = Field(None, description="Размер")
    barcode: str | None = Field(None, description="Баркод")
    doc_type_name: str | None = Field(None, description="Тип документа")
    quantity: int | None = Field(None, description="Количество")
    retail_price: float | None = Field(None, description="Цена розничная, руб.")
    retail_amount: float | None = Field(None, description="Сумма продаж, руб.")
    sale_percent: float | None = Field(None, description="Согласованная скидка, %")
    commission_percent: float | None = Field(None, description="Процент комиссии WB")
    office_name: str | None = Field(None, description="Название офиса/склада доставки")
    supplier_oper_name: str | None = Field(None, description="Обоснование для оплаты")
    order_dt: str | None = Field(None, description="Дата заказа (ISO 8601)")
    sale_dt: str | None = Field(None, description="Дата продажи (ISO 8601)")
    rr_dt: str | None = Field(None, description="Дата операции (ISO 8601)")
    shk_id: int | None = Field(None, description="ID штрих-кода")
    retail_price_withdisc_rub: float | None = Field(None, description="Цена розничная с учётом согласованной скидки, руб.")
    delivery_amount: float | None = Field(None, description="Количество доставок")
    return_amount: float | None = Field(None, description="Количество возвратов")
    delivery_rub: float | None = Field(None, description="Стоимость логистики, руб.")
    gi_box_type_name: str | None = Field(None, description="Тип коробов")
    product_discount_for_report: float | None = Field(None, description="Согласованный продуктовый дисконт, %")
    supplier_promo: float | None = Field(None, description="Промокод поставщика")
    rid: int | None = Field(None, description="ID заказа")
    ppvz_spp_prc: float | None = Field(None, description="Скидка постоянного покупателя, %")
    ppvz_kvw_prc_base: float | None = Field(None, description="Размер КВВ без учёта WB скидки, %")
    ppvz_kvw_prc: float | None = Field(None, description="Итоговый КВВ, %")
    sup_rating_prc_up: float | None = Field(None, description="Повышение рейтинга, %")
    is_kgvp_v2: float | None = Field(None, description="Признак КГВП v2")
    ppvz_sales_commission: float | None = Field(None, description="Вознаграждение с продаж до вычета КВВ, руб.")
    ppvz_for_pay: float | None = Field(None, description="К перечислению продавцу за реализованный товар, руб.")
    ppvz_reward: float | None = Field(None, description="Вознаграждение WB, руб.")
    acquiring_fee: float | None = Field(None, description="Расходы на эквайринг, руб.")
    acquiring_bank: str | None = Field(None, description="Банк-эквайер")
    ppvz_vw: float | None = Field(None, description="Вознаграждение WB без НДС, руб.")
    ppvz_vw_nds: float | None = Field(None, description="НДС с вознаграждения WB, руб.")
    ppvz_office_id: int | None = Field(None, description="ID офиса WB")
    ppvz_office_name: str | None = Field(None, description="Название офиса WB")
    ppvz_supplier_id: int | None = Field(None, description="ID партнёра WB")
    ppvz_supplier_name: str | None = Field(None, description="Наименование партнёра WB")
    ppvz_inn: str | None = Field(None, description="ИНН партнёра WB")
    declaration_number: str | None = Field(None, description="Номер таможенной декларации")
    bonus_type_name: str | None = Field(None, description="Тип бонуса")
    sticker_id: str | None = Field(None, description="ID стикера")
    site_country: str | None = Field(None, description="Страна продажи")
    penalty: float | None = Field(None, description="Штрафы, руб.")
    additional_payment: float | None = Field(None, description="Доплаты, руб.")
    rebill_logistic_cost: float | None = Field(None, description="Стоимость возвратной логистики, руб.")
    rebill_logistic_org: str | None = Field(None, description="Организация возвратной логистики")
    kiz: str | None = Field(None, description="КИЗ — код идентификации знака маркировки")
    storage_fee: float | None = Field(None, description="Стоимость хранения, руб.")
    deduction: float | None = Field(None, description="Прочие удержания, руб.")
    acceptance: float | None = Field(None, description="Стоимость платной приёмки, руб.")
    srid: str | None = Field(None, description="Уникальный ID заказа")


class DocumentCategory(BaseModel):
    """Категория документа."""
    id: int | None = Field(None, description="ID категории")
    name: str | None = Field(None, description="Название категории документов")


class DocumentItem(BaseModel):
    """Документ продавца."""
    id: int | None = Field(None, description="ID документа")
    name: str | None = Field(None, description="Название документа")
    category: str | None = Field(None, description="Категория документа")
    createdAt: str | None = Field(None, description="Дата создания документа (ISO 8601)")
    serviceName: str | None = Field(None, description="Сервис, создавший документ")


class DocumentsResponse(BaseModel):
    """Список документов."""
    documents: list[DocumentItem] | None = Field(None, description="Документы продавца")
    total: int | None = Field(None, description="Общее количество документов")


class DownloadAllDocumentsRequest(BaseModel):
    """Запрос на скачивание всех документов."""
    serviceNames: list[str] = Field(description="Список сервисов, документы которых скачать")
    extension: str | None = Field(None, description="Формат файла: `pdf`, `xlsx`")
