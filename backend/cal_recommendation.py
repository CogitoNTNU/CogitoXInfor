import os
import django
import numpy as np

print("Test", flush=True)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cogitoXInfor.settings')
django.setup()

print("Test2", flush=True)

import csv
from GoogleAmazone.models import Recommendations, Products
from sentence_transformers import SentenceTransformer, util
import time
Recommendations.objects.all().delete()
print("Test3", flush=True)

# Add a recommendation calculation here to precompile recommendations 
# and add them to the database in the Recommendations table

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Test4", flush=True)

all_products = Products.objects.all()
print("All products = ", all_products, flush=True)

#numpy-optim metode
tic = time.time()
desc_matrix = np.zeros((len(all_products), len(model.encode("test")))) #rader, kolonner 
title_matrix = desc_matrix.copy()
id_array_to_identify = []

i = 0
for product in all_products:
    if product.title == "" or product.description == "":
        continue
    desc_matrix[i] = model.encode(product.description)
    #desc_matrix[i] *= (1/np.linalg.norm(desc_matrix[i])) #trenger ikke normalisere
    title_matrix[i] = model.encode(product.title)
    #title_matrix[i] *= (1/np.linalg.norm(title_matrix[i]))
    id_array_to_identify.append(product.id)
    i += 1 

desc_correlation = np.matmul(desc_matrix, desc_matrix.T)
title_correlation = np.matmul(title_matrix, title_matrix.T)
#total_weighted = 0.9*title_correlation + 0.1*desc_correlation
toc = time.time()
print(f"Tid brukt: ", toc-tic, flush=True)
#ferdig
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
    if product.title == "" or product.description == "":
        continue
    id_title_embed[product.id] = model.encode(product.title)
    id_desc_embed[product.id] = model.encode(product.description)





print("Begynner å embedde", flush=True)
# print("id_title_embed.items() = ", id_title_embed.items(), flush=True)
# print("id_desc_embed.items() = ", id_desc_embed.items(), flush=True)

# Compute the cosine similarity between the title and description of all pairs of products and store the results in dictionaries
i = 0
cos_sim_title = {}
for id1, title1 in list(id_title_embed.items()):
    for id2, title2 in list(id_title_embed.items()):
        i += 1
        print("Iterasjon (title): " + str(i), flush=True)
        if id1 != id2:
            if (id1, id2) not in cos_sim_title and (id2, id1) not in cos_sim_title:
                cos_sim_title[(id1, id2)] = util.cos_sim(title1, title2)

i = 0
cos_sim_desc = {}
for id1, desc1 in list(id_desc_embed.items()):
    for id2, desc2 in list(id_desc_embed.items()):
        i += 1
        print("Iterasjon (description): " + str(i), flush=True)
        if id1 != id2:
            if (id1, id2) not in cos_sim_desc and (id2, id1) not in cos_sim_desc:
                cos_sim_desc[(id1, id2)] = util.cos_sim(desc1, desc2)

combined_dict = {}

i = 0
for key, value in cos_sim_title.items():
    i += 1
    print("Iterasjon (combined): " + str(i), flush=True)
    if key in cos_sim_desc:
        combined_dict[key] = [value, cos_sim_desc[key]] # Struktur: (embedding title, embedding description)

i = 0
for pair, sim_title in list(combined_dict.items()):
    i += 1
    print("Iterasjon (save to db): " + str(i), flush=True)
    sim_combined = combined_dict[pair]

    recommendation = Recommendations(col=str(pair[0]), row=str(pair[1]), title_similarity=float(sim_combined[0]), description_similarity=float(sim_combined[1]))
    recommendation.save()

print("Recommendations saved to the database", flush=True)
# print("Cosine similarities titles = ", cos_sim_title, flush=True)
# print("", flush=True)
# print("Cosine similarities descriptions = ", cos_sim_desc, flush=True)
# print("", flush=True)


# print("Combined dictionary = ", combined_dict, flush=True)




