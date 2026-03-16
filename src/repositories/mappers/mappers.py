from src.repositories.mappers.base import DataMapper
from src.models.seller import SellerOrm
from src.schemas.general.seller import SellerInfo


class SellerMapper(DataMapper):
    db_model = SellerOrm
    schema = SellerInfo
