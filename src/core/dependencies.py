from src.product.repository import ProductRepository
from src.product.service import ProductService
from src.core.schemas import PaginationModel
from src.cart.service import CartService
from src.cart.repository import CartRepository
from src.cart.repository import CartItemRepository

def product_service():
    return ProductService(ProductRepository)

def get_cart_service() -> CartService:
    return CartService(
        cart_repo=CartRepository(),
        cart_item_repo=CartItemRepository(),
        product_repo=ProductRepository()
    )


