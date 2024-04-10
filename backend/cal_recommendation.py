import os
import django

print("Test", flush=True)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cogitoXInfor.settings')
django.setup()

print("Test2", flush=True)

import csv
from GoogleAmazone.models import Recommendations, Products
from sentence_transformers import SentenceTransformer, util

Recommendations.objects.all().delete()
print("Test3", flush=True)

# Add a recommendation calculation here to precompile recommendations 
# and add them to the database in the Recommendations table

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Test4", flush=True)

all_products = Products.objects.all()
# print("All products = ", all_products, flush=True)
product_titles = [product.title for product in all_products]
product_descriptions = [product.description for product in all_products]

# Matching product id's with product titles
id_title_embed = {}
id_desc_embed = {}
i = 0
print("All products length = ", len(all_products), flush=True)
for product in all_products:
    i += 1
    print(i, flush=True)
    id_title_embed[product.id] = model.encode(product.title)
    id_desc_embed[product.id] = model.encode(product.description)
    
print("Begynner å embedde", flush=True)
# print("id_title_embed.items() = ", id_title_embed.items(), flush=True)
# print("id_desc_embed.items() = ", id_desc_embed.items(), flush=True)

# Compute the cosine similarity between the title and description of all pairs of products and store the results in dictionaries
cos_sim_title = {}
for id1, title1 in list(id_title_embed.items()):
    for id2, title2 in list(id_title_embed.items()):
        if id1 != id2:
            if (id1, id2) not in cos_sim_title and (id2, id1) not in cos_sim_title:
                cos_sim_title[(id1, id2)] = util.cos_sim(title1, title2)

cos_sim_desc = {}
for id1, desc1 in list(id_desc_embed.items()):
    for id2, desc2 in list(id_desc_embed.items()):
        if id1 != id2:
            if (id1, id2) not in cos_sim_desc and (id2, id1) not in cos_sim_desc:
                cos_sim_desc[(id1, id2)] = util.cos_sim(desc1, desc2)

combined_dict = {}

for key, value in cos_sim_title.items():
    if key in cos_sim_desc:
        combined_dict[key] = (value + cos_sim_desc[key]) / 2

for pair, sim_title in list(combined_dict.items()):
    sim_combined = combined_dict[pair]

    recommendation = Recommendations(col=str(pair[0]), row=str(pair[1]), value=sim_combined)
    recommendation.save()

print("Recommendations saved to the database", flush=True)
# print("Cosine similarities titles = ", cos_sim_title, flush=True)
# print("", flush=True)
# print("Cosine similarities descriptions = ", cos_sim_desc, flush=True)
# print("", flush=True)


# print("Combined dictionary = ", combined_dict, flush=True)




