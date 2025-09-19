from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Order, OrderItem, Product, Cart, CartItem
import random

class Command(BaseCommand):
    help = 'Creates test orders for demonstration'

    def handle(self, *args, **options):
        self.stdout.write('Creating test orders...')

        # Get some products
        products = Product.objects.all()[:5]
        if not products:
            self.stdout.write(self.style.ERROR('No products found. Please run populate_data first.'))
            return

        # Create a test user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write('Created test user: testuser / testpass123')

        # Create some test orders
        order_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
        
        for i in range(10):
            # Create order
            order = Order.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                address=f'{random.randint(100, 9999)} Main Street',
                postal_code=f'{random.randint(10000, 99999)}',
                city=random.choice(cities),
                status=random.choice(order_statuses)
            )
            
            # Add 1-3 random products to the order
            num_items = random.randint(1, 3)
            selected_products = random.sample(list(products), min(num_items, len(products)))
            
            for product in selected_products:
                quantity = random.randint(1, 3)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=quantity
                )
            
            self.stdout.write(f'Created order #{order.id} with {order.items.count()} items')

        self.stdout.write(self.style.SUCCESS(f'Successfully created {Order.objects.count()} test orders!'))
        self.stdout.write(f'Total orders: {Order.objects.count()}')
        self.stdout.write(f'Total order items: {OrderItem.objects.count()}')
