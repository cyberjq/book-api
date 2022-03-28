import typing
from pydantic import BaseModel

from app.models.db_model import subject


class Subject(BaseModel):
    subject_id: typing.Optional[int]
    name: typing.Optional[str]

    class Config:
        orm_mode = True
        orm_model = subject.Subject