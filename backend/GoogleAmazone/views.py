from django.shortcuts import render

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

# Create your views here.

from .models import Products
from .serializers import (
    ProductsSerializer,
    GetRecommendationsOnProductSerializer,
    GetProductsSerializer,
    GetProductSerializer,
)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def GetProducts(request):
    """
    Get products from the database
    """
    try:
        serializer = GetProductsSerializer(data=request.query_params)
        if serializer.is_valid():
            amount = serializer.validated_data.get("amount")
            search = serializer.validated_data.get("search")
            offset = serializer.validated_data.get("offset")
            products = Products.objects.filter(title__contains=search)[
                offset : offset + amount
            ]
            responseSerializer = ProductsSerializer(products, many=True)
            return Response(responseSerializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def GetProduct(request):
    """
    Get products from the database
    """
    try:
        serializer = GetProductSerializer(data=request.query_params)
        if serializer.is_valid():
            id = serializer.validated_data.get("id")
            product = Products.objects.get(id=id)
            responseSerializer = ProductsSerializer(product, many=False)
            return Response(responseSerializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def GetRecommendationsOnProduct(request):
    """
    Get recommendations on a product
    """
    try:
        serializer = GetRecommendationsOnProductSerializer(data=request.query_params)
        if serializer.is_valid():
            id = serializer.validated_data.get("id")
            amount = serializer.validated_data.get("amount")
            product = Products.objects.get(id=id)
            # TODO: Add a recommendation algorithm here!!!
            all_products = Products.objects.all()
            product_descriptions = [product.description for product in all_products]
            print("Selected product = ", product, flush=True)
            id_desc = {}
            for product in all_products:
                id_desc[product.id] = product.description
            # print("id_desc = ", id_desc, flush=True)

            desc_encoding = {}

            emb1 = model.encode(product.description)
            for desc in product_descriptions:
                emb2 = model.encode(desc)
                cos_sim = util.cos_sim(emb1, emb2)
                desc_encoding[desc] = cos_sim

            # print("test", flush=True)
            # print("Desc_encoding = ", desc_encoding, flush=True)

            sorted_desc_encoding = dict(
                sorted(desc_encoding.items(), key=lambda item: item[1], reverse=True)
            )

            # print("Sorted = ", sorted_desc_encoding, flush=True)

            sorted_products = sorted(
                sorted_desc_encoding.items(), key=lambda item: item[1], reverse=True
            )

            # Skip the first one (the product itself) and get the next 5 products
            top_descriptions = [desc for desc, cos_sim in sorted_products[1:6]]
            # print("Top descriptions =", top_descriptions, flush=True)

            # Get the top product IDs from the top descriptions
            top_product_ids = [
                id for id, desc in id_desc.items() if desc in top_descriptions
            ]

            # Retrieve the top products based on the IDs
            top_products = Products.objects.filter(id__in=top_product_ids)

            print("Top products = ", top_products, flush=True)

            # print(product_descriptions)
            # embeddings = model.encode(product_descriptions)

            recommendations = top_products  # Change this to the actual recommendations

            responseSerializer = ProductsSerializer(recommendations, many=True)
            return Response(responseSerializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
