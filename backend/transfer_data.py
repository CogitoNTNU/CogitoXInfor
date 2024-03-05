import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cogitoXInfor.settings')
django.setup()

import csv
from GoogleAmazone.models import Products

def import_products_from_csv(file_path):

    Products.objects.all().delete()

    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:

            product = Products.objects.create(
                id=row['id'],
                title=row['title'],
                price=float(row['price']),
                manufacturer=row['manufacturer'],
                description=row['description']
            )
            product.save()
            print(f"Product {product.title} has been created")
    print("All products have been imported")

csv_file_path = "./../data/Amazon.csv"
import_products_from_csv(csv_file_path)
