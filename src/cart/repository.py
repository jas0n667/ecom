from src.core.repository import PostgresRepository
from src.cart.models import Cart, CartItem
from src.product.schemas import ProductResponse
from src.core.db import async_session_maker

from sqlalchemy import insert, select, func, asc, desc, delete
from sqlalchemy.orm import selectinload
from typing import Optional
from uuid import UUID

class CartRepository(PostgresRepository):
    model = Cart

    async def get_by_session(self, session_id: str) -> Optional[Cart]:
        async with async_session_maker() as session:
            stmt = (
                select(self.model)
                .where(self.model.session_id == session_id)
                .options(
                    selectinload(Cart.items).selectinload(CartItem.product)  # загружаем всё сразу
                )
            )
            res = await session.execute(stmt)
            return res.scalar_one_or_none()
        

class CartItemRepository(PostgresRepository):
    model = CartItem

    async def get_item(self, cart_id: UUID, item_id: UUID) -> Optional[CartItem]:
        async with async_session_maker() as session:
            stmt = select(self.model).where(
                self.model.id == item_id,
                self.model.cart_id == cart_id
            ).options(selectinload(CartItem.product))
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def get_item_by_product(self, cart_id: UUID, product_id: UUID) -> Optional[CartItem]:
        async with async_session_maker() as session:
            stmt = select(self.model).where(
                self.model.cart_id == cart_id,
                self.model.product_id == product_id
            ).options(selectinload(CartItem.product))
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def update_item(self, item: CartItem) -> None:
        async with async_session_maker() as session:
            await session.merge(item)
            await session.commit()

    async def delete_item(self, item_id: UUID) -> None:
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.id == item_id)
            await session.execute(stmt)
            await session.commit()
