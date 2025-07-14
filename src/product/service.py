from src.core.repository import PostgresRepository
from src.product.repository import ProductRepository
from uuid import UUID

class ProductService():
    def __init__(self, product_repo: PostgresRepository):
        self.product_repo: ProductRepository = product_repo()

    async def add_product(self, product: PostgresRepository):
        product_dict = product.model_dump()
        product_db = await self.product_repo.add_one(product_dict)
        return product_db

    async def get_product(self, id: UUID):
        product = await self.product_repo.get_one(id=id)
        if not product:
            raise Exception(f"Product with id {id} not found")
        return product
    
    async def get_all_products(self, limit: int, offset:int,filter:dict):
        filters = filter.model_dump()
        if filters["min_price"] and filters["max_price"] and filters["max_price"] < filters["min_price"]:
            raise Exception(f"Min price can not be bigger than max_price")
        products = await self.product_repo.get_all_with_query(limit = limit, offset=offset,filter=filters)
        return products