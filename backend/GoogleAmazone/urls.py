"""
URL configuration for cogitoXInfor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
"""
from django.urls import path
from .views import GetProducts, GetRecommendationsOnProduct

# TODO Add uls here to the different parts functions of the project
urlpatterns = [
    path("products", GetProducts, name="GetProducts"),
    path("recommendations", GetRecommendationsOnProduct, name="GetRecommendationsOnProduct"),
]
