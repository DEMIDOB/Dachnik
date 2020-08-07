
try:
    import requests
except:
    from os import system
    system("pip install requests")
    import requests

from django.http import HttpResponse
from django.shortcuts import render

from .gets import *
from cart.get import u_cart
from reserve.get import *

# Create your views here.

def products_view(request, *args, **kwargs):

    productsRows, categories = repr_producstCatrows()

    myContext = {
        "title": "Товары",
        "categories": categories,
        "products": productsRows
    }

    responseData = json.dumps(myContext, ensure_ascii=False)

    return HttpResponse(responseData)


def product_detail_view(request, *args, **kwargs):
    thisCart = u_cart(request)
    queryDict = request.GET
    requestedArticle = int(request.GET['article'])
    requestedObject = Product.objects.get(article=requestedArticle)
    # requestedObject.amount -= getReservation(requestedArticle) # TODO: remove and deal with availableAmount on frontend




    myContext = {
        "title": f"Купить {requestedObject.title}",
        "pr": repr_product_dct(requestedObject)
    }

    # requests.get(f"https://api.telegram.org/bot1225466990:AAHeSxZ66mt1sOD_0ojhUf4EpbxoVK06TAY/sendMessage?chat_id=@dchadm&text=Кто-то%20заказал:%20{requestedObject.title}")

    responseStr = json.dumps(myContext, ensure_ascii=False)

    # return render(request, "product_details.html", myContext)
    return HttpResponse(responseStr)

def add_to_cart(request, *args, **kwargs):
    thisCart = u_cart(request)
    queryDict = request.GET

    if not (request.method == "GET") or not ('article' in queryDict):
        return HttpResponse("Иди куда подальще!")

    try:
        requestedArticle = int(request.GET['article'])
        requestedAmount = int (request.GET['amount'])
        requestedObject = Product.objects.get(article=requestedArticle)
        if requestedAmount > requestedObject.amount:
            return HttpResponse("Нет такого количества товаров!")
    except:
        return HttpResponse("Bad request!")

    newAmount = requestedObject.amount - requestedAmount
    whetherAvailable = True
    if newAmount == 0:
        whetherAvailable = False

    return HttpResponse(requestedObject.title)