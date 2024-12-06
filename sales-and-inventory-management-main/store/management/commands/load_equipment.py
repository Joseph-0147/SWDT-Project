import csv
from django.core.management.base import BaseCommand
from store.models import Category, Item  # Adjust this based on where your models are defined
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Load construction equipment data from CSV into the database'

    def handle(self, *args, **kwargs):
        # Open and read the CSV file
        with open('construction_equipment.csv', mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Get or create the category
                category_name = row['category']
                category, created = Category.objects.get_or_create(name=category_name)
                
                # Try to create the item
                try:
                    Item.objects.create(
                        name=row['name'],
                        description=row['description'],
                        category=category,
                        quantity=int(row['quantity']),
                        price=float(row['price'])
                    )
                    self.stdout.write(self.style.SUCCESS(f"Successfully added item: {row['name']}"))

                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(f"Error adding item {row['name']}: {e}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Unexpected error with item {row['name']}: {e}"))
