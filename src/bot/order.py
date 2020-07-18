try:
    import requests
except:
    from os import system
    system("pip install requests")
    import requests

from products.models import Product

def sendOrderNotification(name, cartData, oid, phone, email, comment, removeLink):
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
[Отменить заказ]({removeLink})
    """
    requests.get(f"https://api.telegram.org/bot1225466990:AAHeSxZ66mt1sOD_0ojhUf4EpbxoVK06TAY/sendMessage?chat_id=@dchadm&parse_mode=markdown&text={msg}")

def sendCancelledOrderNotification(oid):
    msg = f"*Отмена заказа №{oid}*"
    requests.get(f"https://api.telegram.org/bot1225466990:AAHeSxZ66mt1sOD_0ojhUf4EpbxoVK06TAY/sendMessage?chat_id=@dchadm&parse_mode=markdown&text={msg}")

