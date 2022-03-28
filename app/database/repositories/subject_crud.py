import typing

from sqlalchemy import asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.db_model import subject as subject_model_db
from app.models.pydantic_model import subject as subject_model


class SubjectRepository:

    async def get(self, db: AsyncSession, subject_id: int) -> typing.Optional[subject_model_db.Subject]:
        result = await db.execute(select(subject_model_db.Subject)
                                  .filter(subject_model_db.Subject.subject_id == subject_id))
        return result.scalars().first()

    async def gets(self, db: AsyncSession, skip: int = 0, limit: int = 100) \
            -> typing.Optional[typing.List[subject_model_db.Subject]]:
        results = await db.execute(select(subject_model_db.Subject).offset(skip).limit(limit)
                                   .order_by(asc(subject_model_db.Subject.subject_id)))
        return results.scalars().all()

    async def create(self, db: AsyncSession, subject: subject_model.Subject) -> subject_model_db.Subject:
        db_subject = subject_model_db.Subject(**subject.dict())
        db.add(db_subject)
        await db.commit()
        await db.refresh(db_subject)
        return db_subject

    async def update(self, db: AsyncSession, subject: subject_model.Subject) -> subject_model_db.Subject:
        db_subject = await self.get(db, subject.subject_id)

        if not db_subject:
            return db_subject

        db_subject.name = subject.name

        db.add(db_subject)
        await db.commit()
        await db.refresh(db_subject)
        return db_subject

    async def delete(self, db: AsyncSession, subject: subject_model.Subject):
        db_subject = await self.get(db, subject.subject_id)
        await db.delete(db_subject)
        await db.commit()