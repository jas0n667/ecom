from typing import  Any, Optional, List, Literal
from uuid import UUID
from pydantic import BaseModel, model_validator
from src.core.schemas import ProductModel
from enum import Enum 


class Category(Enum):
    electronics = "Электроника"
    clothing = "Одежда"
    appliances = "Бытовая техника"    


class SortBy(Enum):
    name = "name"
    price = "price"

class ProductCreate(ProductModel):
    pass

class ProductResponse(ProductModel):
    id: UUID
    description: Optional[str] = None

    class Config:
        from_attributes = True

class ProductsResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[ProductResponse]

        
    class Config:
        from_attributes = True


class ProductFilter(BaseModel):
    category: Optional[Category] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    q: Optional[str] = None
    sort_by: Optional[SortBy] = None
    order: Optional[Literal["asc", "desc"]] = "asc" # asc or decs


