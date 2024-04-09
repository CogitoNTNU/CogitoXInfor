from django.db import models

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
    col = models.CharField("Col", default="", help_text="Column name", db_index=True, max_length=256)
    row = models.CharField("Row", default="", help_text="Column name", db_index=True, max_length=256)
    value = models.FloatField("Value", default=0, help_text="Value of the recommendation")

    class Meta:
        unique_together = ['col', 'row']

    def __str__(self) -> float:
        return self.value