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

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')

# Initialize lemmatizer
# lemmatizer = WordNetLemmatizer()

# def preprocess_text(text):
#     # Convert text to lowercase
#     text = text.lower()
#     # Remove punctuation and special characters
#     text = re.sub(r'\W', ' ', text)
#     # Remove all single characters
#     text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
#     # Remove single characters from the start
#     text = re.sub(r'\^[a-zA-Z]\s+', ' ', text) 
#     # Replace multiple spaces with a single space
#     text = re.sub(r'\s+', ' ', text, flags=re.I)
#     # Removing digits or numbers
#     text = re.sub(r'\d', '', text)
#     # Lemmatization
#     tokens = text.split()
#     tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stopwords.words('english')]
#     return ' '.join(tokens)


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
            all_products = Products.objects.all()[:10]
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
            
            print("", flush=True)
            #Encoding titles of all other products and using cosine similarity (vectors)
            title_encoding = {}
            emb1 = model.encode(product.title)
            for title in product_titles:
                emb2 = model.encode(title)
                cos_sim = util.cos_sim(emb1, emb2)
                title_encoding[title] = cos_sim
            print("Title encoding = ", title_encoding, flush=True)

            # Encoding descriptions of all other products and using cosine similarity (vectors)
            desc_encoding = {}
            emb3 = model.encode(product.description)
            for desc in product_descriptions:
                emb4 = model.encode(desc)
                cos_sim = util.cos_sim(emb3, emb4)
                desc_encoding[desc] = cos_sim
            # print("Product descriptions = ", product_descriptions, flush=True)
            print("Description encoding = ", desc_encoding, flush=True)
            print("", flush=True)

            # Combining and taking the average of the two encodings
            combined_encoding = {}
            for title, cos_sim in title_encoding.items():
                id = [id for id, title2 in id_title.items() if title == title2][0]
                print("Current product ID = ", id, flush=True)
                desc = id_desc[id]
                print("Description of current product = ", desc, flush=True)
                combined_encoding[title] = (cos_sim + desc_encoding[desc]) / 2
            print("",flush=True)
            print("Combined encoding = ", combined_encoding, flush=True)
            

            # Sorting the combined encodings
            sorted_combined = sorted(combined_encoding.items(), key=lambda item: item[1], reverse=True)

            # Skip the first one (the product itself) and select the next top products
            top_products = [title for title, cos_sim in sorted_combined[1:amount]]

            # Get the top product IDs from the top products
            top_product_ids = [
                id for id, title in id_title.items() if title in top_products
            ]

            # Get the actual top products from the IDs
            top_products = Products.objects.filter(id__in=top_product_ids)
            print("Top products = ", top_products, flush=True)

            recommendations = top_products # Change this to the actual recommendations

            responseSerializer = ProductsSerializer(recommendations, many=True)
            return Response(responseSerializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
