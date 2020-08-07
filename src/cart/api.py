import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Cart
from .get import u_cart
from .sets import addToCart, removeFromCart, removeAmount

from pages.templatetags import calcPrice
from products.models import Product
from products.gets import *

# Create your views here.

requiredMethod = "GET" # TODO: Change to "POST" after debugging

def add_to_cart_view(request, *args, **kwargs):
    

    if requiredMethod == "GET":
        queryDict = request.GET
    else:
        queryDict = request.POST

    if not request.method == requiredMethod:
        return HttpResponse(f'Wrong request method: "{request.method}". Expected: {requiredMethod}')
    if 'article' not in queryDict or 'amount' not in queryDict:
        return HttpResponse(f'Not enough arguments!')

    try:
        requestedArticle = int(request.GET['article'])
        requestedAmount  = int(request.GET['amount'])
        requestedObject = Product.objects.get(article=requestedArticle)
        if requestedAmount > requestedObject.amount:
            return HttpResponse("Нет такого количества товаров!")
    except:
        return HttpResponse("Bad request!")

    try:
        updatedCartJson = addToCart(request, requestedArticle, requestedAmount)
    except:
        return HttpResponse('-1')

    return HttpResponse(updatedCartJson)
    

def user_cart_view(request, *args, **kwargs):
    print(request.session._session_key)
    thisCart = json.loads(u_cart(request).json)
    productsRows, categories = getProductsCatrows()
    cartProducts = Product.objects.filter(isAvailable=True, article__in=thisCart)

    repr_cartProducts = []

    totalPrice = 0
    for cpr in cartProducts:
        repr_cartProducts.append(repr_product_dct(cpr, request=request))
        totalPrice += calcPrice.calc_final_price(cpr, thisCart)

    print(thisCart, repr_cartProducts)
    
    myContext = {
        "title": "Корзина",
        "cartProducts": repr_cartProducts,
        "thisCart": thisCart,
        "totalPrice": float(totalPrice),
        "isEmpty": len(repr_cartProducts) == 0
    }
    try:
        responseStr = json.dumps(myContext, ensure_ascii=False)
    except Exception as e:
        print(e)
        responseStr = "-1"
    print(responseStr)

    return HttpResponse(responseStr)

def remove_from_cart(request, *args, **kwargs):

    if requiredMethod == "GET":
        queryDict = request.GET
    else:
        queryDict = request.POST

    if not request.method == requiredMethod:
        return HttpResponse(f'Wrong request method: "{request.method}". Expected: {requiredMethod}')
    if 'article' not in queryDict:
        return HttpResponse(f'Not enough arguments!')

    try:
        requestedArticle = int(request.GET['article'])
    except:
        return HttpResponse("Bad request!")

    try:
        responseStr = removeFromCart(request, requestedArticle)
    except:
        responseStr = "-1"
        return HttpResponse('-1')

    return user_cart_view(request)

def update_cart(request):
    if requiredMethod == "GET":
        queryDict = request.GET
    else:
        queryDict = request.POST

    if not request.method == requiredMethod:
        responseData = {
            "code": -1,
            "message": f"Wrongs request method! Expected: {requiredMethod}"
        }
        responseStr = json.dumps(responseData, ensure_ascii=False)
        return HttpResponse(responseStr)

    if 'article' not in queryDict or 'deltaAmount' not in queryDict:
        responseData = {
            "code": -1,
            "message": f"Required arguments are not provided."
        }
        responseStr = json.dumps(responseData, ensure_ascii=False)
        return HttpResponse(responseStr)

    requestedArticle = queryDict['article']

    try:
        requestedDeltaAmount = int(queryDict['deltaAmount'])
        if requestedDeltaAmount == -1:
            print("remove")
            removeAmount(request, requestedArticle, 1)
        elif requestedDeltaAmount == 1:
            print("add")
            addToCart(request, requestedArticle, 1)
    except Exception as exc:
        responseData = {
            "code": -1,
            "message": f"Could not finish the operation.",
            "exception": str(exc)
        }
        responseStr = json.dumps(responseData, ensure_ascii=False)
        return HttpResponse(responseStr)

    return user_cart_view(request)
