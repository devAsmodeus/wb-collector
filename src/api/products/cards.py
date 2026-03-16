"""Роутер: Работа с товарами — Карточки товаров."""
from fastapi import APIRouter, Query
from src.schemas.products.cards import CardsListRequest
from src.services.products.cards import CardsService

router = APIRouter()
svc = CardsService()


@router.post("/cards", summary="Список карточек товаров")
async def get_cards(request: CardsListRequest | None = None, locale: str = Query("ru")):
    return await svc.get_cards(request=request, locale=locale)


@router.get("/cards/limits", summary="Лимиты карточек товаров")
async def get_cards_limits():
    return await svc.get_cards_limits()


@router.get("/cards/errors", summary="Карточки с ошибками создания")
async def get_cards_errors():
    return await svc.get_cards_errors()


@router.post("/cards/trash", summary="Карточки в корзине")
async def get_trash_cards(locale: str = Query("ru")):
    return await svc.get_trash_cards(locale=locale)


@router.post("/barcodes", summary="Генерация баркодов")
async def generate_barcodes(count: int = Query(..., ge=1, le=5000)):
    return await svc.generate_barcodes(count)
