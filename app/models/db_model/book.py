from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from app.database.base_class import Base
from app.models.db_model.author_book import AuthorBook
from app.models.db_model.number_books import NumberBooks
from app.models.db_model.subject_book import SubjectBook


class Book(Base):
    __tablename__ = "book"

    book_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    publishing_house_id = Column(BigInteger, ForeignKey("publishing_house.pub_house_id"))
    printing_year = Column(Integer)
    isbn = Column(String, nullable=False)

    publishing_house = relationship("PublishingHouse", back_populates="books", cascade_backrefs=False, lazy="selectin",)
    subjects = relationship("Subject", secondary=SubjectBook.__table__, lazy="selectin",
                            back_populates="books", cascade_backrefs=False)
    warehouses = relationship("Warehouse", secondary=NumberBooks.__table__, lazy="selectin",
                              back_populates="books", cascade_backrefs=False)
    authors = relationship("Author", secondary=AuthorBook.__table__, lazy="selectin",
                           back_populates="books", cascade_backrefs=False)
