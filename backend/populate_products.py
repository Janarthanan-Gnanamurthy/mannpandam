"""
Script to populate the database with modern Indian pottery products.
Run this script to add products to your database.
"""
import sys
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Product

# Ensure tables exist
Base.metadata.create_all(bind=engine)

# Modern Indian Pottery Products for Contemporary Society
PRODUCTS = [
    {
        "name": "Matki Water Dispenser - Modern Design",
        "description": "Traditional earthen pot reimagined for modern kitchens. Features a sleek design with a convenient tap for easy water dispensing. Made from natural clay, it naturally cools water and adds an authentic Indian touch to contemporary homes.",
        "price": 1299.00,
        "category": "Kitchenware",
        "stock": 45,
        "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500",
        "rating": 4.5,
        "review_count": 128
    },
    {
        "name": "Bankura Horse Figurine - Terracotta Art",
        "description": "Handcrafted terracotta horse sculpture from West Bengal. This traditional Bankura horse has been redesigned with contemporary aesthetics, perfect for modern home decor. Each piece is unique and hand-painted.",
        "price": 1599.00,
        "category": "Home Decor",
        "stock": 32,
        "image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=500",
        "rating": 4.7,
        "review_count": 89
    },
    {
        "name": "Nizamabad Black Clay Vase with Silver Inlay",
        "description": "Elegant black clay vase from Uttar Pradesh featuring intricate silver inlay patterns. This contemporary piece combines traditional Nizamabad craftsmanship with modern design sensibilities, perfect for displaying flowers or as a standalone art piece.",
        "price": 1899.00,
        "category": "Home Decor",
        "stock": 28,
        "image_url": "https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=500",
        "rating": 4.6,
        "review_count": 156
    },
    {
        "name": "Jaipur Blue Pottery Decorative Plate Set",
        "description": "Set of 4 vibrant blue pottery plates from Jaipur. Each plate features intricate hand-painted designs in traditional blue and white patterns, adapted for modern dining. Food-safe glaze ensures durability and easy cleaning.",
        "price": 2499.00,
        "category": "Dinnerware",
        "stock": 38,
        "image_url": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=500",
        "rating": 4.8,
        "review_count": 203
    },
    {
        "name": "Khurja Ceramic Coffee Mug Set",
        "description": "Set of 6 colorful ceramic mugs from Khurja, Uttar Pradesh. Each mug features unique hand-painted floral and geometric patterns. Microwave and dishwasher safe, perfect for modern kitchens.",
        "price": 1799.00,
        "category": "Kitchenware",
        "stock": 52,
        "image_url": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=500",
        "rating": 4.4,
        "review_count": 167
    },
    {
        "name": "Longpi Black Pottery Tea Set",
        "description": "Contemporary tea set made from Longpi black pottery from Manipur. Crafted without a potter's wheel using traditional techniques, this set includes a teapot and 4 cups. The sleek black finish adds elegance to any modern tea ceremony.",
        "price": 3499.00,
        "category": "Kitchenware",
        "stock": 24,
        "image_url": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=500",
        "rating": 4.9,
        "review_count": 94
    },
    {
        "name": "Terracotta Planter Set - Modern Design",
        "description": "Set of 3 terracotta planters in varying sizes, perfect for indoor plants. These modern planters feature clean lines and natural reddish-brown finish. Includes drainage holes and saucers for healthy plant growth.",
        "price": 999.00,
        "category": "Garden & Outdoor",
        "stock": 67,
        "image_url": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=500",
        "rating": 4.3,
        "review_count": 245
    },
    {
        "name": "Blue Pottery Coaster Set",
        "description": "Set of 6 hand-painted blue pottery coasters from Jaipur. Each coaster features unique traditional patterns and is glazed for protection. Perfect for protecting modern furniture while adding an Indian touch.",
        "price": 699.00,
        "category": "Home Decor",
        "stock": 89,
        "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500",
        "rating": 4.5,
        "review_count": 312
    },
    {
        "name": "Nizamabad Black Clay Serving Bowl",
        "description": "Large black clay serving bowl with silver inlay border. Perfect for serving salads, fruits, or as a decorative centerpiece. The dark finish contrasts beautifully with modern table settings.",
        "price": 2199.00,
        "category": "Dinnerware",
        "stock": 31,
        "image_url": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=500",
        "rating": 4.7,
        "review_count": 178
    },
    {
        "name": "Terracotta Wall Hanging - Geometric Pattern",
        "description": "Modern terracotta wall hanging featuring contemporary geometric patterns. Handcrafted and hand-painted, this piece adds warmth and Indian heritage to minimalist modern interiors.",
        "price": 1499.00,
        "category": "Home Decor",
        "stock": 43,
        "image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=500",
        "rating": 4.6,
        "review_count": 134
    },
    {
        "name": "Khurja Dinnerware Set - 6 Pieces",
        "description": "Complete dinnerware set for 2 people (2 plates, 2 bowls, 2 cups) from Khurja. Features vibrant hand-painted designs with modern shapes. All pieces are food-safe and dishwasher safe.",
        "price": 3299.00,
        "category": "Dinnerware",
        "stock": 29,
        "image_url": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=500",
        "rating": 4.8,
        "review_count": 267
    },
    {
        "name": "Longpi Black Pottery Serving Bowl",
        "description": "Elegant black pottery serving bowl from Manipur. The smooth, matte finish and minimalist design make it perfect for modern dining. Ideal for serving rice, dal, or as a fruit bowl.",
        "price": 1899.00,
        "category": "Dinnerware",
        "stock": 36,
        "image_url": "https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=500",
        "rating": 4.5,
        "review_count": 198
    },
    {
        "name": "Blue Pottery Vase - Floral Design",
        "description": "Tall blue pottery vase from Jaipur with intricate hand-painted floral motifs. Perfect for displaying fresh or dried flowers. The vibrant blue glaze adds a pop of color to modern interiors.",
        "price": 1699.00,
        "category": "Home Decor",
        "stock": 41,
        "image_url": "https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=500",
        "rating": 4.7,
        "review_count": 223
    },
    {
        "name": "Terracotta Diya Set - Modern Candles",
        "description": "Set of 12 terracotta diyas (oil lamps) redesigned for modern use with candles. Perfect for festivals, parties, or creating ambient lighting. Each piece is handcrafted and unique.",
        "price": 599.00,
        "category": "Home Decor",
        "stock": 78,
        "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500",
        "rating": 4.4,
        "review_count": 189
    },
    {
        "name": "Nizamabad Black Clay Storage Jar",
        "description": "Airtight black clay storage jar with silver inlay lid. Perfect for storing spices, grains, or dry goods in modern kitchens. Combines traditional craftsmanship with contemporary functionality.",
        "price": 2399.00,
        "category": "Kitchenware",
        "stock": 27,
        "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500",
        "rating": 4.6,
        "review_count": 145
    },
    {
        "name": "Khurja Ceramic Serving Platter",
        "description": "Large hand-painted ceramic serving platter from Khurja. Features traditional patterns in modern colors. Perfect for serving appetizers, desserts, or as a decorative piece.",
        "price": 2799.00,
        "category": "Dinnerware",
        "stock": 33,
        "image_url": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=500",
        "rating": 4.8,
        "review_count": 156
    },
    {
        "name": "Terracotta Sculpture - Abstract Modern",
        "description": "Contemporary abstract terracotta sculpture inspired by traditional Indian forms. Handcrafted by skilled artisans, this piece serves as a statement art piece for modern homes.",
        "price": 3999.00,
        "category": "Home Decor",
        "stock": 18,
        "image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=500",
        "rating": 4.9,
        "review_count": 87
    },
    {
        "name": "Blue Pottery Tiles - Decorative Set",
        "description": "Set of 4 decorative blue pottery tiles from Jaipur. Can be used as wall art, trivets, or coasters. Each tile features unique hand-painted traditional patterns.",
        "price": 1199.00,
        "category": "Home Decor",
        "stock": 56,
        "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500",
        "rating": 4.5,
        "review_count": 201
    },
    {
        "name": "Longpi Black Pottery Coffee Mugs",
        "description": "Set of 2 sleek black pottery coffee mugs from Manipur. The minimalist design and smooth finish make them perfect for modern coffee lovers. Handcrafted using traditional techniques.",
        "price": 1299.00,
        "category": "Kitchenware",
        "stock": 48,
        "image_url": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=500",
        "rating": 4.6,
        "review_count": 172
    },
    {
        "name": "Matki Water Pot - Traditional with Modern Twist",
        "description": "Classic matki water pot with contemporary design elements. Made from natural clay, it naturally cools water. Features a modern spout design while maintaining traditional cooling properties.",
        "price": 1099.00,
        "category": "Kitchenware",
        "stock": 61,
        "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500",
        "rating": 4.7,
        "review_count": 234
    }
]


def populate_products():
    """Populate the database with modern Indian pottery products."""
    db: Session = SessionLocal()
    
    try:
        added_count = 0
        skipped_count = 0
        
        for product_data in PRODUCTS:
            # Check if product already exists
            existing_product = db.query(Product).filter(
                Product.name == product_data["name"]
            ).first()
            
            if existing_product:
                print(f"⏭️  Skipping '{product_data['name']}' - already exists")
                skipped_count += 1
                continue
            
            # Create new product
            product = Product(**product_data)
            db.add(product)
            added_count += 1
            print(f"✅ Added '{product_data['name']}' - ₹{product_data['price']}")
        
        db.commit()
        print(f"\n{'='*60}")
        print(f"✨ Database update complete!")
        print(f"   Added: {added_count} products")
        print(f"   Skipped: {skipped_count} products (already exist)")
        print(f"{'='*60}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Starting product database update...")
    print("📦 Adding modern Indian pottery products...\n")
    populate_products()

