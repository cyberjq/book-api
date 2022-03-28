import typing
from pydantic import BaseModel

from app.models.db_model import warehouse


class Warehouse(BaseModel):
    warehouses_id: typing.Optional[int]
    name: typing.Optional[str]
    address: typing.Optional[str]
    phone: typing.Optional[str]
    site: typing.Optional[str]
    quantity: typing.Optional[int]

    class Config:
        orm_mode = True
        orm_model = warehouse.Warehouse