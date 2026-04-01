"""Коллектор: Коммуникации — Отзывы."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.communications.feedbacks import (
    FeedbackCountUnanswered,
    FeedbackCount,
    FeedbacksResponse,
)


class FeedbacksCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_FEEDBACKS_URL, token=settings.WB_API_TOKEN, timeout=120)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_count_unanswered(self) -> FeedbackCountUnanswered:
        data = await self._client.get("/api/v1/feedbacks/count-unanswered")
        return FeedbackCountUnanswered.model_validate(data if isinstance(data, dict) else {})

    async def get_count(self, has_answer: bool | None = None) -> FeedbackCount:
        params: dict = {}
        if has_answer is not None:
            params["hasAnswer"] = str(has_answer).lower()
        data = await self._client.get("/api/v1/feedbacks/count", params=params)
        return FeedbackCount.model_validate(data if isinstance(data, dict) else {})

    async def get_list(
        self,
        is_answered: bool = False,
        nm_id: int | None = None,
        limit: int = 10,
        offset: int = 0,
        order: str = "dateDesc",
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> FeedbacksResponse:
        params: dict = {"isAnswered": str(is_answered).lower(), "take": limit, "skip": offset, "order": order}
        if nm_id: params["nmId"] = nm_id
        if date_from: params["dateFrom"] = date_from
        if date_to: params["dateTo"] = date_to
        data = await self._client.get("/api/v1/feedbacks", params=params)
        return FeedbacksResponse.model_validate(data if isinstance(data, dict) else {})

    async def answer_feedback(self, payload: dict) -> dict:
        return await self._client.post("/api/v1/feedbacks/answer", json=payload)

    async def update_feedback_answer(self, payload: dict) -> dict:
        return await self._client.patch("/api/v1/feedbacks/answer", json=payload)

    async def request_return(self, payload: dict) -> dict:
        return await self._client.post("/api/v1/feedbacks/order/return", json=payload)

    async def get_feedback(self, feedback_id: str) -> dict:
        return await self._client.get("/api/v1/feedback", params={"id": feedback_id})

    async def get_archive(
        self,
        nm_id: int | None = None,
        limit: int = 10,
        offset: int = 0,
        order: str = "dateDesc",
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> dict:
        params: dict = {"take": limit, "skip": offset, "order": order}
        if nm_id: params["nmId"] = nm_id
        if date_from: params["dateFrom"] = date_from
        if date_to: params["dateTo"] = date_to
        return await self._client.get("/api/v1/feedbacks/archive", params=params)
