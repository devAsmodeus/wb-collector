from fastapi import APIRouter
from src.api.products.directories import router as directories_router
from src.api.products.tags import router as tags_router
from src.api.products.cards import router as cards_router
from src.api.products.prices import router as prices_router
from src.api.products.warehouses import router as warehouses_router

router = APIRouter(prefix="/products", tags=["02 — Products"])
router.include_router(directories_router)
router.include_router(tags_router)
router.include_router(cards_router)
router.include_router(prices_router)
router.include_router(warehouses_router)
