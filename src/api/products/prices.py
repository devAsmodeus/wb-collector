"""Роутер: Работа с товарами — Цены и скидки."""
from fastapi import APIRouter, Query
from src.schemas.products.prices import GoodsListResponse
from src.services.products.prices import PricesService

router = APIRouter()
svc = PricesService()


@router.get("/prices/goods", response_model=GoodsListResponse, summary="Товары с ценами и скидками")
async def get_goods(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    return await svc.get_goods(limit=limit, offset=offset)


@router.get("/prices/goods/sizes", summary="Цены по размерам артикула")
async def get_goods_sizes(nm_id: int = Query(...)):
    return await svc.get_goods_sizes(nm_id)


@router.get("/prices/goods/quarantine", summary="Товары на карантине")
async def get_quarantine(limit: int = Query(100), offset: int = Query(0)):
    return await svc.get_quarantine(limit=limit, offset=offset)


@router.get("/prices/history", summary="История загрузок цен")
async def get_upload_history(limit: int = Query(100), offset: int = Query(0)):
    return await svc.get_upload_history(limit=limit, offset=offset)


@router.get("/prices/history/goods", summary="Товары конкретной загрузки цен")
async def get_upload_goods(upload_id: int = Query(...)):
    return await svc.get_upload_goods(upload_id)


@router.get("/prices/buffer", summary="Задачи в буфере цен")
async def get_buffer_tasks(limit: int = Query(100), offset: int = Query(0)):
    return await svc.get_buffer_tasks(limit=limit, offset=offset)


@router.get("/prices/buffer/goods", summary="Товары задачи в буфере цен")
async def get_buffer_goods(upload_id: int = Query(...)):
    return await svc.get_buffer_goods(upload_id)
