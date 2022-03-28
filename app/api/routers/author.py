import typing
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import dependencies
from app.database.repositories.author_crud import AuthorRepository
from app.models.pydantic_model.author import Author

router = APIRouter()
author_repository = AuthorRepository()


@router.get("/api/authors/{author_id}", response_model=Author)
async def get_author(author_id: int, db: AsyncSession = Depends(dependencies.get_db)):
    db_author = await author_repository.get(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="AuthorNotFound")
    return db_author


@router.get("/api/authors/", response_model=typing.List[Author])
async def get_authors(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(dependencies.get_db)):
    authors = await author_repository.gets(db, skip, limit)
    return authors


@router.post("/api/authors/", response_model=Author)
async def create_author(author: Author, db: AsyncSession = Depends(dependencies.get_db)):
    db_author = await author_repository.create(db, author)
    if not db_author:
        raise HTTPException(status_code=400, detail="UserNotCreated")

    return db_author


@router.put("/api/authors/", response_model=Author)
async def update_author(author: Author, db: AsyncSession = Depends(dependencies.get_db)):
    db_author = await author_repository.update(db, author)
    if not db_author:
        raise HTTPException(status_code=400, detail="UserNotUpdated")

    return db_author


@router.delete("/api/authors/")
async def delete_author(author: Author, db: AsyncSession = Depends(dependencies.get_db)):
    await author_repository.delete(db, author)