from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db, get_current_admin
from app.models.user import User
from app.models.product import Product
from app.models.order import Order, OrderStatus
from app.schemas.product import ProductResponse
from app.schemas.order import OrderResponse


router = APIRouter()


@router.get("/dashboard/stats")
def get_dashboard_stats(
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_admin)
):
    """
    Obtiene estadísticas generales para el dashboard de administración

    **Requires admin role**

    Retorna:
    - Total de productos
    - Total de pedidos
    - Ventas totales (excluyendo pedidos cancelados)
    - Pedidos pendientes (pending + processing)
    - Productos sin stock
    - Productos con stock bajo (< 10 unidades)
    - Desglose de pedidos por estado
    - Últimos 5 pedidos
    - Top 10 productos con stock bajo
    """

    # Total de productos
    total_products = db.query(Product).count()

    # Total de pedidos
    total_orders = db.query(Order).count()

    # Productos sin stock
    out_of_stock_products = db.query(Product).filter(Product.stock == 0).count()

    # Productos con stock bajo (< 10)
    low_stock_products = db.query(Product).filter(
        Product.stock > 0,
        Product.stock < 10
    ).count()

    # Ventas totales (excluyendo cancelados)
    total_revenue = db.query(func.sum(Order.total_amount)).filter(
        Order.status != OrderStatus.CANCELLED
    ).scalar() or 0.0

    # Pedidos pendientes (pending + processing)
    pending_orders = db.query(Order).filter(
        Order.status.in_([OrderStatus.PENDING, OrderStatus.PROCESSING])
    ).count()

    # Pedidos por estado
    orders_by_status = {
        "pending": db.query(Order).filter(Order.status == OrderStatus.PENDING).count(),
        "confirmed": db.query(Order).filter(Order.status == OrderStatus.CONFIRMED).count(),
        "processing": db.query(Order).filter(Order.status == OrderStatus.PROCESSING).count(),
        "shipped": db.query(Order).filter(Order.status == OrderStatus.SHIPPED).count(),
        "delivered": db.query(Order).filter(Order.status == OrderStatus.DELIVERED).count(),
        "cancelled": db.query(Order).filter(Order.status == OrderStatus.CANCELLED).count(),
    }

    # Últimos 5 pedidos (ordenados por fecha de creación descendente)
    recent_orders_query = db.query(Order).order_by(Order.created_at.desc()).limit(5)
    recent_orders = [OrderResponse.model_validate(order) for order in recent_orders_query]

    # Top 10 productos con stock bajo
    low_stock_products_query = db.query(Product).filter(
        Product.stock < 10
    ).order_by(Product.stock.asc()).limit(10)
    low_stock_products_list = [ProductResponse.model_validate(product) for product in low_stock_products_query]

    return {
        "totalProducts": total_products,
        "totalOrders": total_orders,
        "totalRevenue": total_revenue,
        "pendingOrders": pending_orders,
        "outOfStockProducts": out_of_stock_products,
        "lowStockProducts": low_stock_products,
        "ordersByStatus": orders_by_status,
        "recentOrders": recent_orders,
        "lowStockProductsList": low_stock_products_list
    }
