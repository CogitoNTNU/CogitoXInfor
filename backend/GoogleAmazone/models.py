from django.db import models
from sentence_transformers import SentenceTransformer
import numpy as np
# Create your models here.
class Products(models.Model):
    id = models.CharField("ID", default="",max_length=100, primary_key=True)
    title = models.CharField("Title", default="",max_length=256)
    price = models.FloatField("Price", default=0)
    manufacturer = models.CharField("Manufacturer", default="",max_length=256)
    description = models.TextField("Description", default="")

    def __str__(self) -> str:
        return self.title
    
class Recommendations(models.Model):
    id = models.CharField("ID", default="",max_length=100, primary_key=True)
    def recommend(self) -> str:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        print("init into the recommentadion", flush=True)
        other_Products = Products.objects.all(self.id != id)
        array_embeddings = np.zeros(len(other_Products))
        array_embeddings = model.encode(other_Products)
        for i in range(len(other_Products)):
            array_embeddings[i] = model.encode(other_Products[i].description)
            print(array_embeddings[i], flush=True)
        return self.title