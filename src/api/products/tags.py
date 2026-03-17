"""
Контроллер: Products / Теги
WB API: content-api.wildberries.ru

Теги позволяют группировать карточки товаров в кабинете продавца
для удобной фильтрации и управления ассортиментом.
"""
from litestar import Controller, delete, get, patch, post
from litestar.params import Parameter
from litestar.status_codes import HTTP_204_NO_CONTENT

from src.schemas.products.tags import (
    TagCreateRequest,
    TagLinkRequest,
    TagsResponse,
    TagUpdateRequest,
)
from src.services.products.tags import TagsService


class TagsController(Controller):
    path = "/tags"
    tags = ["Products — Теги"]

    @get(
        "/",
        summary="Список тегов продавца",
        description=(
            "Возвращает все теги, созданные в кабинете продавца.\n\n"
            "Теги используются для группировки и фильтрации карточек товаров "
            "в интерфейсе кабинета (напр. 'Акция', 'Новинка', 'Под заказ').\n\n"
            "**WB endpoint:** `GET content-api.wildberries.ru/api/v2/tags`"
        ),
    )
    async def get_tags(self) -> TagsResponse:
        return await TagsService().get_tags()

    @post(
        "/",
        summary="Создать тег",
        description=(
            "Создаёт новый тег для группировки карточек товаров.\n\n"
            "После создания тег можно привязать к карточкам через `POST /tags/link`.\n\n"
            "Максимальное количество тегов в кабинете — **30**.\n\n"
            "**WB endpoint:** `POST content-api.wildberries.ru/api/v2/tags`"
        ),
    )
    async def create_tag(self, data: TagCreateRequest) -> TagsResponse:
        return await TagsService().create_tag(name=data.name, color=data.color)

    @patch(
        "/{tag_id:int}",
        summary="Изменить тег",
        description=(
            "Обновляет название и/или цвет существующего тега.\n\n"
            "Можно передать только `name`, только `color` или оба поля сразу.\n\n"
            "**WB endpoint:** `PATCH content-api.wildberries.ru/api/v2/tags/{tagID}`"
        ),
    )
    async def update_tag(
        self,
        data: TagUpdateRequest,
        tag_id: int = Parameter(description="ID тега, который нужно изменить"),
    ) -> TagsResponse:
        return await TagsService().update_tag(
            tag_id=tag_id,
            name=data.name,
            color=data.color,
        )

    @delete(
        "/{tag_id:int}",
        status_code=HTTP_204_NO_CONTENT,
        summary="Удалить тег",
        description=(
            "Удаляет тег по его ID.\n\n"
            "Тег автоматически отвязывается от всех карточек товаров, к которым был привязан.\n\n"
            "Операция необратима.\n\n"
            "**WB endpoint:** `DELETE content-api.wildberries.ru/api/v2/tags/{tagID}`"
        ),
    )
    async def delete_tag(
        self,
        tag_id: int = Parameter(description="ID тега, который нужно удалить"),
    ) -> None:
        await TagsService().delete_tag(tag_id)

    @post(
        "/link",
        status_code=HTTP_204_NO_CONTENT,
        summary="Привязать / отвязать теги к карточке",
        description=(
            "Устанавливает список тегов для карточки товара.\n\n"
            "**Логика работы:** переданный список **полностью заменяет** текущие теги карточки.\n\n"
            "- Передайте `tagIDs: [1, 2, 3]` — карточка получит эти теги.\n"
            "- Передайте `tagIDs: []` — все теги с карточки будут сняты.\n\n"
            "**WB endpoint:** `POST content-api.wildberries.ru/api/v2/tags/goods/link`"
        ),
    )
    async def link_tags(self, data: TagLinkRequest) -> None:
        await TagsService().link_tags(nm_id=data.nmID, tag_ids=data.tagIDs)
