import typing
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import dependencies
from app.database.repositories.book_crud import BookRepository
from app.models.pydantic_model.book import Book
from app.models.pydantic_model.filter_book import FilterBook

router = APIRouter()
book_repository = BookRepository()


@router.get("/api/books/{book_id}", response_model=Book)
async def get_book(book_id: int, db: AsyncSession = Depends(dependencies.get_db)):
    db_book = await book_repository.get(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="BookNotFound")
    return db_book


@router.get("/api/books/", response_model=typing.List[Book])
async def get_books(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(dependencies.get_db)):
    books = await book_repository.gets(db, skip, limit)
    return books


@router.post("/api/books/", response_model=Book)
async def create_book(book: Book, db: AsyncSession = Depends(dependencies.get_db)):
    db_book = await book_repository.create(db, book)
    if not db_book:
        raise HTTPException(status_code=400, detail="BookNotCreated")

    return db_book

@router.post("/api/books/filters", response_model=typing.List[Book])
async def create_book(filterBook: FilterBook, db: AsyncSession = Depends(dependencies.get_db)):
    books = await book_repository.gets(db, filter=filterBook)

    return books


@router.put("/api/books/", response_model=Book)
async def update_book(book: Book, db: AsyncSession = Depends(dependencies.get_db)):
    db_book = await book_repository.update(db, book)
    if not db_book:
        raise HTTPException(status_code=400, detail="BookNotUpdated")

    return db_book


@router.delete("/api/books/")
async def delete_book(book: Book, db: AsyncSession = Depends(dependencies.get_db)):
    await book_repository.delete(db, book)