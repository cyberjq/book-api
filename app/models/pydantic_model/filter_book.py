import typing
from pydantic import BaseModel


class FilterBook(BaseModel):
    name: typing.Optional[str]
    printing_year_start: typing.Optional[int]
    printing_year_end: typing.Optional[int]