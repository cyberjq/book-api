from sqlalchemy import Column, ForeignKey, BigInteger

from app.database.base_class import Base


class SubjectBook(Base):
    __tablename__ = "subject_book"

    id = Column(BigInteger, primary_key=True, index=True)
    book_id = Column(BigInteger, ForeignKey("book.book_id"))
    subject_id = Column(BigInteger, ForeignKey("subject.subject_id"))