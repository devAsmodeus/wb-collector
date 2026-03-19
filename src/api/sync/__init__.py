"""Sync router — /sync/*"""
from litestar import Router
from src.api.sync.general import sync_general_router

sync_router = Router(
    path="/sync",
    route_handlers=[sync_general_router],
)
