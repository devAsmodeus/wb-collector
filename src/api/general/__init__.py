from fastapi import APIRouter
from src.api.general.seller import router as seller_router
from src.api.general.news import router as news_router
from src.api.general.users import router as users_router

router = APIRouter(prefix="/general", tags=["01 — General"])
router.include_router(seller_router)
router.include_router(news_router)
router.include_router(users_router)
