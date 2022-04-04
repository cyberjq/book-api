import typing
from pydantic import BaseModel

from app.models.db_model import book
from app.models.pydantic_model.author import Author
from app.models.pydantic_model.publishing_house import PublishingHouse
from app.models.pydantic_model.subject import Subject
from app.models.pydantic_model.warehouse import Warehouse


class Book(BaseModel):
    book_id: typing.Optional[int]
    name: typing.Optional[str]
    publishing_house_id: typing.Optional[int]
    printing_year: typing.Optional[int]
    isbn: typing.Optional[str]

    publishing_house: typing.Optional[PublishingHouse]
    subjects: typing.Optional[typing.List[Subject]] = []
    warehouses: typing.Optional[typing.List[Warehouse]] = []
    authors: typing.Optional[typing.List[Author]] = []

    class Config:
        orm_mode = True
        orm_model = book.Book
