from django.http import HttpResponse
from django.shortcuts import render
from products.models import Product

from products.gets import *

# Create your views here.


def allproducts_view(request, *args, **kwargs):
    myContext = {
        "title": "Все товары",
        "products": [],
        "seeds": []
    }

    productRows, avProducts = getProductsRow()
    myContext["products"] = avProducts
    print(productRows)

    for avpr in avProducts:
        if avpr.category.lower() == "семена":
            myContext["seeds"].append(avpr)

    return render(request, "allproducts.html", myContext)


def homepage_view(request, *agrs, **kwargs):

    productsRows, categories = getProductsCatrows()

    myContext = {
        "title": "Главная",
        "categories": categories
    }

    myContext["products"] = productsRows

    return render(request, "home.html", myContext)


def products_view(request, *args, **kwargs):

    productsRows, categories = getProductsCatrows()

    myContext = {
        "title": "Товары",
        "categories": categories
    }

    myContext["products"] = productsRows

    print(myContext)

    return render(request, "products.html", myContext)


def productpage_view(request, *args, **kwargs):

    queryDict = request.GET

    if not request.method == "GET" or not 'article' in queryDict:
        return HttpResponse("Bad request!")

    try:
        requestedArticle = int(request.GET['article'])
        requestedObject = Product.objects.get(article=requestedArticle)
    except:
        return HttpResponse("Bad request!")

    return HttpResponse(str(requestedObject.title))
