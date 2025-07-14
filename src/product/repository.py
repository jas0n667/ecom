from src.core.repository import PostgresRepository
from src.product.models import Product
from src.product.schemas import ProductResponse
from src.core.db import async_session_maker
from sqlalchemy import insert, select, func, asc, desc


class ProductRepository(PostgresRepository):
    model = Product

    async def get_all_with_query(self, limit:int, offset:int, filter: dict):
        async with async_session_maker() as session:
            stmt = select(self.model)

            # фильтр
            if filter["category"] is not None:
                stmt = stmt.where(self.model.category == filter["category"].value)
            if filter["min_price"] is not None:
                stmt = stmt.where(self.model.price >= filter["min_price"])
            if filter["max_price"] is not None:
                stmt = stmt.where(self.model.price <= filter["max_price"])
            if filter["q"]:
                keyword = f"%{filter['q'].lower()}%"
                stmt = stmt.where(
                    func.lower(self.model.name).ilike(keyword) |
                    func.lower(self.model.description).ilike(keyword)
                )

            sort_by = filter.get("sort_by")
            order = filter.get("order", "asc")

            if filter.get("sort_by"):
                column = getattr(self.model, sort_by.value)
                direction = desc if order == "desc" else asc
                stmt = stmt.order_by(direction(column))


            # Подсчёт количества записей  после фильтра
            total_stmt = select(func.count()).select_from(stmt.subquery())
            total = await session.execute(total_stmt)
            total_count = total.scalar_one()

            # пагинация
            stmt = stmt.offset(offset).limit(limit)

            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            
            return res, total_count

