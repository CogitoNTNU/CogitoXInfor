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