import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Cart
from .get import u_cart
from .sets import addToCart, removeFromCart

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
        addToCart(request, requestedArticle, requestedAmount)
    except:
        return HttpResponse('-1')

    return HttpResponse('0')
    

def user_cart_view(request, *args, **kwargs):
    print(request.session._session_key)
    thisCart = json.loads(u_cart(request).json)
    productsRows, categories = getProductsCatrows()
    cartProducts = Product.objects.filter(isAvailable=True, article__in=thisCart)

    repr_cartProducts = []

    totalPrice = 0
    for cpr in cartProducts:
        repr_cartProducts.append(repr_product_dct(cpr))
        totalPrice += calcPrice.calc_final_price(cpr, thisCart)

    print(thisCart)
    
    myContext = {
        "title": "Корзина",
        "cartProducts": repr_cartProducts,
        "thisCart": thisCart,
        "totalPrice": totalPrice,
        "isEmpty": len(repr_cartProducts) == 0
    }

    responseStr = json.dumps(myContext, ensure_ascii=False)

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
        removeFromCart(request, requestedArticle)
    except:
        return HttpResponse('-1')

    return HttpResponse("0")