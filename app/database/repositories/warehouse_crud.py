import typing

from sqlalchemy import asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.db_model import warehouse as warehouse_model_db
from app.models.pydantic_model import warehouse as warehouse_model


class WarehouseRepository:

    async def get(self, db: AsyncSession, warehouses_id: int) -> typing.Optional[warehouse_model_db.Warehouse]:
        result = await db.execute(select(warehouse_model_db.Warehouse)
                                  .filter(warehouse_model_db.Warehouse.warehouses_id == warehouses_id))
        return result.scalars().first()

    async def gets(self, db: AsyncSession, skip: int = 0, limit: int = 100) \
            -> typing.Optional[typing.List[warehouse_model_db.Warehouse]]:

        results = await db.execute(select(warehouse_model_db.Warehouse).offset(skip).limit(limit)
                                   .order_by(asc(warehouse_model_db.Warehouse.warehouses_id)))
        return results.scalars().all()

    async def create(self, db: AsyncSession, warehouses: warehouse_model.Warehouse) -> warehouse_model_db.Warehouse:
        db_warehouses = warehouse_model_db.Warehouse(**warehouses.dict())
        db.add(db_warehouses)
        await db.commit()
        await db.refresh(db_warehouses)
        return db_warehouses

    async def update(self, db: AsyncSession, warehouses: warehouse_model.Warehouse) -> warehouse_model_db.Warehouse:
        db_warehouses = await self.get(db, warehouses.warehouses_id)

        if not db_warehouses:
            return db_warehouses

        db_warehouses.name = warehouses.name
        db_warehouses.site = warehouses.site
        db_warehouses.address = warehouses.address
        db_warehouses.phone = warehouses.phone

        db.add(db_warehouses)
        await db.commit()
        await db.refresh(db_warehouses)
        return db_warehouses

    async def delete(self, db: AsyncSession, warehouses: warehouse_model.Warehouse):
        db_warehouses = await self.get(db, warehouses.warehouses_id)
        await db.delete(db_warehouses)
        await db.commit()