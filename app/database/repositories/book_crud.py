import typing

from sqlalchemy import asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.db_model import author as author_model_db
from app.models.db_model import book as book_model_db
from app.models.db_model import number_books as number_books_model_db
from app.models.db_model import author_book as author_book_model_db
from app.models.db_model import subject_book as subject_book_model_db
from app.models.db_model import publishing_house as publishing_house_model_db
from app.models.db_model import subject as subject_model_db
from app.models.db_model import warehouse as warehouse_model_db
from app.models.pydantic_model import book as book_model
from app.models.pydantic_model.book import Book
from app.models.pydantic_model.filter_book import FilterBook


class BookRepository:

    async def get(self, db: AsyncSession, book_id: int) -> typing.Optional[book_model_db.Book]:
        result = await db.execute(select(book_model_db.Book).filter(book_model_db.Book.book_id == book_id))
        return result.scalars().first()

    async def gets(self, db: AsyncSession, skip: int = 0, limit: int = 100, filter: FilterBook = None) \
            -> typing.Optional[typing.List[book_model_db.Book]]:
        if not filter:
            s = select(book_model_db.Book).offset(skip).limit(limit)
        else:
            s = select(book_model_db.Book)

            if filter.name:
                s = s.where(book_model_db.Book.name.like(f'%{filter.name.lower()}%'))

            if filter.printing_year_start:
                s = s.where(book_model_db.Book.printing_year >= filter.printing_year_start)

            if filter.printing_year_end:
                s = s.where(book_model_db.Book.printing_year <= filter.printing_year_end)

        return (await db.execute(s.order_by(asc(book_model_db.Book.book_id)))).scalars().all()

    async def create(self, db: AsyncSession, book: book_model.Book) -> Book:

        subjects = [subject_model_db.Subject(**subject.dict()) for subject in book.subjects]
        authors = [author_model_db.Author(**author.dict()) for author in book.authors]
        publishing_house = publishing_house_model_db.PublishingHouse(**book.publishing_house.dict())
        warehouses = [warehouse_model_db.Warehouse(
            warehouses_id=warehouse.warehouses_id,
            name=warehouse.name,
            address=warehouse.address,
            phone=warehouse.phone,
            site=warehouse.site,
        ) for warehouse in book.warehouses]

        db_book = book_model_db.Book(
            name=book.name,
            isbn=book.isbn,
            printing_year=book.printing_year,
            publishing_house_id=book.publishing_house_id,
            publishing_house=publishing_house,
            warehouses=warehouses,
            authors=authors,
            subjects=subjects
        )

        new_book_db = await db.merge(db_book)
        await db.flush()

        new_book_numbers = [await db.merge(number_books_model_db.NumberBooks(
            book_id=new_book_db.book_id,
            wh_id=warehouse.warehouses_id,
            quantity=warehouse.quantity,
        )) for warehouse in book.warehouses]

        await db.flush()
        await db.commit()

        new_book_db = Book.from_orm(new_book_db)

        for book_number, warehouse in zip(new_book_numbers, new_book_db.warehouses):
            warehouse.quantity = book_number.quantity

        return new_book_db

    async def update(self, db: AsyncSession, book: book_model.Book) -> book_model_db.Book:
        db_book = await self.get(db, book.book_id)

        if not db_book:
            return db_book

        db_book.name = book.name
        db_book.isbn = book.isbn
        db_book.printing_year = book.printing_year
        db_book.publishing_houser_id = book.publishing_house_id

        # subject_book = [subject_model_db.SubjectBook(book_id=db_book.book_id,
        #                                              subject_id=subject.subject_id)
        #                 for subject in book.subjects]
        #
        # author_book = [author_book_model_db.AuthorBook(book_id=db_book.book_id,
        #                                                author_id=author.author_id)
        #                for author in book.authors]
        # number_books = [number_books_model_db.NumberBooks(book_id=db_book.book_id)]

        db_book.subjects = [subject_model_db.Subject(**subject.dict()) for subject in book.subjects]
        db_book.warehouses = [warehouse_model_db.Warehouse(**warehouse.dict()) for warehouse in book.warehouses]
        db_book.authors = [author_model_db.Author(**author.dict()) for author in book.authors]
        # await db.flush()

        await db.commit()
        return db_book

    async def delete(self, db: AsyncSession, book: book_model.Book):
        db_book = await self.get(db, book.book_id)
        await db.delete(db_book)
        await db.commit()
