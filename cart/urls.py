from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('productsdata/', views.getJsonProductsData, name='productsdata'),
    path('productPhotosPath/<int:product_id>/', views.getJsonProductPhotosPath, name='productPhotosPath'),
] 