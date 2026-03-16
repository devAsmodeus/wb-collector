"""Схемы: Работа с товарами — Категории, предметы, характеристики."""
from typing import Any
from pydantic import BaseModel


class WBResponse(BaseModel):
    error: bool = False
    errorText: str = ""
    additionalErrors: Any = None


class ParentCategory(BaseModel):
    id: int | None = None
    name: str | None = None


class ParentCategoriesResponse(WBResponse):
    data: list[ParentCategory] | Any = None


class Subject(BaseModel):
    subjectID: int
    parentID: int
    subjectName: str
    parentName: str


class SubjectsResponse(WBResponse):
    data: list[Subject] = []


class SubjectCharc(BaseModel):
    charcID: int
    subjectName: str
    subjectID: int
    name: str
    required: bool = False
    unitName: str = ""
    maxCount: int = 0
    popular: bool = False
    charcType: int = 1


class SubjectCharcsResponse(WBResponse):
    data: list[SubjectCharc] = []


class TnvedCode(BaseModel):
    tnved: str
    isKiz: bool = False


class TnvedResponse(WBResponse):
    data: list[TnvedCode] = []


class Brand(BaseModel):
    id: int
    name: str
    logoUrl: str | None = None


class BrandsResponse(BaseModel):
    brands: list[Brand] = []
    next: int | None = None
    total: int = 0
