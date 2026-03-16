"""Роутер: Работа с товарами — Категории, предметы, характеристики."""
from fastapi import APIRouter, Query
from src.services.products.directories import DirectoriesService

router = APIRouter()
svc = DirectoriesService()


@router.get("/directories/categories", summary="Родительские категории товаров")
async def get_parent_categories(locale: str = Query("ru")):
    return await svc.get_parent_categories(locale=locale)


@router.get("/directories/subjects", summary="Список предметов")
async def get_subjects(name: str | None = Query(None), limit: int = Query(1000, ge=1, le=1000)):
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
