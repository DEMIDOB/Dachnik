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


