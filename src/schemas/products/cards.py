"""Схемы: Товары — Карточки товаров."""
from typing import Any
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Вложенные схемы карточки
# ---------------------------------------------------------------------------

class CardPhoto(BaseModel):
    """Фотографии карточки товара в разных размерах."""
    big: str | None = Field(None, description="URL фото большого размера")
    c246x328: str | None = Field(None, description="URL фото 246×328 px")
    c516x688: str | None = Field(None, description="URL фото 516×688 px")
    square: str | None = Field(None, description="URL квадратного фото")
    tm: str | None = Field(None, description="URL миниатюры")


class CardSize(BaseModel):
    """Размер / вариант товара (SKU)."""
    chrtID: int | None = Field(None, description="ID характеристики размера")
    techSize: str = Field(default="", description="Технический размер (напр. '42', 'XL', '0')")
    wbSize: str = Field(default="", description="Размер в российской таблице WB")
    skus: list[str] = Field(default=[], description="Список баркодов (EAN-13) для данного размера")
    price: int | None = Field(None, description="Цена размера в копейках × 100 (напр. 300000 = 3000 ₽)")


class CardCharacteristic(BaseModel):
    """Характеристика карточки товара."""
    id: int = Field(description="ID характеристики (charcID из справочника)")
    name: str = Field(description="Название характеристики (напр. 'Цвет', 'Материал')")
    value: Any = Field(None, description="Значение характеристики (строка, число или список)")


class CardTag(BaseModel):
    """Тег, привязанный к карточке."""
    id: int = Field(description="ID тега")
    name: str = Field(description="Название тега")
    color: str = Field(description="Цвет тега в HEX без # (напр. 'D41D1D')")


class CardDimensions(BaseModel):
    """Габариты и вес товара."""
    length: float | None = Field(None, description="Длина упаковки, см")
    width: float | None = Field(None, description="Ширина упаковки, см")
    height: float | None = Field(None, description="Высота упаковки, см")
    weightBrutto: float | None = Field(None, description="Вес брутто (с упаковкой), кг")


# ---------------------------------------------------------------------------
# Карточка товара
# ---------------------------------------------------------------------------

class ProductCard(BaseModel):
    """Карточка товара WB."""
    nmID: int = Field(description="Артикул WB (числовой идентификатор карточки)")
    imtID: int | None = Field(None, description="ID предмета (группы карточек одного товара)")
    nmUUID: str | None = Field(None, description="UUID карточки")
    subjectID: int | None = Field(None, description="ID предмета (категории) карточки")
    subjectName: str | None = Field(None, description="Название предмета (напр. 'Футболка')")
    vendorCode: str = Field(default="", description="Артикул продавца (ваш внутренний код товара)")
    brand: str = Field(default="", description="Бренд товара")
    title: str = Field(default="", description="Наименование товара")
    description: str = Field(default="", description="Описание товара")
    needKiz: bool = Field(default=False, description="Требуется ли маркировка КИЗ (честный знак)")
    photos: list[CardPhoto] = Field(default=[], description="Фотографии товара")
    video: str | None = Field(None, description="URL видео товара")
    dimensions: CardDimensions | None = Field(None, description="Габариты и вес")
    characteristics: list[CardCharacteristic] = Field(default=[], description="Характеристики карточки")
    sizes: list[CardSize] = Field(default=[], description="Размеры / варианты товара с баркодами")
    tags: list[CardTag] = Field(default=[], description="Теги, привязанные к карточке")
    createdAt: str | None = Field(None, description="Дата создания карточки (ISO 8601)")
    updatedAt: str | None = Field(None, description="Дата последнего обновления (ISO 8601)")


# ---------------------------------------------------------------------------
# Список карточек (cursor-based пагинация)
# ---------------------------------------------------------------------------

class CardCursor(BaseModel):
    """Курсор для следующей страницы при запросе карточек."""
    updatedAt: str | None = Field(None, description="Дата обновления последней карточки в ответе — передать в следующий запрос")
    nmID: int | None = Field(None, description="nmID последней карточки в ответе — передать в следующий запрос")
    total: int = Field(default=0, description="Общее количество карточек (только в первом ответе)")


