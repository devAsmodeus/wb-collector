"""Роутер: Общее — АПИ новостей."""
from fastapi import APIRouter, Query
from src.schemas.general.news import NewsResponse
from src.services.general.news import NewsService

router = APIRouter()


@router.get("/news", response_model=NewsResponse, summary="Новости портала продавцов")
async def get_news(
    from_date: str | None = Query(None, description="Дата от (ISO 8601), напр. 2024-01-01"),
    from_id: int | None = Query(None, description="ID новости, начиная с которой выдать список"),
):
    return await NewsService().get_news(from_date=from_date, from_id=from_id)
