from sqlalchemy import Column, ForeignKey, BigInteger
from app.database.base_class import Base


class AuthorBook(Base):
    __tablename__ = "author_book"

    id = Column(BigInteger, primary_key=True, index=True)
    book_id = Column(BigInteger, ForeignKey("book.book_id"))
    author_id = Column(BigInteger, ForeignKey("author.author_id"))
