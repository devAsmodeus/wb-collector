"""Роутер: Работа с товарами — Остатки и склады продавца."""
from fastapi import APIRouter
from src.services.products.warehouses import WarehousesService

router = APIRouter()
svc = WarehousesService()


@router.get("/warehouses/wb", summary="Офисы WB (пункты сдачи)")
async def get_wb_offices():
    return await svc.get_wb_offices()


@router.get("/warehouses", summary="Склады продавца")
async def get_seller_warehouses():
    return await svc.get_seller_warehouses()


@router.post("/warehouses/{warehouse_id}/stocks", summary="Остатки на складе")
async def get_stocks(warehouse_id: int, skus: list[str]):
    return await svc.get_stocks(warehouse_id=warehouse_id, skus=skus)
