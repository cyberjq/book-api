from sqlalchemy import Column, ForeignKey, BigInteger, Integer
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class NumberBooks(Base):
    __tablename__ = "number_books"

    id = Column(BigInteger, primary_key=True, index=True)
    book_id = Column(BigInteger, ForeignKey("book.book_id"))
    wh_id = Column(BigInteger, ForeignKey("warehouses.warehouses_id"))
    quantity = Column(Integer, nullable=False, default=0)

    # warehouse = relationship("Warehouse", backref="number_books")
    # book = relationship("Book", back_populates="warehouses")
