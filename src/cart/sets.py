import json

from .models import Cart
from .get import u_cart
from products.models import Product

def addToCart(request, productArticle, amount):
    thisCart = u_cart(request)
    currentData = json.loads(thisCart.json)

    productArticle = str(productArticle)

    print(productArticle in currentData)

    if productArticle in currentData:
        currentData[productArticle] += amount
    else:
        currentData[productArticle] = amount

    thisCart.json = json.dumps(currentData)
    thisCart.save()

def removeFromCart(request, article):
    thisCart = u_cart(request)
    currentData = json.loads(thisCart.json)
    currentData.pop(str(article))
    thisCart.json = json.dumps(currentData)
    thisCart.save()