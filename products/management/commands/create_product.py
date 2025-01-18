import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Product
from vendor.models import Vendor
from products.choices import Category

class Command(BaseCommand):
    help = 'Create 100 random products for a vendor'

    def add_arguments(self, parser):
        parser.add_argument('vendor_id', type=int, help='ID of the vendor')

    def handle(self, *args, **kwargs):
        vendor_id = kwargs['vendor_id']
        fake = Faker()

        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Vendor with ID {vendor_id} does not exist'))
            return

        categories = [choice[0] for choice in Category.choices]

        for _ in range(100):
            name = fake.unique.word().capitalize()
            product = Product(
                vendor=vendor,
                name=name,
                slug=slugify(name),
                category=random.choice(categories),
                description=fake.text(max_nb_chars=200),
                price=round(random.uniform(10.0, 1000.0), 2),
                discount_price=round(random.uniform(5.0, 500.0), 2) if random.choice([True, False]) else None,
                quantity=random.randint(1, 100)
            )
            product.save()
            self.stdout.write(self.style.SUCCESS(f'Product "{product.name}" created successfully'))

        self.stdout.write(self.style.SUCCESS('100 products created successfully'))