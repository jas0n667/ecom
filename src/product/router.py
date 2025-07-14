from fastapi import APIRouter, Depends, Request, HTTPException
from typing import List, Annotated
from .schemas import ProductCreate,ProductResponse, ProductsResponse, ProductFilter
from src.core.schemas import PaginationModel
from src.product.service import ProductService
from src.core.dependencies import product_service
from src.core.utils import replace_query_params
from uuid import UUID


route = APIRouter(tags=["Products API"],prefix="/products")

@route.post("/", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    product_service: Annotated[ProductService, Depends(product_service)]
):
    product = await product_service.add_product(product=product_data)

    return product

@route.get("/", response_model=ProductsResponse)
async def get_products(
    request: Request,
    pagination: Annotated[PaginationModel, Depends(PaginationModel)],
    filter_params: Annotated[ProductFilter, Depends()],
    product_service: Annotated[ProductService, Depends(product_service)],
):
    try:
        base_url = str(request.url)

        # получаем продукты
        products, total_count = await product_service.get_all_products(
            offset=pagination.offset,
            limit=pagination.limit,
            filter = filter_params
        )

        # строим next ссылку
        next_url = (
            replace_query_params(base_url, offset=pagination.offset + pagination.limit, limit=pagination.limit)
            if pagination.offset + pagination.limit < total_count else None
        )

        # строим previous ссылку
        prev_offset = max(pagination.offset - pagination.limit, 0)

        previous_url = (
            replace_query_params(base_url, offset=prev_offset, limit=pagination.limit)
            if pagination.offset > 0 else None
        )

        return {
            "count": total_count,
            "next": next_url,
            "previous": previous_url,
            "results": products
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@route.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID,
    product_service: Annotated[ProductService, Depends(product_service)]
):
    try:
        product = await product_service.get_product(id= product_id)
        return product
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))