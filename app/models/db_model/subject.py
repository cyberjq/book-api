from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from app.database.base_class import Base
from app.models.db_model.subject_book import SubjectBook


class Subject(Base):
    __tablename__ = "subject"

    subject_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)

    books = relationship("Book", secondary=SubjectBook.__table__,
                         back_populates="subjects", cascade_backrefs=False)
