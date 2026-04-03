"""
Контроллер: Products / Склады и остатки
WB API: marketplace-api.wildberries.ru
"""
from litestar import Controller, get, post, put
from litestar.handlers import delete
from litestar.params import Parameter

from src.schemas.products.warehouses import (
    SellerWarehousesResponse,
    StocksRequest,
    StocksResponse,
    WBOfficesResponse,
)
from src.services.products.wb.warehouses import WarehousesService


class WBOfficesController(Controller):
    path = "/offices"
    tags = ["02. API Wildberries"]

    @get("/", summary="Склады WB (офисы приёмки)",
         description="GET /api/v3/offices — пункты сдачи товара на WB.")
    async def get_wb_offices(self) -> WBOfficesResponse:
        return await WarehousesService().get_wb_offices()


class SellerWarehousesController(Controller):
    path = "/warehouses"
    tags = ["02. API Wildberries"]

    @get("/", summary="Склады продавца",
         description="GET /api/v3/warehouses")
    async def get_seller_warehouses(self) -> SellerWarehousesResponse:
        return await WarehousesService().get_seller_warehouses()

    @post("/", summary="Создать склад продавца ⚠️",
          description="POST /api/v3/warehouses — **изменяет реальные данные**.")
    async def create_seller_warehouse(self, data: dict) -> dict:
        return await WarehousesService().create_seller_warehouse(
            name=data.get("name", ""),
            office_id=data.get("officeId", 0),
        )

    @put("/{warehouse_id:int}", summary="Обновить склад продавца ⚠️",
         description="PUT /api/v3/warehouses/{warehouseId}")
    async def update_seller_warehouse(self, warehouse_id: int, data: dict) -> dict:
        return await WarehousesService().update_seller_warehouse(warehouse_id, data)

    @delete("/{warehouse_id:int}", summary="Удалить склад продавца ⚠️",
            description="DELETE /api/v3/warehouses/{warehouseId}", status_code=200)
    async def delete_seller_warehouse(self, warehouse_id: int) -> dict:
        return await WarehousesService().delete_seller_warehouse(warehouse_id)

    @post("/{warehouse_id:int}/stocks", summary="Остатки на складе",
          description="POST /api/v3/stocks/{warehouseId}")
    async def get_stocks(self, data: StocksRequest, warehouse_id: int) -> StocksResponse:
        return await WarehousesService().get_stocks(warehouse_id=warehouse_id, skus=data.skus)

    @put("/{warehouse_id:int}/stocks", summary="Обновить остатки на складе ⚠️",
         description="PUT /api/v3/stocks/{warehouseId}")
    async def update_stocks(self, data: dict, warehouse_id: int) -> dict:
        return await WarehousesService().update_stocks(warehouse_id, data.get("stocks", []))

    @delete("/{warehouse_id:int}/stocks", summary="Удалить остатки на складе ⚠️",
            description="DELETE /api/v3/stocks/{warehouseId}", status_code=200)
    async def delete_stocks(self, data: dict, warehouse_id: int) -> dict:
        return await WarehousesService().delete_stocks(warehouse_id, data.get("skus", []))
