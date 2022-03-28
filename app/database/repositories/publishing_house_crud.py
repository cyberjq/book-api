import typing

from sqlalchemy import asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.db_model import publishing_house as publishing_house_model_db
from app.models.pydantic_model import publishing_house as publishing_house_model


class PublishingHouseRepository:

    async def get(self, db: AsyncSession, ph_id: int) -> typing.Optional[publishing_house_model_db.PublishingHouse]:
        result = await db.execute(select(publishing_house_model_db.PublishingHouse)
                                  .filter(publishing_house_model_db.PublishingHouse.pub_house_id == ph_id))
        return result.scalars().first()

    async def gets(self, db: AsyncSession, skip: int = 0, limit: int = 100) \
            -> typing.Optional[typing.List[publishing_house_model_db.PublishingHouse]]:
        results = await db.execute(select(publishing_house_model_db.PublishingHouse).offset(skip).limit(limit)
                                   .order_by(asc(publishing_house_model_db.PublishingHouse.pub_house_id)))
        return results.scalars().all()

    async def create(self, db: AsyncSession, publishing_house: publishing_house_model.PublishingHouse) \
            -> publishing_house_model_db.PublishingHouse:

        db_publishing_house = publishing_house_model_db.PublishingHouse(**publishing_house.dict())
        db.add(db_publishing_house)
        await db.commit()
        await db.refresh(db_publishing_house)
        return db_publishing_house

    async def update(self, db: AsyncSession, publishing_house: publishing_house_model.PublishingHouse)\
            -> publishing_house_model_db.PublishingHouse:

        db_publishing_house = await self.get(db, publishing_house.pub_house_id)

        if not db_publishing_house:
            return db_publishing_house

        db_publishing_house.name = publishing_house.name
        db_publishing_house.site = publishing_house.site
        db_publishing_house.address = publishing_house.address
        db_publishing_house.main = publishing_house.mail
        db_publishing_house.phone = publishing_house.phone

        db.add(db_publishing_house)
        await db.commit()
        await db.refresh(db_publishing_house)
        return db_publishing_house

    async def delete(self, db: AsyncSession, publishing_house: publishing_house_model.PublishingHouse):
        db_publishing_house = await self.get(db, publishing_house.pub_house_id)
        await db.delete(db_publishing_house)
        await db.commit()