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
            all_products = Products.objects.all()[:500]
            product_titles = [product.title for product in all_products]
            product_descriptions = [product.description for product in all_products]
            print("Selected product = ", product, flush=True)

            # Matching product id's with product titles
            id_title = {}
            for product in all_products:
                id_title[product.id] = product.title

            # Matching product id's with product descriptions
            id_desc = {}
            for product in all_products:
                id_desc[product.id] = product.description
            # print("id_desc = ", id_desc, flush=True)
                
            # EMBEDDING ============================================================================================================
                
            #Encoding titles of all other products and using cosine similarity (vectors)
            title_encoding = {}
            emb1 = model.encode(product.title)
            for title in product_titles:
                emb2 = model.encode(title)
                cos_sim = util.cos_sim(emb1, emb2)
                title_encoding[title] = cos_sim

            # Encoding descriptions of all other products and using cosine similarity (vectors)
            desc_encoding = {}
            emb3 = model.encode(product.description)
            for desc in product_descriptions:
                emb4 = model.encode(desc)
                cos_sim = util.cos_sim(emb3, emb4)
                desc_encoding[desc] = cos_sim

            # 

            # TITLES ============================================================================================================
                
            # Sort the encoded titles by cosine similarity
            # sorted_titles = sorted(title_encoding.items(), key=lambda item: item[1], reverse=True)

            # # Skip the first one (the product itself) and select the next top titles
            # top_titles = [title for title, cos_sim in sorted_titles[1:amount]]

            # # Get the top product IDs from the top titles
            # top_product_ids_for_titles = [
            #     id for id, title in id_title.items() if title in top_titles
            # ]

            # DESCRIPTIONS ============================================================================================================

            # Connecting the top descriptions to their respective products
            # sorted_descriptions = sorted(
            #     desc_encoding.items(), key=lambda item: item[1], reverse=True
            # )
            # # print("Sorted descriptions = ", sorted_descriptions, flush=True)

            # # Skip the first one (the product itself) and get the next 5 products
            # top_descriptions = [desc for desc, cos_sim in sorted_descriptions[1:6]]
            # # print("Top descriptions =", top_descriptions, flush=True)

            # # Get the top product IDs from the top descriptions
            # top_product_ids = [
            #     id for id, desc in id_desc.items() if desc in top_descriptions
            # ]

            # Retrieve the top products based on the IDs
            top_products_descriptions = Products.objects.filter(id__in=top_product_ids)

            # COMBINING TITLES AND DESCRIPTIONS =========================================================================================



            recommendations = None  # Change this to the actual recommendations

            responseSerializer = ProductsSerializer(recommendations, many=True)
            return Response(responseSerializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
