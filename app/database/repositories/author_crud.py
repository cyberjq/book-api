import typing

from sqlalchemy import asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.db_model import author as author_model_db
from app.models.pydantic_model import author as author_model


class AuthorRepository:

    async def get(self, db: AsyncSession, author_id: int) -> typing.Optional[author_model_db.Author]:
        result = await db.execute(select(author_model_db.Author).filter(author_model_db.Author.author_id == author_id))
        return result.scalars().first()

    async def gets(self, db: AsyncSession, skip: int = 0, limit: int = 100) \
            -> typing.Optional[typing.List[author_model_db.Author]]:

        results = await db.execute(select(author_model_db.Author).offset(skip).limit(limit)
                                   .order_by(asc(author_model_db.Author.author_id)))
        return results.scalars().all()

    async def create(self, db: AsyncSession, author: author_model.Author) -> author_model_db.Author:
        db_author = author_model_db.Author(**author.dict())
        db.add(db_author)
        await db.commit()
        await db.refresh(db_author)
        return db_author

    async def update(self, db: AsyncSession, author: author_model.Author) -> author_model_db.Author:

        db_author = await self.get(db, author.author_id)

        if not db_author:
            return db_author

        db_author.last_name = author.last_name
        db_author.first_name = author.first_name
        db_author.middle_name = author.middle_name
        db_author.nickname = author.nickname

        db.add(db_author)
        await db.commit()
        await db.refresh(db_author)
        return db_author

    async def delete(self, db: AsyncSession, author: author_model.Author):
        db_author = await self.get(db, author.author_id)
        await db.delete(db_author)
        await db.commit()
