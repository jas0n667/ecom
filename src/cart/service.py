from src.cart.schemas import CartItemResponse, CartResponse, AddItemInput
from src.cart.repository import CartRepository, CartItemRepository
from src.product.repository import ProductRepository
from typing import List
from uuid import UUID


# services/cart_service.py

from uuid import UUID
from typing import List
from src.cart.models import Cart





class CartService:
    def __init__(
        self,
        cart_repo: CartRepository,
        cart_item_repo: CartItemRepository,
        product_repo: ProductRepository,
    ):
        self.cart_repo = cart_repo
        self.cart_item_repo = cart_item_repo
        self.product_repo = product_repo

    async def _get_or_create_cart(self, session_id: str) -> Cart:
        cart = await self.cart_repo.get_by_session(session_id)
        if not cart:
            cart = await self.cart_repo.add_one({"session_id": session_id})
        return cart

    async def get_cart(self, session_id: str) -> CartResponse:
        cart = await self._get_or_create_cart(session_id)
        total = sum(item.quantity * item.product.price for item in cart.items)

        return CartResponse(
            items=[
                CartItemResponse(
                    id=item.id,
                    product=item.product.to_read_model(),
                    quantity=item.quantity,
                )
                for item in cart.items
            ],
            total_price=total,
        )

    async def add_item(self, session_id: str, product_id: UUID, quantity: int) -> CartItemResponse:
        cart = await self._get_or_create_cart(session_id)

        product = await self.product_repo.get_one(product_id)
        if not product:
            raise Exception("Product not found")

        item = await self.cart_item_repo.get_item_by_product(cart.id, product_id)
        if item:
            item.quantity += quantity
            await self.cart_item_repo.update_item(item)
        else:
            item = await self.cart_item_repo.add_one({
                "cart_id": cart.id,
                "product_id": product_id,
                "quantity": quantity,
            })

        return CartItemResponse(
            id=item.id,
            product=item.product.to_read_model(),
            quantity=item.quantity,
        )

    async def update_item(self, session_id: str, item_id: UUID, quantity: int) -> CartItemResponse:
        cart = await self._get_or_create_cart(session_id)

        item = await self.cart_item_repo.get_item(cart.id, item_id)
        if not item:
            raise Exception("Cart item not found")
        item.quantity = quantity
        await self.cart_item_repo.update_item(item)

        return CartItemResponse(
            id=item.id,
            product=item.product.to_read_model(),
            quantity=item.quantity,
        )

    async def remove_item(self, session_id: str, item_id: UUID) -> None:
        cart = await self._get_or_create_cart(session_id)
        item = await self.cart_item_repo.get_item(cart.id, item_id)
        if not item:
            raise Exception("Item not found")

        await self.cart_item_repo.delete_item(item.id)
