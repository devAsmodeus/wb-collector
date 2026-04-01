"""Test that all ORM models are properly defined and importable."""
import pytest
from src.models import (
    SellerOrm,
    WbCard, WbPrice, WbTag, WbWarehouse, WbCategory, WbSubject,
    FbsOrder, DbwOrder, DbsOrder, PickupOrder,
    WbStock, WbOrderReport, WbSaleReport, WbFinancialReport,
    WbCampaign, WbCampaignStat, WbPromotion,
    WbFeedback, WbQuestion, WbClaim,
    WbNews,
    WbTariffCommission, WbTariffBox, WbTariffPallet, WbTariffSupply,
    WbSyncState,
)


def test_all_models_have_tablename():
    """All models must have __tablename__ defined."""
    models = [
        SellerOrm,
        WbCard, WbPrice, WbTag, WbWarehouse, WbCategory, WbSubject,
        FbsOrder, DbwOrder, DbsOrder, PickupOrder,
        WbStock, WbOrderReport, WbSaleReport, WbFinancialReport,
        WbCampaign, WbCampaignStat, WbPromotion,
        WbFeedback, WbQuestion, WbClaim,
        WbNews,
        WbTariffCommission, WbTariffBox, WbTariffPallet, WbTariffSupply,
        WbSyncState,
    ]
    for model in models:
        assert hasattr(model, "__tablename__"), f"{model.__name__} missing __tablename__"
        assert model.__tablename__, f"{model.__name__} has empty __tablename__"


def test_model_count():
    """We should have 26 models total."""
    from src.models import __all__
    assert len(__all__) >= 22, f"Expected 22+ models, got {len(__all__)}"
