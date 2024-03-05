from rest_framework import serializers
from .models import Products

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class GetRecommendationsOnProductSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=100, help_text="Product ID to be used to get recommendations on it.")
    amount = serializers.IntegerField(help_text="Amount of recommendations to be returned.", default=5)

class GetProductsSerializer(serializers.Serializer):
    amount = serializers.IntegerField(help_text="Amount of products to be returned.", default=20)
    search = serializers.CharField(help_text="Search string to be used to filter products.", default="")
    offset = serializers.IntegerField(help_text="Offset of products to be returned.", default=0)

class GetProductSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=100, help_text="Product ID to get the product details.")