from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from app.database.base_class import Base
from app.models.db_model.author_book import AuthorBook


class Author(Base):
    __tablename__ = "author"

    author_id = Column(BigInteger, primary_key=True, index=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String)
    nickname = Column(String)

    books = relationship("Book", secondary=AuthorBook.__table__, back_populates="authors", cascade_backrefs=False)