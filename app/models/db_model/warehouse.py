from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from app.database.base_class import Base
from app.models.db_model.number_books import NumberBooks


class Warehouse(Base):
    __tablename__ = "warehouses"

    warehouses_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    site = Column(String)

    books = relationship("Book", secondary=NumberBooks.__table__,
                         back_populates="warehouses", cascade_backrefs=False)
