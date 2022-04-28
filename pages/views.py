from django.db import connection
from django.shortcuts import render
from django.db import connection
from supershop import definitions
# Create your views here.
def home(request):
    cursor=connection.cursor()
    query="""select CATEGORY_NAME from product_category"""
    cursor.execute(query)
    result=definitions.dictfetchall(cursor)
    ans=[ x['CATEGORY_NAME'] for x in result ]
    query="""select PRODUCT_NAME, UNIT_ID, STOCK_QUANTITY, PRODUCT_PRICE, OFFER_PCT, PRODUCT_RATING from products WHERE PRODUCT_ID=%s"""
    cursor.execute(query,[str(1)])
    result=definitions.dictfetchone(cursor)
    name=result['PRODUCT_NAME']
    unit=result['UNIT_ID']
    if(unit==1):
        unit='kg'
    elif(unit==2):
        unit='piece'
    stock=result['STOCK_QUANTITY']
    price=result['PRODUCT_PRICE']
    offer_pct=result['OFFER_PCT']
    rating=result['PRODUCT_RATING']
    query="""select PATH from product_photos_path where PRODUCT_ID=%s"""
    cursor.execute(query,[str(1)])
    result=cursor.fetchall()
    photos_path=[dict[0] for dict in result]
    data={
        'categories':ans,
        'photos':photos_path,
        'name': name,
        'price':price,
        'unit':unit,
        'stock':stock,
        'offer_pct':offer_pct,
        'rating':rating,
    }
    return render(request,'pages/home.html',data)
