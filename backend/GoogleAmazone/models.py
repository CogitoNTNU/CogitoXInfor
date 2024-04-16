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
    col = models.CharField("Col", max_length=100, db_index=True, help_text="Product ID of product to recommend for")
    row = models.CharField("Row", max_length=100, db_index=True, help_text="Product ID of product to compare with")
    title_similarity = models.FloatField("Title Cosine Similarity", default=0.0)
    description_similarity = models.FloatField("Description Cosine Similarity", default=0.0)

    class Meta:
        unique_together = ['col', 'row']
        indexes = [
            models.Index(fields=['col', 'row']),  # Compound index for quicker lookups on pairs
        ]

    def __str__(self) -> str:
        return f"Recommendation between {self.col} and {self.row}: Title Sim={self.title_similarity}, Desc Sim={self.description_similarity}"
