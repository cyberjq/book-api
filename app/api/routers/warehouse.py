import typing
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import dependencies
from app.database.repositories.warehouse_crud import WarehouseRepository
from app.models.pydantic_model.warehouse import Warehouse

router = APIRouter()
warehouses_repository = WarehouseRepository()


@router.get("/api/warehouses/{warehouses_id}", response_model=Warehouse)
async def get_warehouse(warehouses_id: int, db: AsyncSession = Depends(dependencies.get_db)):
    db_warehouses = await warehouses_repository.get(db, warehouses_id)
    if db_warehouses is None:
        raise HTTPException(status_code=404, detail="WarehousesNotFound")
    return db_warehouses


@router.get("/api/warehouses/", response_model=typing.List[Warehouse])
async def get_warehouses(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(dependencies.get_db)):
    warehouses = await warehouses_repository.gets(db, skip, limit)
    return warehouses


@router.post("/api/warehouses/", response_model=Warehouse)
async def create_warehouse(warehouse: Warehouse, db: AsyncSession = Depends(dependencies.get_db)):
    db_warehouse = await warehouses_repository.create(db, warehouse)
    if not db_warehouse:
        raise HTTPException(status_code=400, detail="WarehouseNotCreated")

    return db_warehouse


@router.put("/api/warehouses/", response_model=Warehouse)
async def update_warehouse(warehouse: Warehouse, db: AsyncSession = Depends(dependencies.get_db)):
    db_warehouse = await warehouses_repository.update(db, warehouse)
    if not db_warehouse:
        raise HTTPException(status_code=400, detail="WarehouseNotUpdated")

    return db_warehouse


@router.delete("/api/warehouses/")
async def delete_warehouse(warehouse: Warehouse, db: AsyncSession = Depends(dependencies.get_db)):
    await warehouses_repository.delete(db, warehouse)