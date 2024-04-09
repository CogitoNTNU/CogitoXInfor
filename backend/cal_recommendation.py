import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cogitoXInfor.settings')
django.setup()

import csv
from GoogleAmazone.models import Recommendations, Products
from sentence_transformers import SentenceTransformer, util

# Add a recommendation calculation here to precompile recommendations 
# and add then to the database in the Recommendations table

model = SentenceTransformer("all-MiniLM-L6-v2")

all_products = Products.objects.all()
product_titles = [product.title for product in all_products]
product_descriptions = [product.description for product in all_products]

# Matching product id's with product titles
id_title = {}
id_desc = {}
for product in all_products:
    id_title[product.id] = model.encode(product.title)
    id_desc[product.id] = model.encode(product.description)
    
#Vi kom så langt! jeg la til dette for å teste  


# print("id_desc = ", id_desc, flush=True)
    
# EMBEDDING ============================================================================================================

print("", flush=True)
#Encoding titles of all other products and using cosine similarity (vectors)
title_encoding = {}
emb1 = model.encode(product.title)
for title in product_titles:
    emb2 = model.encode(title)
    cos_sim = util.cos_sim(emb1, emb2)
    title_encoding[title] = cos_sim
print("Title encoding = ", title_encoding, flush=True)

# Encoding descriptions of all other products and using cosine similarity (vectors)
desc_encoding = {}
emb3 = model.encode(product.description)
for desc in product_descriptions:
    emb4 = model.encode(desc)
    cos_sim = util.cos_sim(emb3, emb4)
    desc_encoding[desc] = cos_sim
# print("Product descriptions = ", product_descriptions, flush=True)
print("Description encoding = ", desc_encoding, flush=True)
print("", flush=True)

# Combining and taking the average of the two encodings
combined_encoding = {}
for title, cos_sim in title_encoding.items():
    id = [id for id, title2 in id_title.items() if title == title2][0]
    print("Current product ID = ", id, flush=True)
    desc = id_desc[id]
    print("Description of current product = ", desc, flush=True)
    combined_encoding[title] = (cos_sim + desc_encoding[desc]) / 2
print("",flush=True)
print("Combined encoding = ", combined_encoding, flush=True)


# Sorting the combined encodings
sorted_combined = sorted(combined_encoding.items(), key=lambda item: item[1], reverse=True)

# Skip the first one (the product itself) and select the next top products
top_products = [title for title, cos_sim in sorted_combined[1:amount]]

# Get the top product IDs from the top products
top_product_ids = [
    id for id, title in id_title.items() if title in top_products
]

# Get the actual top products from the IDs
top_products = Products.objects.filter(id__in=top_product_ids)
print("Top products = ", top_products, flush=True)  