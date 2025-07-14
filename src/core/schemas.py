from pydantic import BaseModel, HttpUrl, UUID4, Field
from typing import Optional, List
from decimal import Decimal
from uuid import UUID


class ProductModel(BaseModel):
    name: str
    price: Decimal
    image: Optional[HttpUrl] = None
    category: Optional[str] = None

class PaginationModel(BaseModel):
    limit: int = Field(5, ge=0, le=100)
    offset: int = Field(0,ge=0)


