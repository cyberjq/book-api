import typing
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import dependencies
from app.database.repositories.publishing_house_crud import PublishingHouseRepository
from app.models.pydantic_model.publishing_house import PublishingHouse

router = APIRouter()
publishing_house_repository = PublishingHouseRepository()


@router.get("/api/publishing_houses/{pub_house_id}", response_model=PublishingHouse)
async def get_publishing_house(pub_house_id: int, db: AsyncSession = Depends(dependencies.get_db)):
    db_publishing_house = await publishing_house_repository.get(db, pub_house_id)
    if db_publishing_house is None:
        raise HTTPException(status_code=404, detail="PublishingHouseNotFound")
    return db_publishing_house


@router.get("/api/publishing_houses/", response_model=typing.List[PublishingHouse])
async def get_publishing_houses(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(dependencies.get_db)):
    publishing_houses = await publishing_house_repository.gets(db, skip, limit)
    return publishing_houses


@router.post("/api/publishing_houses/", response_model=PublishingHouse)
async def create_publishing_house(publishing_house: PublishingHouse, db: AsyncSession = Depends(dependencies.get_db)):
    db_publishing_house = await publishing_house_repository.create(db, publishing_house)
    if not db_publishing_house:
        raise HTTPException(status_code=400, detail="PublishingHouseNotCreated")

    return db_publishing_house


@router.put("/api/publishing_houses/", response_model=PublishingHouse)
async def update_publishing_house(publishing_house: PublishingHouse, db: AsyncSession = Depends(dependencies.get_db)):
    db_publishing_house = await publishing_house_repository.update(db, publishing_house)
    if not db_publishing_house:
        raise HTTPException(status_code=400, detail="PublishingHouseNotUpdated")

    return db_publishing_house


@router.delete("/api/publishing_houses/")
async def delete_publishing_house(publishing_house: PublishingHouse, db: AsyncSession = Depends(dependencies.get_db)):
    await publishing_house_repository.delete(db, publishing_house)