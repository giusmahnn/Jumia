import random
from faker import Faker
from django.core.management.base import BaseCommand
from accounts.models import Account
from vendor.models import Vendor


class Command(BaseCommand):
    help = 'Create a new account and vendor'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(5):
            first_name = fake.unique.first_name()
            last_name = fake.unique.last_name()
            username = fake.unique.user_name()
            email = fake.unique.email()
            password = "SecurePassword!123"
            # Create the user account
            user = Account.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                first_name=first_name,
                last_name=last_name,
                profile_picture=fake.image_url(width=200, height=200),
                phone_number=fake.phone_number(),
                gender=random.choice(['Male', 'Female', 'Other']),
                date_of_birth=fake.date_of_birth(tzinfo=None),
                is_seller_user=True
            )

            # Create the vendor associated with the user
            vendor = Vendor.objects.create(
                user=user,
                store_logo=fake.image_url(),
                store_name=fake.company(),
                store_description=fake.text(max_nb_chars=200),
                phone_number=fake.phone_number(),
                nationality=fake.country(),
                state=fake.state(),
                city=fake.city(),
                address=fake.address()
            )
            vendor.save()

        # Output a success message indicating that the account and vendor were created successfully
        self.stdout.write(self.style.SUCCESS(f'Account "{user.username}" and Vendor "{vendor.store_name}" created successfully'))