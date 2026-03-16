from fastapi import APIRouter, Query
from src.schemas.products import GoodsListResponse, CardsListRequest, CardsListResponse
from src.services.products import ProductsService

router = APIRouter(prefix="/products", tags=["02 — Products"])
svc = ProductsService()


# ─── Цены и скидки ───────────────────────────────────────────────────────────

@router.get("/goods", response_model=GoodsListResponse, summary="Товары с ценами и скидками")
async def get_goods(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    return await svc.get_goods_prices(limit=limit, offset=offset)


@router.get("/goods/sizes", summary="Цены по размерам артикула")
async def get_goods_sizes(nm_id: int = Query(..., description="Артикул WB")):
    return await svc.get_goods_sizes(nm_id)


@router.get("/goods/quarantine", summary="Товары на карантине")
async def get_quarantine(limit: int = Query(100), offset: int = Query(0)):
    return await svc.get_quarantine(limit=limit, offset=offset)


@router.get("/prices/history", summary="История загрузок цен")
async def get_price_history(limit: int = Query(100), offset: int = Query(0)):
    return await svc.get_price_history(limit=limit, offset=offset)


@router.get("/prices/history/goods", summary="Товары конкретной загрузки цен")
async def get_price_history_goods(upload_id: int = Query(..., description="ID загрузки")):
    return await svc.get_price_history_goods(upload_id)


@router.get("/prices/buffer", summary="Задачи в буфере цен")
async def get_buffer_tasks(limit: int = Query(100), offset: int = Query(0)):
    return await svc.get_buffer_tasks(limit=limit, offset=offset)


@router.get("/prices/buffer/goods", summary="Товары задачи в буфере цен")
async def get_buffer_goods(upload_id: int = Query(...)):
    return await svc.get_buffer_goods(upload_id)


# ─── Карточки ────────────────────────────────────────────────────────────────

@router.post("/cards", response_model=CardsListResponse, summary="Список карточек товаров")
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


# ─── Справочники ─────────────────────────────────────────────────────────────

@router.get("/directories/categories", summary="Родительские категории товаров")
async def get_parent_categories(locale: str = Query("ru")):
    return await svc.get_parent_categories(locale=locale)


@router.get("/directories/subjects", summary="Список предметов")
async def get_subjects(
    name: str | None = Query(None),
    limit: int = Query(1000, ge=1, le=1000),
):
    return await svc.get_subjects(name=name, limit=limit)


@router.get("/directories/subjects/{subject_id}/charcs", summary="Характеристики предмета")
async def get_subject_charcs(subject_id: int):
    return await svc.get_subject_charcs(subject_id)


@router.get("/directories/subjects/{subject_id}/brands", summary="Бренды предмета")
async def get_brands(subject_id: int):
    return await svc.get_brands(subject_id)


@router.get("/directories/{kind}", summary="Справочник (colors|kinds|countries|seasons|vat)")
async def get_directory(kind: str):
    return await svc.get_directory(kind)


# ─── Ярлыки ──────────────────────────────────────────────────────────────────

@router.get("/tags", summary="Список ярлыков")
async def get_tags():
    return await svc.get_tags()


@router.post("/tags", summary="Создать ярлык")
async def create_tag(name: str, color: str):
    return await svc.create_tag(name=name, color=color)


# ─── Склады ──────────────────────────────────────────────────────────────────

@router.get("/warehouses/wb", summary="Офисы WB (пункты сдачи)")
async def get_wb_offices():
    return await svc.get_wb_offices()


@router.get("/warehouses", summary="Склады продавца")
async def get_seller_warehouses():
    return await svc.get_seller_warehouses()


@router.post("/warehouses/{warehouse_id}/stocks", summary="Остатки на складе")
async def get_stocks(warehouse_id: int, skus: list[str]):
    return await svc.get_stocks(warehouse_id=warehouse_id, skus=skus)
