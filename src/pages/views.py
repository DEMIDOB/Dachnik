from django.http import HttpResponse
from django.shortcuts import render
from products.models import Product

from decimal import Decimal

def getProductsRow():
    allProducts = Product.objects.all()
    avProducts = []
    for pr in allProducts:
        if pr.isAvailable:
            newPrice = Decimal("{:.2f}".format(pr.price - pr.price*pr.discount/100))
            pr.price = newPrice
            avProducts.append(pr)

    productRows = []
    stillMoreProducts = True
    for i in range(0, len(avProducts), 3):
        print(i)
        if not stillMoreProducts:
            break
        productRows.append([])
        for j in range(3):
            try:
                productRows[i//3].append(avProducts[i + j])
            except IndexError:
                stillMoreProducts = False
                break
    return productRows, avProducts

# Create your views here.
def products_view(request, *args, **kwargs):
    myContext = {
        "title": "Товары",
        "products": [],
        "seeds": []
    }

    productRows, avProducts = getProductsRow()
    myContext["products"] = productRows
    print(productRows)

    for avpr in avProducts:
        if avpr.category.lower() == "семена":
            myContext["seeds"].append(avpr)

    return render(request, "products.html", myContext)

def homepage_view(request, *agrs, **kwargs):
    myContext = {
        "title": "Главная",
        "products": [],
        "seeds": []
    }

    productRows, avProducts = getProductsRow()
    myContext["products"] = productRows
    print(productRows)

    for avpr in avProducts:
        if avpr.category.lower() == "семена":
            myContext["seeds"].append(avpr)

    return render(request, "home.html", myContext)

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