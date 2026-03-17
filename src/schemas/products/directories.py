"""Схемы: Товары — Справочники (категории, предметы, характеристики, бренды)."""
from typing import Any
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Базовый ответ WB API
# ---------------------------------------------------------------------------

class WBResponse(BaseModel):
    """Стандартная обёртка ответа WB API."""
    error: bool = Field(default=False, description="Признак ошибки")
    errorText: str = Field(default="", description="Текст ошибки (если error=true)")
    additionalErrors: Any = Field(default=None, description="Дополнительные ошибки")


# ---------------------------------------------------------------------------
# Категории
# ---------------------------------------------------------------------------

class ParentCategory(BaseModel):
    """Родительская категория товаров."""
    id: int | None = Field(None, description="ID категории")
    name: str | None = Field(None, description="Название категории (напр. 'Электроника', 'Одежда')")


class ParentCategoriesResponse(WBResponse):
    """Список родительских категорий товаров."""
    data: list[ParentCategory] | Any = Field(None, description="Список категорий")


# ---------------------------------------------------------------------------
# Предметы (subjects)
# ---------------------------------------------------------------------------

class Subject(BaseModel):
    """Предмет — подкатегория товара (напр. 'Футболка', 'Смартфон')."""
    subjectID: int = Field(description="ID предмета")
    parentID: int = Field(description="ID родительской категории")
    subjectName: str = Field(description="Название предмета (напр. 'Футболка')")
    parentName: str = Field(description="Название родительской категории (напр. 'Одежда')")


class SubjectsResponse(WBResponse):
    """Список предметов."""
    data: list[Subject] = Field(default=[], description="Список предметов")


# ---------------------------------------------------------------------------
# Характеристики предмета
# ---------------------------------------------------------------------------

class SubjectCharc(BaseModel):
    """Характеристика предмета (напр. 'Цвет', 'Размер', 'Материал')."""
    charcID: int = Field(description="ID характеристики")
    subjectName: str = Field(description="Название предмета, к которому относится характеристика")
    subjectID: int = Field(description="ID предмета")
    name: str = Field(description="Название характеристики (напр. 'Цвет', 'Пол')")
    required: bool = Field(default=False, description="Обязательна ли характеристика для заполнения карточки")
    unitName: str = Field(default="", description="Единица измерения (напр. 'см', 'кг'). Пустая строка если не применимо.")
    maxCount: int = Field(default=0, description="Максимальное количество значений. 0 — без ограничений.")
    popular: bool = Field(default=False, description="Популярная ли характеристика (используется для сортировки в интерфейсе)")
    charcType: int = Field(
        default=1,
        description=(
            "Тип значения характеристики: "
            "`1` — строка, "
            "`2` — число, "
            "`4` — список значений."
        ),
    )


class SubjectCharcsResponse(WBResponse):
    """Список характеристик предмета."""
    data: list[SubjectCharc] = Field(default=[], description="Список характеристик")


# ---------------------------------------------------------------------------
# ТНВЭД коды
# ---------------------------------------------------------------------------

class TnvedCode(BaseModel):
    """Код ТНВЭД для таможенного оформления."""
    tnved: str = Field(description="Код ТНВЭД (10 цифр)")
    isKiz: bool = Field(default=False, description="Требуется ли маркировка КИЗ (честный знак)")


class TnvedResponse(WBResponse):
    """Список ТНВЭД кодов."""
    data: list[TnvedCode] = Field(default=[], description="Список кодов ТНВЭД")


# ---------------------------------------------------------------------------
# Бренды
# ---------------------------------------------------------------------------

class Brand(BaseModel):
    """Бренд товара."""
    id: int = Field(description="ID бренда")
    name: str = Field(description="Название бренда")
    logoUrl: str | None = Field(None, description="URL логотипа бренда (если есть)")


class BrandsResponse(BaseModel):
    """Список брендов с пагинацией."""
    brands: list[Brand] = Field(default=[], description="Список брендов")
    next: int | None = Field(None, description="Курсор для следующей страницы (передать как offset в следующем запросе)")
    total: int = Field(default=0, description="Общее количество брендов")


# ---------------------------------------------------------------------------
# Универсальные справочники (цвета, виды, страны, сезоны, НДС)
# ---------------------------------------------------------------------------

class DirectoryItem(BaseModel):
    """Элемент универсального справочника."""
    id: int | None = Field(None, description="ID элемента справочника")
    name: str = Field(description="Название элемента (напр. 'Красный', 'Россия', 'Зима')")


class DirectoryResponse(BaseModel):
    """Ответ универсального справочника."""
    data: list[DirectoryItem] = Field(default=[], description="Список элементов справочника")
