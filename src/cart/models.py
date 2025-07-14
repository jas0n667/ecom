from src.core.base import Base
from uuid import uuid4
from sqlalchemy import Column, String, Text, Numeric, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Cart(Base):
    __tablename__ = "carts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(String, unique=True, nullable=False)

    # one‑to‑many: Cart → CartItem[]
    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.id", ondelete="CASCADE"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False)

    # связи назад
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items", lazy="selectin")