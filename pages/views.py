from django.shortcuts import render
from supershop import definitions
from django.db import connection
from django.http import JsonResponse

# Create your views here.

def home(request):
    cursor = connection.cursor()
    query = """SELECT CATEGORY_NAME FROM PRODUCT_CATEGORY"""
    cursor.execute(query)
    result = definitions.dictfetchall(cursor)
    categories = [category['CATEGORY_NAME'] for category in result]
    cursor.close()
    data = {
        'categories' : categories,
    }
    return render(request,'pages/home.html', data)

def getProducts():
    cursor = connection.cursor()
    query = """SELECT PRODUCT_ID, PRODUCT_NAME, UNIT_ID, FOR_UNIT, STOCK_QUANTITY, OFFER_PCT, PRODUCT_PRICE, PRODUCT_RATING FROM PRODUCTS"""
    cursor.execute(query)
    result = definitions.dictfetchall(cursor)
    cursor.close()
    return result

def getJsonProductsData(request):
    products = getProducts()
    return JsonResponse({'data': products})

def getJsonProductPhotosPath(request, product_id):
    cursor = connection.cursor()
    query = """SELECT PATH FROM PRODUCT_PHOTOS_PATH WHERE PRODUCT_ID=%s"""
    cursor.execute(query, [product_id])
    result = definitions.dictfetchall(cursor)
    return JsonResponse({'paths':result})