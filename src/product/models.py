from uuid import uuid4
from sqlalchemy import Column, String, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column,relationship
# from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID

from src.core.base import Base
from src.product.schemas import ProductResponse

class Product(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True)

    cart_items = relationship("CartItem", back_populates="product")

    def to_read_model(self) -> ProductResponse:
        return ProductResponse(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            image=self.image,
            category=self.category,
        )