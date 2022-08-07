from django.shortcuts import render
from supershop import definitions
from django.db import connection
from django.http import JsonResponse

# Create your views here.

def home(request):
    cursor = connection.cursor()
    query = """SELECT CATEGORY_NAME, CATEGORY_ID FROM PRODUCT_CATEGORY"""
    cursor.execute(query)
    result = definitions.dictfetchall(cursor)
    #categories = [dict(category['CATEGORY_NAME'],category['CATEGORY_ID']]) for category in result]
    categories = {}
    for category in result:
        categories[category['CATEGORY_ID']] = category['CATEGORY_NAME']
    cursor.close()
    data = {
        'categories' : categories.items(),
    }
    return render(request,'pages/home.html', data)

def getProducts():
    cursor = connection.cursor()
    query = """SELECT PRODUCT_ID, PRODUCT_NAME, UNIT_ID, FOR_UNIT, STOCK_QUANTITY, OFFER_PCT, PRODUCT_PRICE, PRODUCT_RATING, CATEGORY_ID FROM PRODUCTS"""
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

def product_detail(request, product_id):
    cursor = connection.cursor()
    query = """SELECT PRODUCT_NAME, UNIT_ID, FOR_UNIT, STOCK_QUANTITY, 
                OFFER_PCT, PRODUCT_PRICE, PRODUCT_RATING, DESCRIPTION,
                CATEGORY_ID, EXPIRE_DATE
                FROM PRODUCTS WHERE PRODUCT_ID=%s"""
    cursor.execute(query, [str(product_id)])
    result = definitions.dictfetchone(cursor)
    # name = result["PRODUCT_NAME"]
    # offer = result["OFFER_PCT"]
    unit=""
    if(result["UNIT_ID"]==1):
        unit='kg'
    elif(result["UNIT_ID"]==2): 
        unit = 'pc'
    elif(result["UNIT_ID"]==3):
        unit = 'litre'
    
    stock = str(result["STOCK_QUANTITY"]) + " " + unit
    price = 'Tk. ' + str(result["PRODUCT_PRICE"]) + ' / ' + str(result["FOR_UNIT"]) + " " + unit
    # rating = result["PRODUCT_RATING"]
    # description = result["DESCRIPTION"]
    # exp_date = result["EXPIRE_DATE"]
    
    query = """SELECT CATEGORY_NAME FROM PRODUCT_CATEGORY WHERE CATEGORY_ID=%s"""
    cursor.execute(query, [result["CATEGORY_ID"]])
    result_cat = definitions.dictfetchone(cursor)
    category_name = result_cat["CATEGORY_NAME"]
    query = """SELECT PATH FROM PRODUCT_PHOTOS_PATH WHERE PRODUCT_ID=%s"""
    cursor.execute(query,[product_id])
    result_photos = cursor.fetchall()
    photos_path = [photo[0] for photo in result_photos]
    
    query = """SELECT FIRST_NAME, REVIEW, 
            PROFILE_PIC, REVIEW_DATE
            FROM PRODUCT_REVIEW JOIN USERS USING(USER_ID)
            WHERE PRODUCT_ID = %s AND REVIEW IS NOT NULL;"""
    cursor.execute(query, [product_id])
    reviews = definitions.dictfetchall(cursor)
    
    data = {
        #'product_name': name,
        'product_category': category_name,
        'product_stock': stock,
        #'product_offer': offer,
        'product_price': price,
        #'product_rating': rating,
        #'product_desc': description,
        #'product_exp': exp_date,
        'product' : result,
        'photos': photos_path,
        'reviews': reviews,
    }
    return render(request, 'pages/product-detail.html', data)

def store(request, prod_name=None):
    cursor = connection.cursor()
    query = """SELECT CATEGORY_NAME, CATEGORY_ID FROM PRODUCT_CATEGORY"""
    cursor.execute(query)
    result = definitions.dictfetchall(cursor)
    #categories = [dict(category['CATEGORY_NAME'],category['CATEGORY_ID']]) for category in result]
    categories = {}
    for category in result:
        categories[category['CATEGORY_ID']] = category['CATEGORY_NAME']
    cursor.close()
    if(prod_name!=None):
        data = {
            'prod_name': prod_name,
            'categories' : categories.items(),
        }
    else:
        data = {
            'prod_name': " ",
            'categories' : categories.items(),
        }
    return render(request, 'pages/store.html', data)

def searchstore(request, category_id):
    cursor = connection.cursor()
    query = """SELECT CATEGORY_NAME, CATEGORY_ID FROM PRODUCT_CATEGORY"""
    cursor.execute(query)
    result = definitions.dictfetchall(cursor)
    #categories = [dict(category['CATEGORY_NAME'],category['CATEGORY_ID']]) for category in result]
    categories = {}
    for category in result:
        categories[category['CATEGORY_ID']] = category['CATEGORY_NAME']
    cursor.close()
    data = {
            'category_id': category_id,
            'categories' : categories.items(),
        }
    print(category_id)
    return render(request, 'pages/store_category.html', data)