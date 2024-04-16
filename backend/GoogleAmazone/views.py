from django.shortcuts import render

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from sentence_transformers import SentenceTransformer
# Create your views here.
import pandas as pd
import numpy as np
# from openai import OpenAI
# import openai

from .models import Products, Recommendations
from .serializers import ProductsSerializer, GetRecommendationsOnProductSerializer, GetProductsSerializer, GetProductSerializer

@api_view(['GET'])
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
            products = Products.objects.filter(title__contains=search)[offset:offset+amount]
            responseSerializer = ProductsSerializer(products, many=True)
            return Response(responseSerializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
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

@api_view(['GET'])
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
            print("Selected product = ", product, flush=True)
            
            embeddings = Recommendations.objects.filter(col=id).values("row", "title_similarity", "description_similarity")[:5]
            # print("Embeddings = ", embeddings, flush=True)

            recommendations_dict = {}
            for product in embeddings:
                product_id = product["row"]
                title_similarity = product["title_similarity"]
                description_similarity = product["description_similarity"]
                recommendations_dict[product_id] = title_similarity*0.8 + description_similarity*0.2

            # Sort the recommendations by similarity
            recommendations_dict = dict(sorted(recommendations_dict.items(), key=lambda item: item[1], reverse=True))
            print("Recommendations dict = ", recommendations_dict, flush=True)

            # Get the top amount recommendations
            recommendations = Products.objects.filter(id__in=list(recommendations_dict.keys()))[:5]
            print("Recommendations = ", recommendations, flush=True)
            # print("Embeddings = ", embeddings, flush=True)
            # print("Embeddings[0] = ", embeddings[0], flush=True)

            responseSerializer = ProductsSerializer(recommendations, many=True)
            return Response(responseSerializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)