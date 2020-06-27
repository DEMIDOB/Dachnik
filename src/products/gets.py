from .models import Product

from decimal import Decimal
from reserve.get import *

def getAvailableProducts():
    allProducts = Product.objects.all()
    avProducts = []
    for pr in allProducts:
        print('\n', pr.amount)
        pr.amount -= getReservation(pr.article)
        print('\n', pr.amount)
        if pr.isAvailable:
            # newPrice = Decimal("{:.2f}".format(
            #     pr.price - pr.price * pr.discount / 100))
            # pr.price = newPrice
            avProducts.append(pr)

    return avProducts


def getProductsRow():
    avProducts = getAvailableProducts()

    productRows = []
    stillMoreProducts = True
    for i in range(0, len(avProducts), 3):
        print(i)
        if not stillMoreProducts:
            break
        productRows.append([])
        for j in range(3):
            try:
                productRows[i // 3].append(avProducts[i + j])
            except IndexError:
                stillMoreProducts = False
                break
    return productRows, avProducts


def getProductsCatrows():
    avProducts = getAvailableProducts()
    cats = []
    prows = {}

    for product in avProducts:
        category = product.category.lower()
        if not category in prows:
            prows[category] = []
            cats.append(category)
        prows[category].append(product)

    return prows, cats
