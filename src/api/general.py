from fastapi import APIRouter

from src.schemas.seller import SellerInfo
from src.services.general import GeneralService
from src.utils.db_manager import DBManager

router = APIRouter(prefix="/general", tags=["General"])


@router.get("/ping")
async def ping():
    """Проверить подключение к WB API."""
    svc = GeneralService()
    return await svc.ping()


@router.post("/seller-info/sync", response_model=SellerInfo)
async def sync_seller_info():
    """Получить информацию о продавце из WB и сохранить в БД."""
    svc = GeneralService(db=DBManager())
    return await svc.sync_seller_info()


@router.get("/seller-info", response_model=SellerInfo)
async def get_seller_info():
    """Получить сохранённую информацию о продавце из БД."""
    async with DBManager() as db:
        return await db.seller.get_one()
