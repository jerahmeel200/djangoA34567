from django.core.management.base import BaseCommand
from shop.models import Product
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Seed the database with initial product data'

    def handle(self, *args, **kwargs):
        products = [
            {'name': 'Laptop', 'description': 'High-end laptop', 'price': 1299.99, 'stock': 10},
            {'name': 'Smartphone', 'description': 'Latest smartphone', 'price': 899.99, 'stock': 25},
            {'name': 'Headphones', 'description': 'Noise cancelling headphones', 'price': 199.99, 'stock': 50},
            {'name': 'Headphones', 'description': 'Noise cancelling headphones', 'price': 199.99, 'stock': 50},
            {'name': 'Headphones', 'description': 'Noise cancelling headphones', 'price': 199.99, 'stock': 50},
            {'name': 'Headphones', 'description': 'Noise cancelling headphones', 'price': 199.99, 'stock': 50},
            {'name': 'Headphones', 'description': 'Noise cancelling headphones', 'price': 199.99, 'stock': 50},
        ]

        for prod in products:
            try:
                product, created = Product.objects.get_or_create(
                    name=prod['name'],  # used as the lookup field
                    defaults={
                        'description': prod['description'],
                        'price': prod['price'],
                        'stock': prod['stock'],
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created: {product.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Already exists: {product.name}"))
            except IntegrityError as e:
                self.stderr.write(self.style.ERROR(f"Failed to add {prod['name']}: {e}"))

        self.stdout.write(self.style.SUCCESS('✅ Successfully seeded the database.'))
