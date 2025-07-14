import asyncio
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from src.product.router import route as product_router
from src.cart.router import router as cart_router
from src.core.db import init_db, Base

from src.product.models import Product

app = FastAPI(prefix="/api")
app.include_router(product_router)
app.include_router(cart_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Разрешённые источники
    allow_credentials=True,
    allow_methods=["*"],              # Разрешённые методы: GET, POST и т.п.
    allow_headers=["*"],              # Разрешённые заголовки
)

@app.on_event("startup")
async def startup_event():
    await init_db()