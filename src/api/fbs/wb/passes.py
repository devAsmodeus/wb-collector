"""
Контроллер: FBS / Пропуска на склады WB
WB API: marketplace-api.wildberries.ru

Пропуска нужны для въезда на склады WB, требующие регистрацию транспорта.
"""
from litestar import Controller, delete, get, post, put
from litestar.params import Parameter
from litestar.status_codes import HTTP_204_NO_CONTENT

from src.schemas.fbs.passes import (
    CreatePassRequest, Pass, PassesResponse,
    PassOfficesResponse, UpdatePassRequest,
)
from src.services.fbs.wb.passes import PassesService


class PassesController(Controller):
    path = "/passes"
    tags = ["03. API Wildberries"]

    @get(
        "/offices",
        summary="Склады, требующие пропуск",
        description=(
            "Возвращает список складов WB, для въезда на которые необходимо предварительно оформить пропуск.\n\n"
            "Перед созданием пропуска убедитесь, что нужный склад есть в этом списке.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/passes/offices`"
        ),
    )
    async def get_pass_offices(self) -> PassOfficesResponse:
        return await PassesService().get_pass_offices()

    @get(
        "/",
        summary="Список пропусков продавца",
        description=(
            "Возвращает все пропуска, оформленные продавцом.\n\n"
            "Для каждого пропуска указаны склад, автомобиль, водитель и срок действия.\n\n"
            "**WB endpoint:** `GET marketplace-api.wildberries.ru/api/v3/passes`"
        ),
    )
    async def get_passes(self) -> PassesResponse:
        return await PassesService().get_passes()

    @post(
        "/",
        summary="Создать пропуск на склад",
        description=(
            "Оформляет пропуск для въезда автомобиля на склад WB в указанный период.\n\n"
            "**Важно:** пропуск нужно оформить заранее — как правило, за сутки до приезда.\n\n"
            "Узнать список складов, требующих пропуск: `GET /fbs/wb/passes/offices`\n\n"
            "**WB endpoint:** `POST marketplace-api.wildberries.ru/api/v3/passes`"
        ),
    )
    async def create_pass(self, data: CreatePassRequest) -> Pass:
        return await PassesService().create_pass(data)

    @put(
        "/{pass_id:int}",
        summary="Обновить пропуск",
        description=(
            "Изменяет данные существующего пропуска: дату, авто, водителя.\n\n"
            "Передавайте только поля, которые нужно изменить — остальные останутся прежними.\n\n"
            "**WB endpoint:** `PUT marketplace-api.wildberries.ru/api/v3/passes/{passId}`"
        ),
    )
    async def update_pass(
        self,
        data: UpdatePassRequest,
        pass_id: int = Parameter(description="ID пропуска, который нужно обновить"),
    ) -> dict:
        return await PassesService().update_pass(pass_id, data)

    @delete(
        "/{pass_id:int}",
        status_code=HTTP_204_NO_CONTENT,
        summary="Удалить пропуск",
        description=(
            "Удаляет пропуск по его ID.\n\n"
            "Удалить можно только пропуска в статусе `active`. "
            "Уже использованные пропуска удалить нельзя.\n\n"
            "**WB endpoint:** `DELETE marketplace-api.wildberries.ru/api/v3/passes/{passId}`"
        ),
    )
    async def delete_pass(
        self,
        pass_id: int = Parameter(description="ID пропуска, который нужно удалить"),
    ) -> None:
        await PassesService().delete_pass(pass_id)
