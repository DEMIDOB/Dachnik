import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .forms import OrderForm
from .models import Order

from cart.sets import clearCart

from bot.order import sendOrderNotification, sendCancelledOrderNotification, sendRecievedOrderNotification
from mail.order_mail import *

from customers.get import getCustomerForRequest

# Create your views here.
from pages.templatetags import calcPrice
from products.gets import getProductsCatrows, repr_product_dct
from products.models import Product
from reserve.sets import unreserve


def make_order_view(request, *args, **kwargs):
    userData = getCustomerForRequest(request)
    if not userData["ok"]:
        return HttpResponse(json.dumps({
            "ok": False,
            "msg": userData["msg"]
        }))
    thisCustomer = userData["user"]
    thisCart = thisCustomer.getCart()
    thisCartJSON = json.loads(thisCart.json)

    # productsRows, categories = getProductsCatrows()
    cartProducts = Product.objects.filter(isAvailable=True, article__in=thisCartJSON)

    repr_cartProducts = []

    totalPrice = 0
    for cpr in cartProducts:
        repr_cartProducts.append(repr_product_dct(cpr, request=request))
        totalPrice += calcPrice.calc_final_price(cpr, thisCartJSON)

    myContext = {
        'title': 'Оформление заказа',
        "cartProducts": repr_cartProducts,
        "thisCart": thisCartJSON,
        "totalPrice": float(totalPrice),
        "cartID": request.session._session_key,
        "isEmpty": len(repr_cartProducts) == 0,
        "user": thisCustomer.getRepr()
    }

    reponseStr = json.dumps(myContext, ensure_ascii=False)

    return HttpResponse(reponseStr)

@csrf_exempt
def complete_order(request, *args, **kwargs):
    print(request.get_host())
    queryDict = request.POST

    if not request.method == "POST":
        return HttpResponse(f"Wrong request method '{request.method}'! Expected 'POST'")

    try:
        userData = getCustomerForRequest(request)
        if not userData["ok"]:
            return HttpResponse(json.dumps({
                "ok": False,
                "msg": userData["msg"]
            }))
        thisCustomer = userData["user"]
        thisCart = thisCustomer.getCart()

        cartJSON = thisCart.json
        cartData = json.loads(cartJSON)
        if len(cartData) < 1:
            return HttpResponse(f"Вы пытаетесь оформить пустой заказ. Так нельзя :)")

        name  = queryDict['name']
        phone = queryDict['phone']
        email = queryDict['email']
    except Exception as exc:
        print(exc)
        return HttpResponse(f"Not enough request data!\n\n{exc}")

    try:
        comment = queryDict['comment']
    except:
        comment = "—"
        print("No comment! =)")

    # Create OrderObject:
    OrderObject = Order(json=cartJSON, name=name, email=email)

    # Clear the user's cart:
    try:
        clearCart(request)
    except Exception as exc:
        return HttpResponse(f"Can not clear your cart because of the above exception:\n{exc}")

    OrderObject.save()

    request.session['name'] = f"{name}"

    print(f"{request.get_host()}/remove_order?oid={OrderObject.id}")

    sendOrderNotification(name, cartData, OrderObject.id, phone, email, comment, f"{request.get_host()}/remove_order?oid={OrderObject.id}", f"{request.get_host()}/recieve_order?oid={OrderObject.id}")
    sendThanksForOrderEmail(OrderObject)

    # return HttpResponseRedirect(f'/thankyou/?oid={OrderObject.id}')
    responseData = {
        "ok": True,
        "user": thisCustomer.getRepr()
    }
    responseStr = json.dumps(responseData, ensure_ascii=False)

    return HttpResponse(responseStr)

def remove_order(request, *args, **kwargs):
    queryDict = request.GET

    if not request.method == "GET":
        return HttpResponse(f"Wrong request method '{request.method}'! Expected 'GET'")

    try:
        oid = queryDict['oid']
    except:
        return HttpResponse(f"Not enough arguments!")

    myContext = {
        'oid': f"{oid}"
    }

    return render(request, 'remove_order.html', myContext)

def rm_o(request, *args, **kwargs):
    queryDict = request.GET

    if not request.method == "GET":
        return HttpResponse(f"Wrong request method '{request.method}'! Expected 'GET'")

    try:
        oid = queryDict['oid']
    except:
        return HttpResponse(f"Not enough arguments!")

    try:
        targetOrder = Order.objects.get(id=oid)
    except:
        return HttpResponse(f"There is no such order!")

    orderData = json.loads(targetOrder.json)

    for orderElement in orderData:
        elementAmount = orderData[orderElement]
        unreserve(orderElement, elementAmount)

    targetOrder.delete()

    sendCancelledOrderNotification(oid)
    sendCancelledOrderEmail(targetOrder, oid)

    return HttpResponse(f"Ok!")


def thankyou_view(request, *args, **kwargs):
    return render(request, 'thankyou.html', {'oid': request.GET['oid']})

def recieve_order_view(request, *args, **kwargs):
    queryDict = request.GET

    if not request.method == "GET":
        return HttpResponse(f"Wrong request method '{request.method}'! Expected 'GET'")

    try:
        oid = queryDict['oid']
    except:
        return HttpResponse(f"Not enough arguments!")

    myContext = {
        'oid': f"{oid}"
    }

    return render(request, 'recieve_order.html', myContext)

def rec_o(request, *args, **kwargs):
    queryDict = request.GET

    if not request.method == "GET":
        return HttpResponse(f"Wrong request method '{request.method}'! Expected 'GET'")

    try:
        oid = queryDict['oid']
    except:
        return HttpResponse(f"Not enough arguments!")

    try:
        targetOrder = Order.objects.get(id=oid)
    except:
        return HttpResponse(f"There is no such order!")

    orderData = json.loads(targetOrder.json)

    for orderElement in orderData:
        try:
            targetProduct = Product.objects.get(article=orderElement)
        except:
            return HttpResponse(f"There is no product with such article: {orderElement}!")
        elementAmount = orderData[orderElement]
        newAmount = targetProduct.amount - elementAmount
        if newAmount < 0:
            return HttpResponse(f"There are not so ({elementAmount}) many products!")
        unreserve(orderElement, elementAmount)
        targetProduct.amount = newAmount
        targetProduct.save()

    targetOrder.delete()

    sendRecievedOrderNotification(oid)
    sendRecievedOrderEmail(targetOrder, oid)

    return HttpResponse("Ok!")
