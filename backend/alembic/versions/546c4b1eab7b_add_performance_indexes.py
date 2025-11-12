"""add_performance_indexes

Revision ID: 546c4b1eab7b
Revises: d4e5f6a7b8c9
Create Date: 2025-11-10 15:20:28.034517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '546c4b1eab7b'
down_revision = 'd4e5f6a7b8c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Products table indexes for better query performance

    # Index on price for range queries (min_price, max_price filters)
    op.create_index('idx_products_price', 'products', ['price'])

    # Index on stock for availability queries (in_stock, low_stock)
    op.create_index('idx_products_stock', 'products', ['stock'])

    # Composite index for category + stock queries (common combination)
    op.create_index(
        'idx_products_category_stock',
        'products',
        ['category_id', 'stock']
    )

    # Composite index for category + price queries (for sorting by price within category)
    op.create_index(
        'idx_products_category_price',
        'products',
        ['category_id', 'price']
    )

    # Orders table composite indexes for better filtering and pagination

    # Composite index for user + status queries (get user orders by status)
    op.create_index(
        'idx_orders_user_status',
        'orders',
        ['user_id', 'status']
    )

    # Composite index for user + created_at (pagination for user orders)
    op.create_index(
        'idx_orders_user_created',
        'orders',
        ['user_id', 'created_at']
    )

    # Composite index for status + created_at (admin filtering by status)
    op.create_index(
        'idx_orders_status_created',
        'orders',
        ['status', 'created_at']
    )

    # Order items table indexes for joins

    # Index on order_id for faster joins (if not already created by FK)
    op.create_index('idx_order_items_order_id', 'order_items', ['order_id'])

    # Index on product_id for joins with products table
    op.create_index('idx_order_items_product_id', 'order_items', ['product_id'])


def downgrade() -> None:
    # Drop all created indexes in reverse order
    op.drop_index('idx_order_items_product_id', table_name='order_items')
    op.drop_index('idx_order_items_order_id', table_name='order_items')
    op.drop_index('idx_orders_status_created', table_name='orders')
    op.drop_index('idx_orders_user_created', table_name='orders')
    op.drop_index('idx_orders_user_status', table_name='orders')
    op.drop_index('idx_products_category_price', table_name='products')
    op.drop_index('idx_products_category_stock', table_name='products')
    op.drop_index('idx_products_stock', table_name='products')
    op.drop_index('idx_products_price', table_name='products')
