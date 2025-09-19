from django.core.management.base import BaseCommand
from shop.models import Category, Product

class Command(BaseCommand):
    help = 'Populate the database with sample data for the e-commerce PoC'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {
                'name': 'Electronics',
                'slug': 'electronics',
                'description': 'Latest electronic gadgets and devices'
            },
            {
                'name': 'Clothing',
                'slug': 'clothing',
                'description': 'Fashion and apparel for all seasons'
            },
            {
                'name': 'Home & Garden',
                'slug': 'home-garden',
                'description': 'Everything for your home and garden'
            },
            {
                'name': 'Sports',
                'slug': 'sports',
                'description': 'Sports equipment and fitness gear'
            },
            {
                'name': 'Books',
                'slug': 'books',
                'description': 'Books for all ages and interests'
            }
        ]
        
        created_categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            created_categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create products
        products_data = [
            # Electronics
            {
                'name': 'Wireless Bluetooth Headphones',
                'slug': 'wireless-bluetooth-headphones',
                'description': 'High-quality wireless headphones with noise cancellation and 30-hour battery life.',
                'short_description': 'Premium wireless headphones with noise cancellation',
                'price': 199.99,
                'stock': 50,
                'is_featured': True,
                'category_slug': 'electronics'
            },
            {
                'name': 'Smartphone 128GB',
                'slug': 'smartphone-128gb',
                'description': 'Latest generation smartphone with advanced camera system and all-day battery.',
                'short_description': 'Latest generation smartphone with advanced features',
                'price': 699.99,
                'stock': 25,
                'is_featured': True,
                'category_slug': 'electronics'
            },
            {
                'name': 'Laptop Computer',
                'slug': 'laptop-computer',
                'description': 'High-performance laptop perfect for work and entertainment.',
                'short_description': 'High-performance laptop for work and play',
                'price': 1299.99,
                'stock': 15,
                'is_featured': True,
                'category_slug': 'electronics'
            },
            # Clothing
            {
                'name': 'Cotton T-Shirt',
                'slug': 'cotton-t-shirt',
                'description': 'Comfortable 100% cotton t-shirt available in multiple colors.',
                'short_description': 'Comfortable 100% cotton t-shirt',
                'price': 24.99,
                'stock': 100,
                'is_featured': False,
                'category_slug': 'clothing'
            },
            {
                'name': 'Denim Jeans',
                'slug': 'denim-jeans',
                'description': 'Classic fit denim jeans made from premium denim fabric.',
                'short_description': 'Classic fit premium denim jeans',
                'price': 79.99,
                'stock': 75,
                'is_featured': True,
                'category_slug': 'clothing'
            },
            # Home & Garden
            {
                'name': 'Coffee Maker',
                'slug': 'coffee-maker',
                'description': 'Programmable coffee maker with built-in grinder and thermal carafe.',
                'short_description': 'Programmable coffee maker with grinder',
                'price': 149.99,
                'stock': 30,
                'is_featured': False,
                'category_slug': 'home-garden'
            },
            {
                'name': 'Garden Tools Set',
                'slug': 'garden-tools-set',
                'description': 'Complete set of professional garden tools for all your gardening needs.',
                'short_description': 'Complete professional garden tools set',
                'price': 89.99,
                'stock': 40,
                'is_featured': False,
                'category_slug': 'home-garden'
            },
            # Sports
            {
                'name': 'Yoga Mat',
                'slug': 'yoga-mat',
                'description': 'Non-slip yoga mat perfect for yoga, pilates, and other exercises.',
                'short_description': 'Non-slip yoga mat for all exercises',
                'price': 39.99,
                'stock': 60,
                'is_featured': False,
                'category_slug': 'sports'
            },
            {
                'name': 'Running Shoes',
                'slug': 'running-shoes',
                'description': 'Lightweight running shoes with excellent cushioning and support.',
                'short_description': 'Lightweight running shoes with cushioning',
                'price': 129.99,
                'stock': 45,
                'is_featured': True,
                'category_slug': 'sports'
            },
            # Books
            {
                'name': 'Programming Guide',
                'slug': 'programming-guide',
                'description': 'Comprehensive guide to modern programming techniques and best practices.',
                'short_description': 'Comprehensive programming guide',
                'price': 49.99,
                'stock': 80,
                'is_featured': False,
                'category_slug': 'books'
            },
            {
                'name': 'Cookbook Collection',
                'slug': 'cookbook-collection',
                'description': 'Beautiful cookbook with recipes from around the world.',
                'short_description': 'Beautiful international cookbook',
                'price': 34.99,
                'stock': 55,
                'is_featured': False,
                'category_slug': 'books'
            },
            # Additional featured products
            {
                'name': 'Smart Watch',
                'slug': 'smart-watch',
                'description': 'Advanced smartwatch with health monitoring and GPS capabilities.',
                'short_description': 'Advanced smartwatch with health monitoring',
                'price': 299.99,
                'stock': 35,
                'is_featured': True,
                'category_slug': 'electronics'
            },
            {
                'name': 'Winter Jacket',
                'slug': 'winter-jacket',
                'description': 'Warm and stylish winter jacket perfect for cold weather.',
                'short_description': 'Warm and stylish winter jacket',
                'price': 159.99,
                'stock': 20,
                'is_featured': True,
                'category_slug': 'clothing'
            }
        ]
        
        for product_data in products_data:
            category = next(cat for cat in created_categories if cat.slug == product_data['category_slug'])
            product_data.pop('category_slug')
            product_data['category'] = category
            
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
        self.stdout.write(f'Created {len(created_categories)} categories and {len(products_data)} products.')
