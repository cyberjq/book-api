import typing
from pydantic import BaseModel

from app.models.db_model import publishing_house


class PublishingHouse(BaseModel):
    pub_house_id: typing.Optional[int]
    name: typing.Optional[str]
    address: typing.Optional[str]
    phone: typing.Optional[str]
    mail: typing.Optional[str]
    site: typing.Optional[str]

    class Config:
        orm_mode = True
        orm_model = publishing_house.PublishingHouse