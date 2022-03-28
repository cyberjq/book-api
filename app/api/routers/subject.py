import typing
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import dependencies
from app.database.repositories.subject_crud import SubjectRepository
from app.models.pydantic_model.subject import Subject

router = APIRouter()
subject_repository = SubjectRepository()


@router.get("/api/subjects/{subject_id}", response_model=Subject)
async def get_subject(subject_id: int, db: AsyncSession = Depends(dependencies.get_db)):
    db_subject = await subject_repository.get(db, subject_id)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="SubjectNotFound")
    return db_subject


@router.get("/api/subjects/", response_model=typing.List[Subject])
async def get_subjects(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(dependencies.get_db)):
    subjects = await subject_repository.gets(db, skip, limit)
    return subjects


@router.post("/api/subjects/", response_model=Subject)
async def create_subject(subject: Subject, db: AsyncSession = Depends(dependencies.get_db)):
    db_subject = await subject_repository.create(db, subject)
    if not db_subject:
        raise HTTPException(status_code=400, detail="SubjectNotCreated")

    return db_subject


@router.put("/api/subjects/", response_model=Subject)
async def update_subject(subject: Subject, db: AsyncSession = Depends(dependencies.get_db)):
    db_subject = await subject_repository.update(db, subject)
    if not db_subject:
        raise HTTPException(status_code=400, detail="SubjectNotUpdated")

    return db_subject


@router.delete("/api/subjects/")
async def delete_subject(subject: Subject, db: AsyncSession = Depends(dependencies.get_db)):
    await subject_repository.delete(db, subject)