class CardsListResponse(BaseModel):
    """Ответ со списком карточек товаров."""
    cards: list[ProductCard] = Field(default=[], description="Список карточек")
    cursor: CardCursor | None = Field(None, description="Курсор для получения следующей страницы")


class CardsCursorRequest(BaseModel):
    """Курсор для запроса следующей страницы карточек."""
    updatedAt: str | None = Field(None, description="updatedAt из предыдущего ответа")
    nmID: int | None = Field(None, description="nmID из предыдущего ответа")
    limit: int = Field(default=100, ge=1, le=1000, description="Количество карточек на странице (1–1000)")


class CardsFilterRequest(BaseModel):
    """Фильтры для запроса карточек."""
    textSearch: str | None = Field(None, description="Поиск по названию, артикулу продавца или nmID")
    allowedCategoriesOnly: bool | None = Field(None, description="Только карточки разрешённых категорий")
    tagIDs: list[int] | None = Field(None, description="Фильтр по ID тегов")
    objectIDs: list[int] | None = Field(None, description="Фильтр по ID предметов (subjectID)")
    brands: list[str] | None = Field(None, description="Фильтр по названиям брендов")
    imtID: int | None = Field(None, description="Фильтр по imtID (группе карточек)")


class CardsListRequest(BaseModel):
    """Тело запроса для получения списка карточек товаров."""
    settings: dict | None = Field(
        None,
        description=(
            "Параметры запроса. Пример:\n"
            "```json\n"
            '{"cursor": {"limit": 100}, "filter": {"textSearch": "футболка"}}\n'
            "```"
        ),
    )


# ---------------------------------------------------------------------------
# Лимиты карточек
# ---------------------------------------------------------------------------

class CardLimits(BaseModel):
    """Лимиты на создание карточек товаров."""
    freeToUse: int | None = Field(None, description="Доступно для создания карточек прямо сейчас")
    freeLimitBase: int | None = Field(None, description="Базовый бесплатный лимит карточек")
    paidLimitBase: int | None = Field(None, description="Платный лимит карточек")
    used: int | None = Field(None, description="Использовано карточек из лимита")


class CardLimitsResponse(BaseModel):
    """Ответ с лимитами карточек."""
    error: bool = Field(default=False, description="Признак ошибки")
    errorText: str = Field(default="", description="Текст ошибки")
    data: CardLimits | Any = Field(None, description="Данные лимитов")


# ---------------------------------------------------------------------------
# Баркоды
# ---------------------------------------------------------------------------

class BarcodesResponse(BaseModel):
    """Ответ с созданными баркодами."""
    error: bool = Field(default=False, description="Признак ошибки")
    errorText: str = Field(default="", description="Текст ошибки")
    data: list[str] = Field(default=[], description="Список сгенерированных баркодов (EAN-13)")


# ---------------------------------------------------------------------------
# Карточки с ошибками
# ---------------------------------------------------------------------------

class CardErrorItem(BaseModel):
    """Карточка с ошибками при создании / редактировании."""
    batchUUID: str | None = Field(None, description="UUID батча загрузки")
    vendorCodes: list[str] = Field(default=[], description="Артикулы продавца с ошибками")
    errors: dict | None = Field(None, description="Список ошибок по полям")
    subjects: dict | None = Field(None, description="Ошибки по предметам")
    brands: dict | None = Field(None, description="Ошибки по брендам")


class CardErrorCursor(BaseModel):
    """Курсор пагинации для карточек с ошибками."""
    next: bool = Field(default=False, description="Есть ли следующая страница")
    updatedAt: str | None = Field(None, description="Дата последней ошибки в ответе")
    batchUUID: str | None = Field(None, description="UUID последнего батча в ответе")


class CardErrorData(BaseModel):
    items: list[CardErrorItem] = Field(default=[], description="Карточки с ошибками")
    cursor: CardErrorCursor | None = Field(None, description="Курсор для следующей страницы")


class CardErrorsResponse(BaseModel):
    """Ответ со списком карточек, содержащих ошибки."""
    error: bool = Field(default=False, description="Признак ошибки запроса")
    errorText: str = Field(default="", description="Текст ошибки запроса")
    data: CardErrorData | None = Field(None, description="Карточки с ошибками и курсор")
