from django.http import HttpResponse
from django.shortcuts import render

from .gets import *

# Create your views here.

def products_view(request, *args, **kwargs):

    productsRows, categories = getProductsCatrows()

    myContext = {
        "title": "Товары",
        "categories": categories
    }

    myContext["products"] = productsRows

    print(myContext)

    return render(request, "products.html", myContext)


def product_detail_view(request, *args, **kwargs):
    queryDict = request.GET

    if not (request.method == "GET") or not ('article' in queryDict):
        return HttpResponse("Bad request!")

    try:
        requestedArticle = int(request.GET['article'])
        requestedObject = Product.objects.get(article=requestedArticle)
    except:
        return HttpResponse("Bad request!")

    return HttpResponse(str(requestedObject.title))
