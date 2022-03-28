from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class PublishingHouse(Base):
    __tablename__ = "publishing_house"

    pub_house_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    mail = Column(String)
    site = Column(String)

    books = relationship("Book", back_populates="publishing_house", cascade_backrefs=False)
