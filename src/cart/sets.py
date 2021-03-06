import json

from django.http import HttpResponse

from .models import Cart
from customers.get import getCustomerForRequest
from products.models import Product
from reserve.sets import *
from reserve.get import *

def addToCart(request, productArticle, amount):
    userData = getCustomerForRequest(request)
    if not userData["ok"]:
        return HttpResponse(json.dumps({
            "ok": False,
            "msg": userData["msg"]
        }))
    thisCustomer = userData["user"]
    thisCart = thisCustomer.getCart()

    currentData = json.loads(thisCart.json)

    productArticle = str(productArticle)

    # print(productArticle in currentData)

    newAmount = amount

    if productArticle in currentData:
        newAmount += currentData[productArticle]



    try:
        pr = Product.objects.get(article=productArticle)
    except Exception as exc:
        return -1

    print("CCCCC", pr.amount - getReservation(pr.article))

    if amount > pr.amount - getReservation(pr.article):
        print("oh shit")
        return -1

    currentData[productArticle] = newAmount

    thisCart.json = json.dumps(currentData)
    thisCart.save()

    reserve(productArticle, amount)

    return thisCart.json

def removeAmount(request, productArticle, amount):
    try:
        userData = getCustomerForRequest(request)
        if not userData["ok"]:
            return HttpResponse(json.dumps({
                "ok": False,
                "msg": userData["msg"]
            }))
        thisCustomer = userData["user"]
        thisCart = thisCustomer.getCart()

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
    userData = getCustomerForRequest(request)
    if not userData["ok"]:
        return HttpResponse(json.dumps({
            "ok": False,
            "msg": userData["msg"]
        }))
    thisCustomer = userData["user"]
    thisCart = thisCustomer.getCart()

    currentData = json.loads(thisCart.json)

    unreserve(article, currentData[str(article)])

    currentData.pop(str(article))
    thisCart.json = json.dumps(currentData)
    thisCart.save()

    return thisCart.json

def clearCart(request):
    userData = getCustomerForRequest(request)
    if not userData["ok"]:
        return HttpResponse(json.dumps({
            "ok": False,
            "msg": userData["msg"]
        }))
    thisCustomer = userData["user"]
    thisCart = thisCustomer.getCart()

    thisCart.json = "{}"
    thisCart.save()
