from django.http import HttpResponse
from django.shortcuts import render
from products.models import Product

# Create your views here.
def products_view(request, *args, **kwargs):
    myContext = {
        "title": "Товары",
        "products": [],
        "seeds": []
    }

    avProducts = Product.objects.all()
    for pr in avProducts:
        if pr.isAvailable:
            myContext["products"].append(pr)

    for avpr in myContext["products"]:
        if avpr.category.lower() == "семена":
            myContext["seeds"].append(avpr)

    return render(request, "products.html", myContext)

def homepage_view(request, *agrs, **kwargs):
    myContext = {
        "title": "Главная",
        "products": [],
        "seeds": []
    }

    avProducts = Product.objects.all()
    for pr in avProducts:
        if pr.isAvailable:
            myContext["products"].append(pr)

    for avpr in myContext["products"]:
        if avpr.category.lower() == "семена":
            myContext["seeds"].append(avpr)

    return render(request, "home.html", myContext)