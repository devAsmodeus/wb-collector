"""WB API proxy router — /wb/*"""
from litestar import Router
from src.api.wb.general import wb_general_router

wb_router = Router(
    path="/wb",
    route_handlers=[wb_general_router],
)
