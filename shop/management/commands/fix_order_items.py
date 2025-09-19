from django.core.management.base import BaseCommand
from django.db import models
from shop.models import OrderItem

class Command(BaseCommand):
    help = 'Fix OrderItem records with None price or quantity values'

    def handle(self, *args, **options):
        self.stdout.write('Checking for OrderItem records with None values...')
        
        # Find OrderItems with None price
        none_price_items = OrderItem.objects.filter(price__isnull=True)
        if none_price_items.exists():
            self.stdout.write(f'Found {none_price_items.count()} items with None price')
            for item in none_price_items:
                if item.product:
                    item.price = item.product.price
                    item.save()
                    self.stdout.write(f'Fixed OrderItem {item.id}: set price to {item.price}')
        
        # Find OrderItems with None quantity
        none_quantity_items = OrderItem.objects.filter(quantity__isnull=True)
        if none_quantity_items.exists():
            self.stdout.write(f'Found {none_quantity_items.count()} items with None quantity')
            for item in none_quantity_items:
                item.quantity = 1  # Default quantity
                item.save()
                self.stdout.write(f'Fixed OrderItem {item.id}: set quantity to {item.quantity}')
        
        # Check for any remaining issues
        problematic_items = OrderItem.objects.filter(
            models.Q(price__isnull=True) | models.Q(quantity__isnull=True)
        )
        
        if problematic_items.exists():
            self.stdout.write(self.style.ERROR(f'Still have {problematic_items.count()} problematic items'))
        else:
            self.stdout.write(self.style.SUCCESS('All OrderItem records are now valid!'))
