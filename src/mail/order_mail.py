import json

from .methods import sendMail

from order.models import Order
from products.gets import formReprData

def sendThanksForOrderEmail(order_object: Order):
    orderRepresentation = formReprData(json.loads(order_object.json), telegramMarkdown = False)
    sendMail(f"{order_object.name}, спасибо за заказ!", f"Здравствуйте, {order_object.name}! Вас приветствует магазин \"Дачник\".\n\nВы оформили заказ на сайте:\n{orderRepresentation}\n\nНомер заказа: №{order_object.id}\n\nДля получения заказа в магазине назовите консультанту его номер.", order_object.email)

def sendCancelledOrderEmail(order_object: Order, oid):
    sendMail(f"Отмена заказа №{oid}", f"{order_object.name}, Ваш заказ отменён. Если это сделали не Вы, значит, его отменила администрация.\nЕсли у Вас есть вопросы, позвоните по тел. 44-51-62.", order_object.email)

def sendRecievedOrderEmail(order_object: Order, oid):
    message = f"{order_object.name}, Ваш заказ выкуплен.\nЖдём Вас в нашем магазине снова!"
    sendMail(f"Ваш заказ №{oid} выкуплен!", message, order_object.email)