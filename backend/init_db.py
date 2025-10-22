"""
Script to initialize the database with sample data
Run this script to populate the database with categories and products
"""
from database import SessionLocal, engine
import models

def init_database():
    # Create all tables
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if data already exists
        existing_categories = db.query(models.Category).count()
        if existing_categories > 0:
            print("Database already has data. Skipping initialization.")
            return

        # Create categories
        categories_data = [
            {"name": "Ramen y Fideos", "description": "Fideos instantáneos y tradicionales asiáticos"},
            {"name": "Salsas y Condimentos", "description": "Salsas, aceites y condimentos orientales"},
            {"name": "Snacks", "description": "Aperitivos y golosinas asiáticas"},
            {"name": "Bebidas", "description": "Bebidas tradicionales y modernas de Asia"},
            {"name": "Arroz y Granos", "description": "Arroz, granos y harinas asiáticas"},
            {"name": "Congelados", "description": "Productos congelados: dim sum, gyozas, etc."},
        ]

        categories = []
        for cat_data in categories_data:
            category = models.Category(**cat_data)
            db.add(category)
            categories.append(category)

        db.commit()
        print(f"Created {len(categories)} categories")

        # Refresh to get IDs
        for cat in categories:
            db.refresh(cat)

        # Create products
        products_data = [
            # Ramen y Fideos
            {
                "name": "Nongshim Shin Ramyun",
                "description": "Ramen coreano picante con sabor a carne y verduras",
                "price": 1.50,
                "stock": 100,
                "category_id": categories[0].id,
                "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624"
            },
            {
                "name": "Samyang Buldak Hot Chicken Ramen",
                "description": "Fideos súper picantes con sabor a pollo",
                "price": 1.75,
                "stock": 80,
                "category_id": categories[0].id,
                "image_url": "https://images.unsplash.com/photo-1623341214825-9f4f963727da"
            },
            {
                "name": "Indomie Mi Goreng",
                "description": "Fideos fritos indonesios con salsa dulce y picante",
                "price": 0.50,
                "stock": 150,
                "category_id": categories[0].id,
                "image_url": "https://images.unsplash.com/photo-1585032226651-759b368d7246"
            },
            {
                "name": "Nissin Cup Noodles Seafood",
                "description": "Fideos instantáneos en vaso con sabor a mariscos",
                "price": 1.20,
                "stock": 120,
                "category_id": categories[0].id,
                "image_url": "https://images.unsplash.com/photo-1617093727343-374698b1b08d"
            },

            # Salsas y Condimentos
            {
                "name": "Salsa de Soja Kikkoman",
                "description": "Salsa de soja tradicional japonesa, 500ml",
                "price": 3.50,
                "stock": 60,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1594798592208-0c6d322d9132"
            },
            {
                "name": "Sriracha Huy Fong",
                "description": "Salsa picante de chile tailandesa, 482g",
                "price": 4.20,
                "stock": 50,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1472476443507-c7a5948772fc"
            },
            {
                "name": "Aceite de Sésamo Tostado",
                "description": "Aceite aromático de sésamo para cocina asiática, 250ml",
                "price": 5.80,
                "stock": 40,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5"
            },

            # Snacks
            {
                "name": "Pocky Chocolate",
                "description": "Palitos de galleta cubiertos de chocolate",
                "price": 2.30,
                "stock": 90,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1621939514649-280e2ee25f60"
            },
            {
                "name": "Galletas de Arroz Mochi",
                "description": "Galletas crujientes de arroz japonesas",
                "price": 3.00,
                "stock": 70,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1582716401301-b2407dc7563d"
            },
            {
                "name": "Algas Nori Snack",
                "description": "Algas tostadas y sazonadas listas para comer",
                "price": 2.80,
                "stock": 65,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351"
            },

            # Bebidas
            {
                "name": "Ramune Original",
                "description": "Bebida gaseosa japonesa con bola de cristal, 200ml",
                "price": 2.50,
                "stock": 100,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1625772452859-1c03d5bf1137"
            },
            {
                "name": "Té Verde Matcha Premium",
                "description": "Té verde matcha en polvo japonés, 100g",
                "price": 12.00,
                "stock": 30,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1564890369478-c89ca6d9cda9"
            },

            # Arroz y Granos
            {
                "name": "Arroz para Sushi Nishiki",
                "description": "Arroz de grano corto premium para sushi, 2kg",
                "price": 8.50,
                "stock": 45,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1516684732162-798a0062be99"
            },
            {
                "name": "Arroz Jazmín Tailandés",
                "description": "Arroz aromático de grano largo, 1kg",
                "price": 6.00,
                "stock": 55,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c"
            },

            # Congelados
            {
                "name": "Gyozas de Cerdo",
                "description": "Empanadillas japonesas rellenas de cerdo, 20 unidades",
                "price": 5.50,
                "stock": 40,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1496116218417-1a781b1c416c"
            },
            {
                "name": "Edamame Congelado",
                "description": "Vainas de soja verde listas para hervir, 500g",
                "price": 3.80,
                "stock": 50,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1583596112122-67b8b92e5614"
            },
        ]

        products = []
        for prod_data in products_data:
            product = models.Product(**prod_data)
            db.add(product)
            products.append(product)

        db.commit()
        print(f"Created {len(products)} products")
        print("Database initialization completed successfully!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_database()
