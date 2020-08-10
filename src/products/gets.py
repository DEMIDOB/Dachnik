import json

from .models import Product

from decimal import Decimal
from reserve.get import *
from pages.templatetags.calcPrice import calc_final_price, calc_price
from reserve.get import *

def __getAvailableProducts(**kwargs):
    allProducts = Product.objects.all()
    avProducts = []
    for pr in allProducts:
        # print('\n', pr.amount)
        pr.amount -= getReservation(pr.article)
        # print('\n', pr.amount)
        if pr.isAvailable and pr.amount > 0:
            # newPrice = Decimal("{:.2f}".format(
            #     pr.price - pr.price * pr.discount / 100))
            # pr.price = newPrice
            avProducts.append(pr)

    return avProducts


# def getProductsRow():
#     avProducts = __getAvailableProducts()
#
#     productRows = []
#     stillMoreProducts = True
#     for i in range(0, len(avProducts), 3):
#         print(i)
#         if not stillMoreProducts:
#             break
#         productRows.append([])
#         for j in range(3):
#             try:
#                 productRows[i // 3].append(avProducts[i + j])
#             except IndexError:
#                 stillMoreProducts = False
#                 break
#     return productRows, avProducts


def getProductsCatrows(filters={}):
    avProducts = __getAvailableProducts()
    cats = []
    prows = {}

    filterByCat = False

    if 'category' in filters:
        categoryFilter = filters['category']
        filterByCat = True

    for product in avProducts:
        category = product.category.lower()

        if filterByCat and not category == categoryFilter:
            continue

        if not category in prows:
            prows[category] = []
            cats.append(category)
        prows[category].append(product)

    return prows, cats

def formReprData(cartData, telegramMarkdown = True):
    productsOrder = ""

    counter = 1
    totalPrice = 0

    for cartElement in cartData:
        try:
            productElement = Product.objects.get(article=cartElement)
            if telegramMarkdown:
                productsOrder += f"*{counter}. {str(productElement.title).capitalize()}* — {cartData[cartElement]} шт. (Артикул: *{cartElement}*)\n"
            else:
                productsOrder += f"{counter}. {str(productElement.title).capitalize()} — {cartData[cartElement]} шт. (Артикул: {cartElement})\n"

            totalPrice += calc_final_price(productElement, cartData)

            counter += 1
        except:
            continue

    if telegramMarkdown:
        productsOrder += f"\nИтого: *{totalPrice} ₽*\n"
    else:
        productsOrder += f"\nИтого: {totalPrice} ₽\n"

    return productsOrder

def repr_product_dct(product, **kwargs):
    '''
    Only
    '''
    from cart.get import u_cart
    try:
        request = kwargs['request']
        cart = json.loads(u_cart(request).json)
        print(cart)
        if product.article in cart:
            cartPrice = calc_final_price(product, cart)
        else:
            cartPrice = -1
    except Exception as exc:
        print("Could not calculate the cartPrice", exc)
        cartPrice = -1

    data = {
        'title': str(product.title),
        'description': str(product.description),
        'category': str(product.category),
        'price': str(product.price),
        'finalPrice': str(calc_price(product)),
        "cartPrice": str(cartPrice),
        'discount': str(product.discount),
        'producer': str(product.producer),
        'icon': str(product.icon),
        'article': str(product.article),
        'totalAmount': product.amount,
        'availableAmount': product.amount - getReservation(product.article),
        'isAvailable': product.isAvailable
    }
    return data

def repr_producstCatrows(filters={}):
    prows, categories = getProductsCatrows(filters=filters)

    data = {}

    for category in categories:
        productsInCategory = prows[category]
        data[category] = []
        for product in productsInCategory:
            data[category].append(repr_product_dct(product))

    return data, categories