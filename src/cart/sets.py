import json

from .models import Cart
from .get import u_cart
from products.models import Product
from reserve.sets import *

def addToCart(request, productArticle, amount):

    thisCart = u_cart(request)
    if thisCart == -1:
        return -1
    currentData = json.loads(thisCart.json)

    productArticle = str(productArticle)

    print(productArticle in currentData)

    if productArticle in currentData:
        currentData[productArticle] += amount
    else:
        currentData[productArticle] = amount

    thisCart.json = json.dumps(currentData)
    thisCart.save()

    reserve(productArticle, amount)

    return 0

def removeAmount(request, productArticle, amount):
    try:
        thisCart = u_cart(request)
        if thisCart == -1:
            raise("There is no cart belonging to this user or the user is not registered!")

        currentData = json.loads(thisCart.json)

        if productArticle not in currentData:
            raise("There is no such product in this cart!")

        newAmount = currentData[productArticle] - amount
        if newAmount < 0:
            raise("Not enough items!")
        elif newAmount == 0:
            currentData.__delitem__(productArticle)
        else:
            currentData[productArticle] = newAmount

        thisCart.json = json.dumps(currentData)
        thisCart.save()

        unreserve(productArticle, amount)

    except Exception as exc:
        print(exc)
        return -1

def removeFromCart(request, article):
    thisCart = u_cart(request)
    currentData = json.loads(thisCart.json)

    unreserve(article, currentData[str(article)])

    currentData.pop(str(article))
    thisCart.json = json.dumps(currentData)
    thisCart.save()

def clearCart(request):
    thisCart = u_cart(request)
    thisCart.json = "{}"
    thisCart.save()