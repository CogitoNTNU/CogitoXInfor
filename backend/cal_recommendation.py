import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cogitoXInfor.settings')
django.setup()

from GoogleAmazone.models import Recommendations, Products
from sentence_transformers import SentenceTransformer, util

import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

# Empty the Recommendations table
Recommendations.objects.all().delete()

model = SentenceTransformer("all-MiniLM-L6-v2")

all_products = Products.objects.all()

# Matching product id's with product titles and descriptions
id_title_embed = {}
id_desc_embed = {}
i = 0
for product in all_products:
    i += 1
    print("Embedding product number: " + i, flush=True)
    if product.title == "" or product.description == "":
        continue
    id_title_embed[product.id] = model.encode(product.title)
    id_desc_embed[product.id] = model.encode(product.description)
    
# Compute the cosine similarity between the title and description of all pairs of products and store the results in two distinct dictionaries
i = 0
cos_sim_title = {}
for id1, title1 in list(id_title_embed.items()):
    for id2, title2 in list(id_title_embed.items()):
        i += 1
        print("Iterasjon (title): " + str(i), flush=True)
        if id1 != id2:
            try:
                if (id1, id2) not in cos_sim_title and (id2, id1) not in cos_sim_title:
                    cos_sim_title[(id1, id2)] = util.cos_sim(title1, title2)
            except: 
                print("Error with product-pair: " + id1 + "," + id2, flush=True)

i = 0
cos_sim_desc = {}
for id1, desc1 in list(id_desc_embed.items()):
    for id2, desc2 in list(id_desc_embed.items()):
        i += 1
        print("Iterasjon (description): " + str(i), flush=True)
        if id1 != id2:
            try: 
                if (id1, id2) not in cos_sim_desc and (id2, id1) not in cos_sim_desc:
                    cos_sim_desc[(id1, id2)] = util.cos_sim(desc1, desc2)
            except:
                print("Error with product-pair: " + id1 + "," + id2, flush=True)

combined_dict = {}

# Create a dictionary with the combined cosine similarities of the title and description embeddings
i = 0
for key, value in cos_sim_title.items():
    i += 1
    print("Iterasjon (combined): " + str(i), flush=True)
    if key in cos_sim_desc:
        combined_dict[key] = [value, cos_sim_desc[key]] # Struktur: (embedding title, embedding description)

# Save the recommendations to the database
i = 0
for pair, sim_title in list(combined_dict.items()):
    i += 1
    print("Iterasjon (save to db): " + str(i), flush=True)
    sim_combined = combined_dict[pair]

    recommendation = Recommendations(col=str(pair[0]), row=str(pair[1]), title_similarity=float(sim_combined[0]), description_similarity=float(sim_combined[1]))
    recommendation.save()

print("Recommendations saved to the database", flush=True)