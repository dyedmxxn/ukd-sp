from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    category_id: int = Field(gt=0)
    item_number: str = Field(max_length=50)
    name: str = Field(max_length=150)
    price: Decimal = Field(gt=0)
    measurement_units: str = Field(max_length=50)


class ProductRead(BaseModel):
    id: int
    category_id: int
    item_number: str
    name: str
    price: Decimal
    measurement_units: str

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    category_id: Optional[int] = Field(default=None, gt=0)
    item_number: Optional[str] = Field(default=None, max_length=50)
    name: Optional[str] = Field(default=None, max_length=150)
    price: Optional[Decimal] = Field(default=None, gt=0)
    measurement_units: Optional[str] = Field(default=None, max_length=50)
