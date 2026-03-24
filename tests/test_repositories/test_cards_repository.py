"""Test CardsRepository upsert and query logic."""
import pytest
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.products.cards import CardsRepository
from src.models.products import WbCard


@pytest.mark.anyio
async def test_upsert_many_inserts_new_cards(session: AsyncSession):
    """upsert_many should insert new cards."""
    from unittest.mock import MagicMock

    # Create mock card data matching ProductCard schema
    mock_card = MagicMock()
    mock_card.nmID = 12345
    mock_card.imtID = 67890
    mock_card.nmUUID = "test-uuid"
    mock_card.subjectID = 1
    mock_card.subjectName = "Футболки"
    mock_card.vendorCode = "TEST-001"
    mock_card.brand = "TestBrand"
    mock_card.title = "Test Product"
    mock_card.description = "Test description"
    mock_card.dimensions = None
    mock_card.sizes = []
    mock_card.characteristics = []
    mock_card.photos = []
    mock_card.tags = []
    mock_card.createdAt = "2026-01-01T00:00:00"
    mock_card.updatedAt = "2026-03-24T00:00:00"

    repo = CardsRepository(session)
    count = await repo.upsert_many([mock_card])

    assert count == 1


@pytest.mark.anyio
async def test_upsert_many_updates_existing_cards(session: AsyncSession):
    """upsert_many should update cards on conflict by nm_id."""
    from unittest.mock import MagicMock

    mock_card = MagicMock()
    mock_card.nmID = 99999
    mock_card.imtID = 11111
    mock_card.nmUUID = "uuid-1"
    mock_card.subjectID = 1
    mock_card.subjectName = "Футболки"
    mock_card.vendorCode = "UPD-001"
    mock_card.brand = "Brand1"
    mock_card.title = "Original Title"
    mock_card.description = "Desc"
    mock_card.dimensions = None
    mock_card.sizes = []
    mock_card.characteristics = []
    mock_card.photos = []
    mock_card.tags = []
    mock_card.createdAt = "2026-01-01T00:00:00"
    mock_card.updatedAt = "2026-03-24T00:00:00"

    repo = CardsRepository(session)
    await repo.upsert_many([mock_card])

    # Update title
    mock_card.title = "Updated Title"
    count = await repo.upsert_many([mock_card])
    assert count == 1


@pytest.mark.anyio
async def test_upsert_many_empty_list(session: AsyncSession):
    """upsert_many with empty list returns 0."""
    repo = CardsRepository(session)
    count = await repo.upsert_many([])
    assert count == 0
