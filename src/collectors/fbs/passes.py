"""Коллектор: FBS — Пропуска на склады WB."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.fbs.passes import PassOfficesResponse, PassesResponse, Pass


class PassesCollector:
    def __init__(self):
        self._client = WBApiClient(
            base_url=settings.WB_MARKETPLACE_URL,
            token=settings.WB_API_TOKEN,
        )

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_pass_offices(self) -> PassOfficesResponse:
        """GET /api/v3/passes/offices — склады, требующие пропуск."""
        data = await self._client.get("/api/v3/passes/offices")
        return PassOfficesResponse.model_validate(data if isinstance(data, dict) else {"offices": data or []})

    async def get_passes(self) -> PassesResponse:
        """GET /api/v3/passes — список пропусков продавца."""
        data = await self._client.get("/api/v3/passes")
        return PassesResponse.model_validate(data if isinstance(data, dict) else {"passes": data or []})

    async def create_pass(self, payload: dict) -> Pass:
        """POST /api/v3/passes — создать пропуск."""
        data = await self._client.post("/api/v3/passes", json=payload)
        return Pass.model_validate(data)

    async def update_pass(self, pass_id: int, payload: dict) -> dict:
        """PUT /api/v3/passes/{passId} — обновить пропуск."""
        return await self._client.put(f"/api/v3/passes/{pass_id}", json=payload)

    async def delete_pass(self, pass_id: int) -> None:
        """DELETE /api/v3/passes/{passId} — удалить пропуск."""
        await self._client.delete(f"/api/v3/passes/{pass_id}")
