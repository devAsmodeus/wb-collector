"""Test FbsOrdersRepository."""
import pytest
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.fbs.orders import FbsOrdersRepository


@pytest.mark.anyio
async def test_upsert_many_inserts_orders(session: AsyncSession):
    """upsert_many should insert new FBS orders."""
    orders = [
        {
            "orderId": 100001,
            "orderUID": "uid-001",
            "rid": "rid-001",
            "date": "2026-03-24T10:00:00",
            "lastChangeDate": "2026-03-24T10:00:00",
            "warehouseName": "Москва",
            "countryName": "Россия",
            "oblastOkrugName": "ЦФО",
            "regionName": "Москва",
            "article": "ART-001",
            "nmId": 12345,
            "chrtId": 67890,
            "subject": "Футболки",
            "category": "Одежда",
            "brand": "TestBrand",
            "name": "Test Item",
            "techSize": "M",
            "colorCode": "",
            "totalPrice": 1500.00,
            "discountPercent": 10,
            "spp": 5,
            "finishedPrice": 1350.00,
            "priceWithDisc": 1350.00,
            "isCancel": False,
            "cancelDate": None,
            "orderType": "fbs",
            "supplierStatus": "new",
            "wbStatus": "waiting",
            "skus": ["SKU001"],
            "isZeroOrder": False,
        }
    ]

    repo = FbsOrdersRepository(session)
    count = await repo.upsert_many(orders)
    assert count == 1


@pytest.mark.anyio
async def test_get_all_returns_orders(session: AsyncSession):
    """get_all should return inserted orders."""
    repo = FbsOrdersRepository(session)
    orders = await repo.get_all(limit=10)
    assert isinstance(orders, list)


@pytest.mark.anyio
async def test_upsert_many_empty(session: AsyncSession):
    """upsert_many with empty list returns 0."""
    repo = FbsOrdersRepository(session)
    count = await repo.upsert_many([])
    assert count == 0
