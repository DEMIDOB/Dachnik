try:
    import requests
except:
    from os import system
    system("pip install requests")
    import requests

from .methods import *

from products.models import Product

def sendOrderNotification(name, cartData, oid, phone, email, comment, removeLink, recieveLink):
    productsOrder = ""

    counter = 1

    for cartElement in cartData:
        try:
            productElement = Product.objects.get(article=cartElement)
            productsOrder += f"*{counter}. {str(productElement.title).capitalize()}* — {cartData[cartElement]} шт. (Артикул: *{cartElement}*)\n"
            counter += 1
        except:
            continue

    msg = f"""
        *Новый заказ №{oid} \n
{name}* заказал(-а):
{productsOrder}
*Телефон:* {phone}
*E-Mail:* {email}\n
*Комментарий к заказу:*
{comment}\n
[Отменить заказ]({removeLink}) | [Выкупить заказ]({recieveLink})
    """
    sendMsg(msg)

def sendCancelledOrderNotification(oid):
    msg = f"*Отмена заказа №{oid}*"
    sendMsg(msg)

def sendRecievedOrderNotification(oid):
    msg = f"Заказ *№{oid} выкуплен*"
    sendMsg(msg)