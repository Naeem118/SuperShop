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
    data={'categories':ans}
    return render(request,'pages/home.html',data)
