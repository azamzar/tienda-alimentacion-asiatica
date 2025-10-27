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
            {"name": "Dulces Japoneses", "description": "Caramelos y golosinas tradicionales japonesas"},
            {"name": "Chocolates y Galletas", "description": "Pocky, Kit Kat y galletas japonesas"},
            {"name": "Productos Anime", "description": "Productos con personajes de anime y manga"},
            {"name": "DIY y Especiales", "description": "Kits para hacer dulces y ediciones limitadas"},
            {"name": "Snacks Salados", "description": "Aperitivos crujientes y snacks asiáticos"},
            {"name": "Bebidas", "description": "Bebidas japonesas y asiáticas"},
            {"name": "Salsas y Condimentos", "description": "Salsas y condimentos para cocina asiática"},
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

        # Create products - Anime-themed candies and Japanese snacks catalog
        products_data = [
            # Ramen y Fideos (Category 0)
            {
                "name": "Ramen Carbonara SAMYANG 5Pack",
                "description": "Pack de 5 ramen instantáneos con sabor a carbonara - Como en los animes",
                "price": 6.50,
                "stock": 100,
                "category_id": categories[0].id,
                "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624"
            },
            {
                "name": "Nongshim Shin Ramyun",
                "description": "Ramen coreano picante - El favorito de los protagonistas de anime",
                "price": 1.50,
                "stock": 150,
                "category_id": categories[0].id,
                "image_url": "https://images.unsplash.com/photo-1623341214825-9f4f963727da"
            },
            {
                "name": "Samyang Buldak Hot Chicken Ramen",
                "description": "Fideos súper picantes - Desafío picante nivel extremo",
                "price": 1.85,
                "stock": 120,
                "category_id": categories[0].id,
                "image_url": "https://images.unsplash.com/photo-1585032226651-759b368d7246"
            },
            {
                "name": "Nissin Cup Noodles Original",
                "description": "Fideos instantáneos en vaso - Comida rápida otaku",
                "price": 1.20,
                "stock": 200,
                "category_id": categories[0].id,
                "image_url": "https://images.unsplash.com/photo-1617093727343-374698b1b08d"
            },
            {
                "name": "Maruchan Ramen Tonkotsu",
                "description": "Ramen estilo Hakata con caldo cremoso de cerdo",
                "price": 1.30,
                "stock": 180,
                "category_id": categories[0].id,
                "image_url": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841"
            },
            {
                "name": "Sapporo Ichiban Miso Ramen",
                "description": "Ramen con sabor a miso tradicional japonés",
                "price": 1.40,
                "stock": 160,
                "category_id": categories[0].id,
                "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624"
            },

            # Dulces Japoneses (Category 1)
            {
                "name": "Hi-Chew Surtido Frutas",
                "description": "Caramelos masticables súper jugosos - Sabores: fresa, uva, manzana",
                "price": 3.20,
                "stock": 200,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1582735689155-184926d293d0"
            },
            {
                "name": "Hi-Chew Mango",
                "description": "Caramelos masticables sabor mango tropical",
                "price": 2.80,
                "stock": 180,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1582735689369-4fe2e9a5f1b6"
            },
            {
                "name": "Hi-Chew Fresa Premium",
                "description": "Caramelos masticables sabor fresa japonesa",
                "price": 2.80,
                "stock": 180,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1514517521153-1be72277b32f"
            },
            {
                "name": "Kasugai Gummy Mix",
                "description": "Gominolas japonesas con sabores de frutas reales",
                "price": 2.50,
                "stock": 150,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1582037928769-181f2644ecb7"
            },
            {
                "name": "Kasugai Gummy Uva",
                "description": "Gominolas sabor uva Muscat japonesa",
                "price": 2.30,
                "stock": 140,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1599683560574-c55276007e64"
            },
            {
                "name": "Kasugai Gummy Melocotón",
                "description": "Gominolas sabor melocotón blanco",
                "price": 2.30,
                "stock": 140,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1587248720327-f5b2c9eeb0fe"
            },
            {
                "name": "Morinaga Ramune Candy",
                "description": "Caramelos efervescentes sabor Ramune - Clásico japonés",
                "price": 2.10,
                "stock": 170,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1625772452859-1c03d5bf1137"
            },
            {
                "name": "Fujiya Milky Candy",
                "description": "Caramelos cremosos de leche - Mascota Peko Chan",
                "price": 2.99,
                "stock": 160,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1584308972272-9e4e7685e80f"
            },
            {
                "name": "Meiji Yogurt Candy",
                "description": "Caramelos sabor yogur probiótico",
                "price": 2.50,
                "stock": 150,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1571212515416-26f6a41ed75e"
            },
            {
                "name": "Konpeito Azucarillos",
                "description": "Caramelos de azúcar tradicionales multicolor - Como en El Viaje de Chihiro",
                "price": 3.50,
                "stock": 100,
                "category_id": categories[1].id,
                "image_url": "https://images.unsplash.com/photo-1514517521153-1be72277b32f"
            },

            # Chocolates y Galletas (Category 2)
            {
                "name": "Pocky Chocolate Clásico",
                "description": "Palitos de galleta cubiertos de chocolate - Icono del anime",
                "price": 2.40,
                "stock": 250,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1621939514649-280e2ee25f60"
            },
            {
                "name": "Pocky Fresa",
                "description": "Palitos de galleta con cobertura de fresa",
                "price": 2.40,
                "stock": 240,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1581798459219-c0f6b53b81d8"
            },
            {
                "name": "Pocky Matcha Green Tea",
                "description": "Palitos de galleta con té verde matcha premium",
                "price": 2.80,
                "stock": 200,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1582450871972-ab5ca641643d"
            },
            {
                "name": "Pocky Cookies & Cream",
                "description": "Palitos de galleta con crema de cookies",
                "price": 2.60,
                "stock": 180,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e"
            },
            {
                "name": "Pocky Almond Crush",
                "description": "Palitos de galleta con chocolate y almendra triturada",
                "price": 2.90,
                "stock": 170,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1606312619070-d48b4863db88"
            },
            {
                "name": "Kit Kat Matcha Japonés",
                "description": "Kit Kat de té verde matcha - Edición exclusiva Japón",
                "price": 4.50,
                "stock": 150,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1606312619070-d48b4863db88"
            },
            {
                "name": "Kit Kat Sakura Flor de Cerezo",
                "description": "Kit Kat sabor flor de cerezo - Edición limitada primavera",
                "price": 4.80,
                "stock": 100,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1606890737921-86d1d9a3a7b6"
            },
            {
                "name": "Kit Kat Sake Japonés",
                "description": "Kit Kat con sabor a sake japonés - Edición premium",
                "price": 5.20,
                "stock": 80,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1606312619070-d48b4863db88"
            },
            {
                "name": "Kit Kat Wasabi",
                "description": "Kit Kat picante de wasabi - Para aventureros",
                "price": 4.90,
                "stock": 90,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1606312619070-d48b4863db88"
            },
            {
                "name": "Yan Yan Chocolate",
                "description": "Palitos de galleta para mojar en crema de chocolate",
                "price": 2.20,
                "stock": 200,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1621939514649-280e2ee25f60"
            },
            {
                "name": "Yan Yan Fresa",
                "description": "Palitos de galleta para mojar en crema de fresa",
                "price": 2.20,
                "stock": 190,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1621939514649-280e2ee25f60"
            },
            {
                "name": "Hello Panda Chocolate",
                "description": "Galletas rellenas de chocolate con diseños de panda",
                "price": 2.50,
                "stock": 180,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35"
            },
            {
                "name": "Hello Panda Fresa",
                "description": "Galletas rellenas de crema de fresa con pandas",
                "price": 2.50,
                "stock": 180,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35"
            },
            {
                "name": "Koala March Chocolate",
                "description": "Galletas con forma de koala rellenas de chocolate",
                "price": 2.60,
                "stock": 170,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1590080876876-25bd2eaa34c4"
            },
            {
                "name": "Koala March Fresa",
                "description": "Galletas koala rellenas de crema de fresa",
                "price": 2.60,
                "stock": 170,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1590080876876-25bd2eaa34c4"
            },
            {
                "name": "Toppo Chocolate Sticks",
                "description": "Palitos de pretzel rellenos de chocolate",
                "price": 2.70,
                "stock": 160,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1621939514649-280e2ee25f60"
            },
            {
                "name": "Apollo Chocolate Fresa",
                "description": "Chocolates cónicos con forma de cohete - Nostálgico",
                "price": 2.40,
                "stock": 150,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1606890737921-86d1d9a3a7b6"
            },
            {
                "name": "Chocorooms Meiji",
                "description": "Chocolates con forma de setas - Famosos en anime",
                "price": 3.20,
                "stock": 140,
                "category_id": categories[2].id,
                "image_url": "https://images.unsplash.com/photo-1606312619070-d48b4863db88"
            },

            # Productos Anime (Category 3)
            # Cajas sorpresa creadas por la tienda
            {
                "name": "Caja Sorpresa Pokémon Mix",
                "description": "Surtido de dulces y snacks con temática Pokémon - Creada por la tienda",
                "price": 12.99,
                "stock": 80,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1613975679558-45e4564b5a53"
            },
            {
                "name": "Caja Sorpresa Hello Kitty",
                "description": "Dulces y snacks de Hello Kitty y Sanrio - Creada por la tienda",
                "price": 11.99,
                "stock": 90,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1582735689369-4fe2e9a5f1b6"
            },
            {
                "name": "Caja Sorpresa My Melody",
                "description": "Productos kawaii de My Melody de Sanrio - Creada por la tienda",
                "price": 11.99,
                "stock": 85,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1514517521153-1be72277b32f"
            },

            # Productos individuales Pokémon (para cajas o venta individual)
            {
                "name": "Galletas Pokémon Pikachu",
                "description": "Galletas de mantequilla con diseño de Pikachu",
                "price": 3.50,
                "stock": 150,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35"
            },
            {
                "name": "Gominolas Pokémon Mix",
                "description": "Gominolas con formas de Pokémon: Pikachu, Bulbasaur, Charmander",
                "price": 2.99,
                "stock": 180,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1582037928769-181f2644ecb7"
            },
            {
                "name": "Chocolates Pokémon Ball",
                "description": "Chocolates con forma de Pokébola con sorpresa",
                "price": 3.80,
                "stock": 140,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1606890737921-86d1d9a3a7b6"
            },
            {
                "name": "Caramelos Pokémon Surtidos",
                "description": "Caramelos duros con sabores de frutas y diseños Pokémon",
                "price": 2.50,
                "stock": 160,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1514517521153-1be72277b32f"
            },
            {
                "name": "Pocky Pokémon Edición",
                "description": "Pocky chocolate con packaging especial Pokémon",
                "price": 2.90,
                "stock": 130,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1621939514649-280e2ee25f60"
            },

            # Productos individuales Hello Kitty / Sanrio
            {
                "name": "Galletas Hello Kitty",
                "description": "Galletas de fresa con diseño de Hello Kitty",
                "price": 3.50,
                "stock": 160,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35"
            },
            {
                "name": "Chocolates Hello Kitty",
                "description": "Chocolates con leche en forma de cara de Hello Kitty",
                "price": 3.80,
                "stock": 140,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1606890737921-86d1d9a3a7b6"
            },
            {
                "name": "Caramelos Hello Kitty Fresa",
                "description": "Caramelos duros sabor fresa con diseño Hello Kitty",
                "price": 2.60,
                "stock": 170,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1514517521153-1be72277b32f"
            },
            {
                "name": "Marshmallows Hello Kitty",
                "description": "Marshmallows de vainilla con forma de Hello Kitty",
                "price": 3.20,
                "stock": 120,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1582735689155-184926d293d0"
            },
            {
                "name": "Galletas My Melody",
                "description": "Galletas de fresa con diseño de My Melody",
                "price": 3.50,
                "stock": 140,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35"
            },
            {
                "name": "Chocolates My Melody",
                "description": "Chocolates con leche y diseño de My Melody",
                "price": 3.70,
                "stock": 130,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1606890737921-86d1d9a3a7b6"
            },
            {
                "name": "Galletas Kuromi",
                "description": "Galletas con diseño de Kuromi de Sanrio",
                "price": 3.50,
                "stock": 120,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35"
            },
            {
                "name": "Caramelos Cinnamoroll",
                "description": "Caramelos de canela con diseño de Cinnamoroll",
                "price": 2.80,
                "stock": 130,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1514517521153-1be72277b32f"
            },

            # Productos individuales Rilakkuma
            {
                "name": "Galletas Rilakkuma",
                "description": "Galletas con diseño del oso Rilakkuma",
                "price": 3.80,
                "stock": 120,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1590080876876-25bd2eaa34c4"
            },
            {
                "name": "Chocolates Rilakkuma",
                "description": "Chocolates con forma de Rilakkuma",
                "price": 4.20,
                "stock": 110,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1606890737921-86d1d9a3a7b6"
            },

            # Productos individuales Studio Ghibli
            {
                "name": "Galletas Totoro",
                "description": "Galletas con forma de Totoro de Mi Vecino Totoro",
                "price": 3.90,
                "stock": 110,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1590080876876-25bd2eaa34c4"
            },
            {
                "name": "Chocolates Studio Ghibli Mix",
                "description": "Chocolates con personajes: Totoro, No-Face, Calcifer",
                "price": 5.50,
                "stock": 100,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1606890737921-86d1d9a3a7b6"
            },
            {
                "name": "Caramelos Spirited Away",
                "description": "Caramelos inspirados en El Viaje de Chihiro",
                "price": 3.20,
                "stock": 90,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1514517521153-1be72277b32f"
            },

            # Productos individuales Doraemon
            {
                "name": "Galletas Doraemon",
                "description": "Galletas con diseño de Doraemon",
                "price": 3.50,
                "stock": 130,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35"
            },
            {
                "name": "Chocolates Doraemon",
                "description": "Chocolates con forma de Doraemon",
                "price": 3.80,
                "stock": 120,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1606890737921-86d1d9a3a7b6"
            },
            {
                "name": "Ramune Candy Doraemon",
                "description": "Caramelos Ramune con diseño de Doraemon en el packaging",
                "price": 2.50,
                "stock": 140,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1625772452859-1c03d5bf1137"
            },
            {
                "name": "Gominolas Doraemon",
                "description": "Gominolas con forma de Doraemon y Dorami",
                "price": 2.90,
                "stock": 130,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1582037928769-181f2644ecb7"
            },

            # Productos individuales otros anime populares
            {
                "name": "Mochi Pikachu",
                "description": "Mochi suave con diseño de Pikachu",
                "price": 4.20,
                "stock": 110,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1582716401301-b2407dc7563d"
            },
            {
                "name": "Galletas Naruto",
                "description": "Galletas con símbolos de Naruto",
                "price": 3.60,
                "stock": 100,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35"
            },
            {
                "name": "Snacks Ramen Naruto",
                "description": "Snacks crujientes con forma de Naruto maki",
                "price": 2.80,
                "stock": 120,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1613919120408-66f4a49ddf4d"
            },
            {
                "name": "Chocolates Naruto",
                "description": "Chocolates con diseños de personajes de Naruto",
                "price": 4.50,
                "stock": 90,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1606890737921-86d1d9a3a7b6"
            },
            {
                "name": "Galletas One Piece",
                "description": "Galletas con el logo de One Piece y sombrero de Luffy",
                "price": 3.70,
                "stock": 100,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35"
            },
            {
                "name": "Gominolas One Piece",
                "description": "Gominolas con formas de Frutas del Diablo",
                "price": 3.20,
                "stock": 110,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1582037928769-181f2644ecb7"
            },
            {
                "name": "Chocolates One Piece",
                "description": "Chocolates con personajes de la tripulación Mugiwara",
                "price": 4.80,
                "stock": 85,
                "category_id": categories[3].id,
                "image_url": "https://images.unsplash.com/photo-1606890737921-86d1d9a3a7b6"
            },

            # DIY y Especiales (Category 4)
            {
                "name": "Popin Cookin Sushi DIY",
                "description": "Kit para hacer sushi de dulce - Experiencia divertida",
                "price": 5.99,
                "stock": 100,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351"
            },
            {
                "name": "Popin Cookin Donuts DIY",
                "description": "Kit para crear mini donuts de dulce",
                "price": 5.99,
                "stock": 95,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1514517521153-1be72277b32f"
            },
            {
                "name": "Popin Cookin Ramen DIY",
                "description": "Kit para hacer ramen de gominola",
                "price": 6.50,
                "stock": 90,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624"
            },
            {
                "name": "Kracie Happy Kitchen Hamburguesa",
                "description": "Kit DIY para crear hamburguesa de dulce",
                "price": 5.50,
                "stock": 85,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e"
            },
            {
                "name": "Kracie Happy Kitchen Bento",
                "description": "Kit para hacer bento japonés de gominola",
                "price": 6.20,
                "stock": 80,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1580822184713-fc5400e7fe10"
            },
            {
                "name": "Mochi Daifuku Mix",
                "description": "Mochi relleno de pasta de judía dulce - Sabores variados",
                "price": 5.50,
                "stock": 120,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1582716401301-b2407dc7563d"
            },
            {
                "name": "Mochi Ice Cream Mix",
                "description": "Mochi con helado - Edición especial",
                "price": 6.80,
                "stock": 90,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1582716401301-b2407dc7563d"
            },
            {
                "name": "Taiyaki de Chocolate",
                "description": "Galletas con forma de pez taiyaki rellenas de chocolate",
                "price": 3.90,
                "stock": 110,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1590080876876-25bd2eaa34c4"
            },
            {
                "name": "Dango Hanami Especial",
                "description": "Dango tradicionales para celebrar el hanami",
                "price": 4.50,
                "stock": 100,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1582716401301-b2407dc7563d"
            },
            {
                "name": "Castella Cake Mix",
                "description": "Bizcocho esponjoso japonés - Como en los animes",
                "price": 7.50,
                "stock": 70,
                "category_id": categories[4].id,
                "image_url": "https://images.unsplash.com/photo-1578985545062-69928b1d9587"
            },

            # Snacks Salados (Category 5)
            {
                "name": "Algas Nori Tostadas",
                "description": "Algas tostadas y sazonadas estilo japonés - Snack saludable",
                "price": 2.80,
                "stock": 150,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351"
            },
            {
                "name": "Galletas de Arroz Senbei",
                "description": "Galletas crujientes de arroz japonesas tradicionales",
                "price": 3.20,
                "stock": 140,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1582716401301-b2407dc7563d"
            },
            {
                "name": "Wasabi Peas",
                "description": "Guisantes crujientes con wasabi - Snack picante japonés",
                "price": 2.50,
                "stock": 130,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1599490659213-e2b9527bd087"
            },
            {
                "name": "Pretz Palitos Salados",
                "description": "Palitos de galleta salada estilo japonés - Varios sabores",
                "price": 2.30,
                "stock": 160,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1621939514649-280e2ee25f60"
            },
            {
                "name": "Chips de Camarón Krupuk",
                "description": "Crackers crujientes de camarón - Snack asiático clásico",
                "price": 2.90,
                "stock": 140,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1613919120408-66f4a49ddf4d"
            },
            {
                "name": "Calbee Pizza Potato Chips",
                "description": "Patatas fritas japonesas sabor pizza",
                "price": 3.50,
                "stock": 120,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1566478989037-eec170784d0b"
            },
            {
                "name": "Jagarico Potato Sticks",
                "description": "Palitos de patata crujientes - Sabor salad",
                "price": 2.80,
                "stock": 150,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1621447504864-d8686e12698c"
            },
            {
                "name": "Umaibo Corn Puffs Mix",
                "description": "Snacks de maíz en forma de cilindro - Sabores variados",
                "price": 1.50,
                "stock": 200,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1613919120408-66f4a49ddf4d"
            },
            {
                "name": "Baby Star Ramen Snack",
                "description": "Mini fideos ramen crujientes para snack",
                "price": 1.80,
                "stock": 180,
                "category_id": categories[5].id,
                "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624"
            },

            # Bebidas (Category 6)
            {
                "name": "Ramune Original",
                "description": "Refresco japonés con bola de cristal - Bebida icónica de anime",
                "price": 2.50,
                "stock": 200,
                "category_id": categories[6].id,
                "image_url": "https://images.unsplash.com/photo-1625772452859-1c03d5bf1137"
            },
            {
                "name": "Ramune Fresa",
                "description": "Refresco Ramune sabor fresa con bola de cristal",
                "price": 2.50,
                "stock": 190,
                "category_id": categories[6].id,
                "image_url": "https://images.unsplash.com/photo-1625772299848-391b6a87d7b3"
            },
            {
                "name": "Ramune Melón",
                "description": "Refresco Ramune sabor melón con bola de cristal",
                "price": 2.50,
                "stock": 180,
                "category_id": categories[6].id,
                "image_url": "https://images.unsplash.com/photo-1625772299872-6ab2b8f97f00"
            },
            {
                "name": "Ramune Lichi",
                "description": "Refresco Ramune sabor lichi tropical",
                "price": 2.50,
                "stock": 170,
                "category_id": categories[6].id,
                "image_url": "https://images.unsplash.com/photo-1625772452859-1c03d5bf1137"
            },
            {
                "name": "Calpico Original",
                "description": "Bebida láctea fermentada japonesa - Sabor refrescante único",
                "price": 3.20,
                "stock": 150,
                "category_id": categories[6].id,
                "image_url": "https://images.unsplash.com/photo-1584308972272-9e4e7685e80f"
            },
            {
                "name": "Calpico Fresa",
                "description": "Bebida láctea fermentada sabor fresa",
                "price": 3.20,
                "stock": 140,
                "category_id": categories[6].id,
                "image_url": "https://images.unsplash.com/photo-1584308972272-9e4e7685e80f"
            },
            {
                "name": "Té Verde Matcha Premium Lata",
                "description": "Té verde matcha japonés sin azúcar - Listo para beber",
                "price": 2.80,
                "stock": 160,
                "category_id": categories[6].id,
                "image_url": "https://images.unsplash.com/photo-1564890369478-c89ca6d9cda9"
            },
            {
                "name": "Pocari Sweat",
                "description": "Bebida isotónica japonesa - Popular en anime deportivo",
                "price": 2.90,
                "stock": 150,
                "category_id": categories[6].id,
                "image_url": "https://images.unsplash.com/photo-1624517452488-04869289c4ca"
            },
            {
                "name": "Milkis Bebida Coreana",
                "description": "Bebida carbonatada cremosa sabor yogur",
                "price": 2.60,
                "stock": 140,
                "category_id": categories[6].id,
                "image_url": "https://images.unsplash.com/photo-1584308972272-9e4e7685e80f"
            },
            {
                "name": "Fanta Melocotón Japón",
                "description": "Fanta sabor melocotón - Edición exclusiva Japón",
                "price": 2.70,
                "stock": 130,
                "category_id": categories[6].id,
                "image_url": "https://images.unsplash.com/photo-1624517452488-04869289c4ca"
            },

            # Salsas y Condimentos (Category 7)
            {
                "name": "Salsa de Soja KIKKOMAN 500ml",
                "description": "Salsa de soja tradicional japonesa - Para ramen y sushi",
                "price": 4.50,
                "stock": 100,
                "category_id": categories[7].id,
                "image_url": "https://images.unsplash.com/photo-1594798592208-0c6d322d9132"
            },
            {
                "name": "Sriracha Huy Fong",
                "description": "Salsa picante de chile tailandesa - La original con gallo",
                "price": 4.20,
                "stock": 90,
                "category_id": categories[7].id,
                "image_url": "https://images.unsplash.com/photo-1472476443507-c7a5948772fc"
            },
            {
                "name": "Salsa Teriyaki",
                "description": "Salsa teriyaki para marinad y glaseado - Sabor agridulce",
                "price": 3.90,
                "stock": 85,
                "category_id": categories[7].id,
                "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8"
            },
            {
                "name": "Pasta de Miso",
                "description": "Pasta de miso para sopa y cocina japonesa - 500g",
                "price": 6.50,
                "stock": 70,
                "category_id": categories[7].id,
                "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
            },
            {
                "name": "Furikake Mix",
                "description": "Condimento japonés para arroz - Surtido de sabores",
                "price": 3.80,
                "stock": 80,
                "category_id": categories[7].id,
                "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351"
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
                    {"product_id": products[1].id, "quantity": 2},  # Nongshim Shin Ramyun
                    {"product_id": products[16].id, "quantity": 3},  # Pocky Chocolate Clásico
                    {"product_id": products[37].id, "quantity": 4},  # Gominolas Pokémon Mix
                ]
            },
            {
                "user_id": "test-user-2",
                "items": [
                    {"product_id": products[34].id, "quantity": 1},  # Caja Sorpresa Pokémon Mix
                    {"product_id": products[42].id, "quantity": 2},  # Galletas Hello Kitty
                    {"product_id": products[6].id, "quantity": 3},  # Hi-Chew Surtido Frutas
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
                "notes": "Por favor, llamar antes de entregar. Me encantan los productos de Pokémon!",
                "items": [
                    {"product_id": products[0].id, "quantity": 2, "unit_price": products[0].price},  # Ramen Carbonara SAMYANG
                    {"product_id": products[1].id, "quantity": 5, "unit_price": products[1].price},  # Nongshim Shin Ramyun
                    {"product_id": products[34].id, "quantity": 1, "unit_price": products[34].price},  # Caja Sorpresa Pokémon Mix
                    {"product_id": products[36].id, "quantity": 2, "unit_price": products[36].price},  # Galletas Pokémon Pikachu
                    {"product_id": products[16].id, "quantity": 3, "unit_price": products[16].price},  # Pocky Chocolate Clásico
                ]
            },
            {
                "user_id": "test-user-4",
                "status": OrderStatus.DELIVERED,
                "customer_name": "María García",
                "customer_email": "maria.garcia@example.com",
                "customer_phone": "+34 623 456 789",
                "shipping_address": "Avenida de la Constitución 45, 41001 Sevilla, España",
                "notes": "Fanática de Hello Kitty y Studio Ghibli",
                "items": [
                    {"product_id": products[35].id, "quantity": 1, "unit_price": products[35].price},  # Caja Sorpresa Hello Kitty
                    {"product_id": products[42].id, "quantity": 3, "unit_price": products[42].price},  # Galletas Hello Kitty
                    {"product_id": products[43].id, "quantity": 2, "unit_price": products[43].price},  # Chocolates Hello Kitty
                    {"product_id": products[59].id, "quantity": 2, "unit_price": products[59].price},  # Galletas Totoro
                    {"product_id": products[68].id, "quantity": 3, "unit_price": products[68].price},  # Popin Cookin Sushi DIY
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
