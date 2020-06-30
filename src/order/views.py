import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import OrderForm
from .models import Order

from cart.get import u_cart
from cart.sets import clearCart

from bot.order import sendOrderNotification

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

def complete_order(request, *args, **kwargs):
    queryDict = request.POST

    if not request.method == "POST":
        return HttpResponse(f"Wrong request method '{request.method}'! Expected 'POST'")

    try:
        cartJSON = u_cart(request).json
        cartData = json.loads(cartJSON)

        name  = queryDict['name']
        phone = queryDict['phone']
        email = queryDict['email']
    except:
        return HttpResponse("Not enough request data!")

    try:
        comment = queryDict['comment']
    except:
        comment = "—"
        print("No comment! =)")

    # Create OrderObject:
    OrderObject = Order(json=cartJSON)

    # Clear the user's cart:
    try:
        clearCart(request)
    except Exception as exc:
        return HttpResponse(f"Can not clear your cart because of the above exception:\n{exc}")

    OrderObject.save()

    request.session['name'] = f",<br>{name}!"

    sendOrderNotification(name, cartData, OrderObject.id, phone, email, comment)

    return HttpResponseRedirect(f'/thankyou/?oid={OrderObject.id}')