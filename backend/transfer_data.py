import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cogitoXInfor.settings')
django.setup()

import csv
from itertools import islice
from GoogleAmazone.models import Products

def import_products_from_csv(file_path):

    Products.objects.all().delete()

    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in islice(csv_reader, 2000):

            price = row['price'].replace('£', '').strip()
            try:
                price = float(price)
            except ValueError:
                price = -1

            product = Products.objects.create(
                id=row['uniq_id'],
                title=row['product_name'],
                price=price,
                manufacturer=row['manufacturer'],
                description=row['product_description']
            ) 
            product.save()
            print(f"Product {product.title} has been created")
    print("2000 products have been imported")

csv_file_path = "./../data/better_dataset_toys.csv"
import_products_from_csv(csv_file_path)
