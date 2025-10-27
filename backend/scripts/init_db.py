"""
Script to initialize the database with sample data
Run this script to populate the database with categories and products
Pass --force flag to clear existing data and reinitialize
"""
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parents[1]))

from app.config.database import SessionLocal, engine
from app.models import Base, Category, Product, Cart, CartItem, Order, OrderItem, OrderStatus


def init_database(force=False):
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if data already exists
        existing_categories = db.query(Category).count()
        if existing_categories > 0:
            if not force:
                print("Database already has data. Use --force to clear and reinitialize.")
                return
            else:
                print("Clearing existing data...")
                # Delete all data in correct order (respecting foreign keys)
                db.query(OrderItem).delete()
                db.query(Order).delete()
                db.query(CartItem).delete()
                db.query(Cart).delete()
                db.query(Product).delete()
                db.query(Category).delete()
                db.commit()
                print("Existing data cleared.")

        # Create categories - Non-perishable products with anime theme focus
        categories_data = [
            {"name": "Ramen y Fideos", "description": "Fideos instantáneos japoneses y coreanos estilo anime"},
            {"name": "Snacks Salados", "description": "Aperitivos crujientes y snacks asiáticos"},
            {"name": "Dulces y Golosinas", "description": "Golosinas, chocolates y dulces japoneses"},
            {"name": "Bebidas", "description": "Bebidas japonesas y asiáticas"},
            {"name": "Salsas y Condimentos", "description": "Salsas y condimentos para cocina asiática"},
            {"name": "Arroz y Productos Secos", "description": "Arroz premium y alimentos secos asiáticos"},
        ]

        categories = []
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.add(category)
            categories.append(category)

        db.commit()
        print(f"Created {len(categories)} categories")

        # Refresh to get IDs
        for cat in categories:
            db.refresh(cat)

        # Create products - Non-perishable items from EMB Food catalog
        products_data = [
            # Ramen y Fideos (Category 0)
            {
                "name": "Ramen Carbonara SAMYANG 5Pack",
                "description": "Pack de 5 ramen instantáneos con sabor a carbonara - 40x130g",
                "price": 6.50,
                "stock": 100,
                "category_id": categories[0].id,
                "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624"
            },
            {
                "name": "Nongshim Shin Ramyun",
                "description": "Ramen coreano picante con sabor a carne y verduras - El favorito de los animes",
                "price": 1.50,
                "stock": 150,
                "category_id": categories[0].id,
                "image_url": "https://images.unsplash.com/photo-1623341214825-9f4f963727da"
            },
            {
                "name": "Samyang Buldak Hot Chicken Ramen",
                "description": "Fideos súper picantes con sabor a pollo - Nivel picante extremo",
                "price": 1.85,
                "stock": 120,
                "category_id": categories[0].id,
                "image_url": "https://images.unsplash.com/photo-1585032226651-759b368d7246"
            },
            {
                "name": "Nissin Cup Noodles Original",
                "description": "Fideos instantáneos en vaso, listos en 3 minutos",
                "price": 1.20,
                "stock": 200,
                "category_id": categories[0].id,
                "image_url": "https://images.unsplash.com/photo-1617093727343-374698b1b08d"
            },
            {
                "name": "Indomie Mi Goreng",
                "description": "Fideos fritos indonesios con salsa dulce y picante",
                "price": 0.95,
                "stock": 180,
                "category_id": categories[0].id,
                "image_url": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841"
            },

            # Snacks Salados (Category 1)
            {
                "name": "Algas Nori Tostadas",
                "description": "Algas tostadas y sazonadas estilo japonés - Snack saludable",
                "price": 2.80,
                "stock": 100,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351"
            },
            {
                "name": "Galletas de Arroz Senbei",
                "description": "Galletas crujientes de arroz japonesas tradicionales",
                "price": 3.20,
                "stock": 80,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1582716401301-b2407dc7563d"
            },
            {
                "name": "Wasabi Peas",
                "description": "Guisantes crujientes con wasabi - Snack picante japonés",
                "price": 2.50,
                "stock": 90,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1599490659213-e2b9527bd087"
            },
            {
                "name": "Pretz Palitos Salados",
                "description": "Palitos de galleta salada estilo japonés - Varios sabores",
                "price": 2.30,
                "stock": 110,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1621939514649-280e2ee25f60"
            },
            {
                "name": "Chips de Camarón",
                "description": "Crackers crujientes de camarón - Snack asiático clásico",
                "price": 2.90,
                "stock": 95,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1613919120408-66f4a49ddf4d"
            },

            # Dulces y Golosinas (Category 2)
            {
                "name": "Pocky Chocolate",
                "description": "Palitos de galleta cubiertos de chocolate - Icónico snack de anime",
                "price": 2.40,
                "stock": 150,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1621939514649-280e2ee25f60"
            },
            {
                "name": "Pocky Fresa",
                "description": "Palitos de galleta con cobertura de fresa",
                "price": 2.40,
                "stock": 140,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1581798459219-c0f6b53b81d8"
            },
            {
                "name": "Pocky Matcha",
                "description": "Palitos de galleta con té verde matcha - Sabor premium",
                "price": 2.80,
                "stock": 100,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1582450871972-ab5ca641643d"
            },
            {
                "name": "Kit Kat Japonés Matcha",
                "description": "Kit Kat de té verde matcha - Edición japonesa exclusiva",
                "price": 4.50,
                "stock": 80,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1606312619070-d48b4863db88"
            },
            {
                "name": "Kit Kat Japonés Sakura",
                "description": "Kit Kat sabor flor de cerezo - Edición limitada",
                "price": 4.80,
                "stock": 60,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1606890737921-86d1d9a3a7b6"
            },
            {
                "name": "Hi-Chew Surtido",
                "description": "Caramelos masticables japoneses - Sabores de frutas variadas",
                "price": 3.20,
                "stock": 120,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1582735689155-184926d293d0"
            },
            {
                "name": "Mochi Daifuku Mix",
                "description": "Mochi relleno de pasta de judía dulce - Variedad de sabores",
                "price": 5.50,
                "stock": 70,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1582716401301-b2407dc7563d"
            },
            {
                "name": "Yan Yan Chocolate",
                "description": "Palitos de galleta para mojar en crema de chocolate",
                "price": 2.20,
                "stock": 130,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1621939514649-280e2ee25f60"
            },
            {
                "name": "Galletas Panda Hello Panda",
                "description": "Galletas rellenas de chocolate con diseños de panda",
                "price": 2.50,
                "stock": 110,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35"
            },
            {
                "name": "Koala March Chocolate",
                "description": "Galletas con forma de koala rellenas de chocolate",
                "price": 2.60,
                "stock": 100,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1590080876876-25bd2eaa34c4"
            },

            # Bebidas (Category 3)
            {
                "name": "Ramune Original",
                "description": "Refresco japonés con bola de cristal - Bebida icónica de anime",
                "price": 2.50,
                "stock": 150,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1625772452859-1c03d5bf1137"
            },
            {
                "name": "Ramune Fresa",
                "description": "Refresco Ramune sabor fresa con bola de cristal",
                "price": 2.50,
                "stock": 140,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1625772299848-391b6a87d7b3"
            },
            {
                "name": "Ramune Melón",
                "description": "Refresco Ramune sabor melón con bola de cristal",
                "price": 2.50,
                "stock": 130,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1625772299872-6ab2b8f97f00"
            },
            {
                "name": "Calpico Original",
                "description": "Bebida láctea fermentada japonesa - Sabor refrescante único",
                "price": 3.20,
                "stock": 100,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1584308972272-9e4e7685e80f"
            },
            {
                "name": "Té Verde Matcha Premium Lata",
                "description": "Té verde matcha japonés sin azúcar - Listo para beber",
                "price": 2.80,
                "stock": 120,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1564890369478-c89ca6d9cda9"
            },
            {
                "name": "Pocari Sweat",
                "description": "Bebida isotónica japonesa - Popular en anime deportivo",
                "price": 2.90,
                "stock": 110,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1624517452488-04869289c4ca"
            },

            # Salsas y Condimentos (Category 4)
            {
                "name": "Salsa de Soja KIKKOMAN 1L",
                "description": "Salsa de soja tradicional japonesa premium - 6x1L",
                "price": 8.50,
                "stock": 80,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1594798592208-0c6d322d9132"
            },
            {
                "name": "Salsa de Soja KIKKOMAN 500ml",
                "description": "Salsa de soja tradicional japonesa - Tamaño estándar",
                "price": 4.50,
                "stock": 120,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1594798592208-0c6d322d9132"
            },
            {
                "name": "Sriracha Huy Fong",
                "description": "Salsa picante de chile tailandesa - La original con gallo",
                "price": 4.20,
                "stock": 100,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1472476443507-c7a5948772fc"
            },
            {
                "name": "Aceite de Sésamo Tostado",
                "description": "Aceite aromático de sésamo para cocina asiática - 250ml",
                "price": 5.80,
                "stock": 70,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5"
            },
            {
                "name": "Salsa Teriyaki",
                "description": "Salsa teriyaki para marinad y glaseado - Sabor agridulce",
                "price": 3.90,
                "stock": 90,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8"
            },
            {
                "name": "Pasta de Miso",
                "description": "Pasta de miso para sopa y cocina japonesa - 500g",
                "price": 6.50,
                "stock": 60,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
            },

            # Arroz y Productos Secos (Category 5)
            {
                "name": "Arroz para Sushi Premium",
                "description": "Arroz de grano corto japonés ideal para sushi - 2kg",
                "price": 9.50,
                "stock": 80,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1516684732162-798a0062be99"
            },
            {
                "name": "Arroz Japonés Koshihikari",
                "description": "Arroz premium japonés - La variedad más apreciada - 1kg",
                "price": 12.00,
                "stock": 50,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c"
            },
            {
                "name": "Algas Nori para Sushi",
                "description": "Láminas de alga nori tostada - Pack de 50 hojas",
                "price": 7.50,
                "stock": 70,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351"
            },
            {
                "name": "Fideos Soba Secos",
                "description": "Fideos de trigo sarraceno japoneses - 300g",
                "price": 4.20,
                "stock": 85,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1617093727343-374698b1b08d"
            },
            {
                "name": "Fideos Udon Secos",
                "description": "Fideos udon gruesos tradicionales - 300g",
                "price": 3.80,
                "stock": 90,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1626266061368-46a8f578ddd6"
            },
        ]

        products = []
        for prod_data in products_data:
            product = Product(**prod_data)
            db.add(product)
            products.append(product)

        db.commit()
        print(f"Created {len(products)} products")

        # Create sample carts (optional - for testing)
        sample_carts_data = [
            {
                "user_id": "test-user-1",
                "items": [
                    {"product_id": products[1].id, "quantity": 2},  # Shin Ramyun
                    {"product_id": products[27].id, "quantity": 1},  # Salsa de Soja KIKKOMAN
                ]
            },
            {
                "user_id": "test-user-2",
                "items": [
                    {"product_id": products[10].id, "quantity": 3},  # Pocky Chocolate
                    {"product_id": products[20].id, "quantity": 2},  # Ramune Original
                ]
            }
        ]

        for cart_data in sample_carts_data:
            cart = Cart(user_id=cart_data["user_id"])
            db.add(cart)
            db.commit()
            db.refresh(cart)

            for item_data in cart_data["items"]:
                cart_item = CartItem(
                    cart_id=cart.id,
                    product_id=item_data["product_id"],
                    quantity=item_data["quantity"]
                )
                db.add(cart_item)

        db.commit()
        print(f"Created {len(sample_carts_data)} sample carts")

        # Create sample orders (optional - for testing)
        sample_orders_data = [
            {
                "user_id": "test-user-3",
                "status": OrderStatus.CONFIRMED,
                "customer_name": "Juan Pérez",
                "customer_email": "juan.perez@example.com",
                "customer_phone": "+34 612 345 678",
                "shipping_address": "Calle Mayor 123, 28013 Madrid, España",
                "notes": "Por favor, llamar antes de entregar",
                "items": [
                    {"product_id": products[0].id, "quantity": 2, "unit_price": products[0].price},  # Ramen Carbonara SAMYANG
                    {"product_id": products[1].id, "quantity": 5, "unit_price": products[1].price},  # Shin Ramyun
                    {"product_id": products[10].id, "quantity": 4, "unit_price": products[10].price},  # Pocky Chocolate
                ]
            },
            {
                "user_id": "test-user-4",
                "status": OrderStatus.DELIVERED,
                "customer_name": "María García",
                "customer_email": "maria.garcia@example.com",
                "customer_phone": "+34 623 456 789",
                "shipping_address": "Avenida de la Constitución 45, 41001 Sevilla, España",
                "notes": None,
                "items": [
                    {"product_id": products[20].id, "quantity": 6, "unit_price": products[20].price},  # Ramune Original
                    {"product_id": products[15].id, "quantity": 3, "unit_price": products[15].price},  # Hi-Chew
                    {"product_id": products[33].id, "quantity": 1, "unit_price": products[33].price},  # Arroz para Sushi
                ]
            }
        ]

        for order_data in sample_orders_data:
            # Calculate total
            total_amount = sum(
                item["quantity"] * item["unit_price"]
                for item in order_data["items"]
            )

            order = Order(
                user_id=order_data["user_id"],
                status=order_data["status"],
                total_amount=total_amount,
                customer_name=order_data["customer_name"],
                customer_email=order_data["customer_email"],
                customer_phone=order_data["customer_phone"],
                shipping_address=order_data["shipping_address"],
                notes=order_data["notes"]
            )
            db.add(order)
            db.commit()
            db.refresh(order)

            for item_data in order_data["items"]:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item_data["product_id"],
                    quantity=item_data["quantity"],
                    unit_price=item_data["unit_price"],
                    subtotal=item_data["quantity"] * item_data["unit_price"]
                )
                db.add(order_item)

        db.commit()
        print(f"Created {len(sample_orders_data)} sample orders")
        print("Database initialization completed successfully!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    force = "--force" in sys.argv
    if force:
        print("Force mode enabled: will clear existing data")
    print("Initializing database...")
    init_database(force=force)
