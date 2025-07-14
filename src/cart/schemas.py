from typing import  Any, Optional, List
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, model_validator, Field
from src.core.schemas import ProductModel
from enum import Enum 


class CartItemResponse(BaseModel):
    id: UUID
    product: ProductModel
    quantity: int
    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total_price: Decimal

    class Config:
        from_attributes = True

class AddItemInput(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)

    class Config:
        from_attributes = True

class UpdateItemInput(BaseModel):
    quantity: int

    @model_validator(mode="after")
    def check_quantity(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        return self