from django.core.management.base import BaseCommand
from shop.models import Product

class Command(BaseCommand):
    help = 'Seed the database with initial products'

    def handle(self, *args, **kwargs):
        products = [
            {'name': 'Laptop', 'description': 'High-end laptop', 'price': 1299.99, 'stock': 10},
            {'name': 'Smartphone', 'description': 'Latest smartphone', 'price': 899.99, 'stock': 25},
            {'name': 'Headphones', 'description': 'Noise cancelling headphones', 'price': 199.99, 'stock': 50},
        ]
        for prod in products:
            Product.objects.get_or_create(**prod)
        self.stdout.write(self.style.SUCCESS('Database seeded with products.'))
