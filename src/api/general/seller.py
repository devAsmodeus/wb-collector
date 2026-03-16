"""Роутер: Общее — Информация о продавце."""
from fastapi import APIRouter
from src.schemas.general.seller import SellerInfo
from src.services.general.seller import SellerService
from src.utils.db_manager import DBManager

router = APIRouter()


@router.get("/ping", summary="Проверить подключение к WB API")
async def ping():
    return await SellerService().ping()


@router.post("/seller-info/sync", response_model=SellerInfo, summary="Получить инфо о продавце из WB и сохранить в БД")
async def sync_seller_info():
    return await SellerService(db=DBManager()).sync_seller_info()


@router.get("/seller-info", response_model=SellerInfo, summary="Получить сохранённую инфо о продавце из БД")
async def get_seller_info():
    async with DBManager() as db:
        return await db.seller.get_one()
