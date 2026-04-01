"""
Контроллер: Products / Справочники
WB API: content-api.wildberries.ru

Справочники используются при создании и редактировании карточек товаров:
категории, предметы, характеристики, бренды, цвета, сезоны и т.д.
"""
from litestar import Controller, get
from litestar.params import Parameter

from src.schemas.products.directories import (
    BrandsResponse,
    DirectoryResponse,
    ParentCategoriesResponse,
    SubjectCharcsResponse,
    SubjectsResponse,
)
from src.services.products.wb.directories import DirectoriesService


class DirectoriesController(Controller):
    path = "/directories"
    tags = ["02. API Wildberries"]

    @get(
        "/categories",
        summary="Родительские категории товаров",
        description=(
            "Возвращает список всех родительских категорий товаров WB "
            "(напр. 'Электроника', 'Одежда', 'Дом и сад').\n\n"
            "Категории используются для навигации и выбора предмета при создании карточки.\n\n"
            "**WB endpoint:** `GET content-api.wildberries.ru/api/v2/object/parent/all`"
        ),
    )
    async def get_parent_categories(
        self,
        locale: str = Parameter(
            "ru",
            query="locale",
            description=(
                "Язык ответа. Поддерживаемые значения: "
                "`ru` — русский (по умолчанию), "
                "`en` — английский, "
                "`zh` — китайский."
            ),
        ),
    ) -> ParentCategoriesResponse:
        return await DirectoriesService().get_parent_categories(locale=locale)

    @get(
        "/subjects",
        summary="Предметы (подкатегории товаров)",
        description=(
            "Возвращает список предметов — подкатегорий, к которым относится товар "
            "(напр. 'Футболка', 'Смартфон', 'Диван').\n\n"
            "Предмет определяет набор обязательных и дополнительных характеристик карточки.\n\n"
            "Поиск по имени работает по частичному совпадению.\n\n"
            "**WB endpoint:** `GET content-api.wildberries.ru/api/v2/object/all`"
        ),
    )
    async def get_subjects(
        self,
        name: str | None = Parameter(
            None,
            query="name",
            description=(
                "Фильтр по названию предмета (частичное совпадение, регистронезависимо).\n"
                "Напр. `футбол` вернёт 'Футболка', 'Футбол' и др."
            ),
        ),
        limit: int = Parameter(
            1000,
            query="limit",
            ge=1,
            le=1000,
            description="Максимальное количество предметов в ответе. Диапазон: 1–1000. По умолчанию: 1000.",
        ),
    ) -> SubjectsResponse:
        return await DirectoriesService().get_subjects(name=name, limit=limit)

    @get(
        "/subjects/{subject_id:int}/charcs",
        summary="Характеристики предмета",
        description=(
            "Возвращает список всех характеристик для указанного предмета "
            "(напр. для 'Футболка': Цвет, Размер, Материал, Пол и др.).\n\n"
            "Характеристики с `required=true` обязательны для заполнения карточки.\n\n"
            "**WB endpoint:** `GET content-api.wildberries.ru/api/v2/object/charcs/{subjectId}`"
        ),
    )
    async def get_subject_charcs(
        self,
        subject_id: int = Parameter(description="ID предмета (subjectID из `/directories/subjects`)"),
    ) -> SubjectCharcsResponse:
        return await DirectoriesService().get_subject_charcs(subject_id)

    @get(
        "/subjects/{subject_id:int}/brands",
        summary="Бренды предмета",
        description=(
            "Возвращает список брендов, доступных для указанного предмета.\n\n"
            "Используется при заполнении поля 'Бренд' в карточке товара.\n\n"
            "**WB endpoint:** `GET content-api.wildberries.ru/api/v2/directory/brands`"
        ),
    )
    async def get_brands(
        self,
        subject_id: int = Parameter(description="ID предмета (subjectID из `/directories/subjects`)"),
    ) -> BrandsResponse:
        return await DirectoriesService().get_brands(subject_id)

    @get(
        "/{kind:str}",
        summary="Универсальный справочник",
        description=(
            "Возвращает элементы одного из стандартных справочников WB.\n\n"
            "**Доступные справочники (`kind`):**\n"
            "- `colors` — цвета\n"
            "- `kinds` — виды (пол: мужской, женский, унисекс)\n"
            "- `countries` — страны производства\n"
            "- `seasons` — сезоны (лето, зима, демисезон и др.)\n"
            "- `vat` — ставки НДС\n\n"
            "**WB endpoint:** `GET content-api.wildberries.ru/api/v2/directory/{kind}`"
        ),
    )
    async def get_directory(
        self,
        kind: str = Parameter(
            description=(
                "Тип справочника. Допустимые значения: "
                "`colors`, `kinds`, `countries`, `seasons`, `vat`."
            )
        ),
    ) -> DirectoryResponse:
        return await DirectoriesService().get_directory(kind)
