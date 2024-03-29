from importlib.resources import path
from django import views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('productsdata/', views.getJsonProductsData, name='productsdata'),
    path('productPhotosPath/<int:product_id>/', views.getJsonProductPhotosPath, name='productPhotosPath'),
    path('product-detail/<int:product_id>', views.product_detail, name='product-detail'),
    path('store/', views.store, name='store'),
    path('store/<str:prod_name>', views.store, name='store'),
    path('searchstore/<int:category_id>', views.searchstore, name='searchstore'),
    path('fetch_no_of_product_pics/<int:product_id>/', views.fetch_no_of_product_pics, name='fetch_no_of_product_pics'),
]
