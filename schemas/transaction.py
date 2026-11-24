from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    product_id: int = Field(gt=0)
    type: str = Field(max_length=50)
    amount: int = Field(gt=0)


class TransactionRead(BaseModel):
    id: int
    product_id: int
    date: datetime
    type: str
    amount: int

    model_config = ConfigDict(from_attributes=True)


class TransactionUpdate(BaseModel):
    product_id: Optional[int] = Field(default=None, gt=0)
    type: Optional[str] = Field(default=None, max_length=50)
    amount: Optional[int] = Field(default=None, gt=0)
