from fastapi import APIRouter

from app.api.v1.endpoints import auth, categories, products, carts, orders

api_router = APIRouter()

# Include routers for each resource
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(carts.router, prefix="/carts", tags=["carts"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
