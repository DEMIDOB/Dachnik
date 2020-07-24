try:
    import requests
except:
    from os import system
    system("pip install requests")
    import requests

from .methods import *

from products.models import Product
from products.gets import formReprData

def sendOrderNotification(name, cartData, oid, phone, email, comment, removeLink, recieveLink):
    productsOrder = formReprData(cartData, telegramMarkdown=True)

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