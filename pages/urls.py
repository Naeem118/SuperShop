from importlib.resources import path
from django import views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('productsdata/', views.getJsonProductsData, name='productsdata'),
    path('productPhotosPath/<int:product_id>/', views.getJsonProductPhotosPath, name='productPhotosPath'),
]
