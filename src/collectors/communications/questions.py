"""Коллектор: Коммуникации — Вопросы."""
from src.collectors.base import WBApiClient
from src.config import settings
from src.schemas.communications.questions import (
    QuestionCountUnanswered,
    QuestionCount,
    QuestionsResponse,
)


class QuestionsCollector:
    def __init__(self):
        self._client = WBApiClient(base_url=settings.WB_FEEDBACKS_URL, token=settings.WB_API_TOKEN)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._client.__aexit__(*args)

    async def get_count_unanswered(self) -> QuestionCountUnanswered:
        data = await self._client.get("/api/v1/questions/count-unanswered")
        return QuestionCountUnanswered.model_validate(data if isinstance(data, dict) else {})

    async def get_count(self, has_answer: bool | None = None) -> QuestionCount:
        params: dict = {}
        if has_answer is not None:
            params["hasAnswer"] = str(has_answer).lower()
        data = await self._client.get("/api/v1/questions/count", params=params)
        return QuestionCount.model_validate(data if isinstance(data, dict) else {})

    async def get_list(
        self,
        is_answered: bool = False,
        nm_id: int | None = None,
        limit: int = 10,
        offset: int = 0,
        order: str = "dateDesc",
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> QuestionsResponse:
        params: dict = {"isAnswered": str(is_answered).lower(), "take": limit, "skip": offset, "order": order}
        if nm_id: params["nmId"] = nm_id
        if date_from: params["dateFrom"] = date_from
        if date_to: params["dateTo"] = date_to
        data = await self._client.get("/api/v1/questions", params=params)
        return QuestionsResponse.model_validate(data if isinstance(data, dict) else {})

    async def answer_question(self, payload: dict) -> dict:
        return await self._client.patch("/api/v1/questions", json=payload)

    async def get_question(self, question_id: str) -> dict:
        return await self._client.get("/api/v1/question", params={"id": question_id})
