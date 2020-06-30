try:
    import requests
except:
    from os import system
    system("pip install requests")
    import requests

from products.models import Product

def sendOrderNotification(name, cartData, oid, phone, email, comment):
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
{comment}
    """
    requests.get(f"https://api.telegram.org/bot1225466990:AAHeSxZ66mt1sOD_0ojhUf4EpbxoVK06TAY/sendMessage?chat_id=@dchadm&parse_mode=markdown&text={msg}")