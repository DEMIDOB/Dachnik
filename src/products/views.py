
try:
    import requests
except:
    from os import system
    system("pip install requests")
    import requests

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
        return HttpResponse("Иди куда подальще!")

    try:
        requestedArticle = int(request.GET['article'])
        requestedObject = Product.objects.get(article=requestedArticle)
    except:
        return HttpResponse("Bad request!")

    requests.get(f"https://api.telegram.org/bot1225466990:AAHeSxZ66mt1sOD_0ojhUf4EpbxoVK06TAY/sendMessage?chat_id=@dchadm&text=Кто-то%20заказал:%20{requestedObject.title}")

    return HttpResponse(str(requestedObject.title))
