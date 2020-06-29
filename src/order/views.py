import json

from django.shortcuts import render
from .forms import OrderForm

from cart.get import u_cart

# Create your views here.
from pages.templatetags import calcPrice
from products.gets import getProductsCatrows
from products.models import Product


def make_order_view(request, *args, **kwargs):
    print(request.session._session_key)
    thisCart = json.loads(u_cart(request).json)
    productsRows, categories = getProductsCatrows()
    cartProducts = Product.objects.filter(isAvailable=True, article__in=thisCart)

    totalPrice = 0
    for cpr in cartProducts:
        totalPrice += calcPrice.calc_final_price(cpr, thisCart)

    myContext = {
        'title': 'Оформление заказа',
        'form': OrderForm(request.POST),
        "cartProducts": cartProducts,
        "thisCart": thisCart,
        "totalPrice": totalPrice,
        "cartID": request.session._session_key
    }

    return render(request, 'make_order.html', myContext)