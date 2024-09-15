from django.shortcuts import render
import os
import requests
from dotenv import load_dotenv

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from .models import Products, Recommendations
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

            # Get the picture of the products
            # Turned of this because of the rate limit of the API and the time of each search was to long for the user
            # new_products = [GetProductPicture(product) for product in products]

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

            # Get the picture of the product
            new_product = GetProductPicture(product)

            responseSerializer = ProductsSerializer(new_product, many=False)
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
            # all_products = Products.objects.all() # TODO: Take manufacturer and price into account as well
            print("Selected product = ", product, flush=True)

            embeddings = Recommendations.objects.filter(col=id).values(
                "row", "title_similarity", "description_similarity"
            )

            recommendations_dict = {}
            for product in embeddings:
                product_id = product["row"]
                title_similarity = product["title_similarity"]
                description_similarity = product["description_similarity"]
                recommendations_dict[product_id] = (
                    title_similarity * 0.9 + description_similarity * 0.1
                )

            # Sort the recommendations by similarity and get the 5 most similar products
            sorted_recommendation_dict = sorted(
                recommendations_dict.items(), key=lambda item: item[1], reverse=True
            )[:5]
            sorted_ids = [item[0] for item in sorted_recommendation_dict]

            # Fetch the top recommended products directly in order of their similarity
            recommendations = Products.objects.filter(id__in=sorted_ids)
            recommendations = sorted(
                recommendations, key=lambda x: recommendations_dict[x.id], reverse=True
            )

            # Get the picture of the products
            new_recommendations = [
                GetProductPicture(product) for product in recommendations
            ]
            print(
                f"Image for {new_recommendations[0].title} = {new_recommendations[0].picture}",
                flush=True,
            )

            responseSerializer = ProductsSerializer(new_recommendations, many=True)
            return Response(responseSerializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Helper function to get the pictures to the products
def GetProductPicture(product: Products):
    default_image = "https://www.pinclipart.com/picdir/middle/205-2052870_caution-cartoon-png-clipart.png"
    if not product.picture or product.picture == default_image:
        new_image = _find_image_google_cse(product.title)
        product.picture = new_image
        product.save()
    else:
        product.picture = default_image
    return product


import requests
import os


def _find_image_google_cse(product_title: str) -> str:
    api_key = os.getenv("GOOGLE_CSE_API_KEY")
    search_engine_id = os.getenv("GOOGLE_CSE_ID") 

    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": product_title,
        "cx": search_engine_id,
        "key": api_key,
        "searchType": "image",  # This makes it an image search
        "num": 1,  # Limit to 1 image
    }

    response = requests.get(search_url, params=params)
    try:
        response.raise_for_status()
    except Exception as e:
        print(f"Error in find_image_google_cse (quote exceeded): {e}", flush=True)
        return "https://www.pinclipart.com/picdir/middle/205-2052870_caution-cartoon-png-clipart.png"  # Fallback image
    search_results = response.json()

    if "items" in search_results and len(search_results["items"]) > 0:
        return search_results["items"][0]["link"]  # Return the first image URL
    return "https://www.pinclipart.com/picdir/middle/205-2052870_caution-cartoon-png-clipart.png"  # Fallback image