from fastapi import APIRouter, Depends, Request, HTTPException
from uuid import UUID
from typing import Annotated

from src.cart.schemas import CartResponse, CartItemResponse
from src.cart.service import CartService
from src.core.dependencies import get_cart_service
from src.cart.schemas import AddItemInput, UpdateItemInput
from src.core.utils import get_or_create_session_id

router = APIRouter(prefix="/api/cart", tags=["Cart"])


@router.get("/", response_model=CartResponse)
async def get_cart(
    session_id: Annotated[str, Depends(get_or_create_session_id)],
    cart_service: Annotated[CartService, Depends(get_cart_service)],
):
    try:
        return await cart_service.get_cart(session_id)
    except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=CartItemResponse)
async def add_to_cart(
    data: AddItemInput,
    session_id: Annotated[str, Depends(get_or_create_session_id)],
    cart_service: Annotated[CartService, Depends(get_cart_service)],
):
    try:
        return await cart_service.add_item(session_id, data.product_id, data.quantity)
    except Exception as e:
        return {"detail": str(e)}

@router.put("/{item_id}/", response_model=CartItemResponse)
async def update_cart_item(
    item_id: UUID,
    data: UpdateItemInput,
    session_id: Annotated[str, Depends(get_or_create_session_id)],
    cart_service: Annotated[CartService, Depends(get_cart_service)],
):
    try:
        return await cart_service.update_item(session_id, item_id, data.quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/{item_id}/")
async def delete_cart_item(
    item_id: UUID,
    session_id: Annotated[str, Depends(get_or_create_session_id)],
    cart_service: Annotated[CartService, Depends(get_cart_service)],
):
    try:
        await cart_service.remove_item(session_id, item_id)
        return {"detail": "Item removed"}
    except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

