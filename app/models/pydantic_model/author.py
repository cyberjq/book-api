import typing
from pydantic import BaseModel
from app.models.db_model import author


class Author(BaseModel):
    author_id: typing.Optional[int]
    last_name: typing.Optional[str]
    first_name: typing.Optional[str]
    middle_name: typing.Optional[str]
    nickname: typing.Optional[str]

    class Config:
        orm_mode = True
        orm_model = author.Author
