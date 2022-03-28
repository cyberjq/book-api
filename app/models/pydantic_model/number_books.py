import typing
from pydantic import BaseModel

from app.models.db_model import number_books


class NumberBooks(BaseModel):

    book_id: typing.Optional[int]
    wh_id: typing.Optional[int]
    quantity: typing.Optional[int]

    class Config:
        orm_mode = True
        orm_model = number_books.NumberBooks