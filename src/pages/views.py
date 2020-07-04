from django.http import HttpResponse
from django.shortcuts import render
from products.models import Product

from products.gets import *
from feedback.forms import FeedbackForm
from cart.get import u_cart
from blog.syncPosts import syncPosts

import pickle

# Create your views here.


# def allproducts_view(request, *args, **kwargs):
#     myContext = {
#         "title": "Все товары",
#         "products": [],
#         "seeds": []
#     }

#     productRows, avProducts = getProductsRow()
#     myContext["products"] = avProducts
#     print(productRows)

#     # for avpr in avProducts:
#     #     if avpr.category.lower() == "семена":
#     #         myContext["seeds"].append(avpr)

#     myContext["seeds"] = avProducts.filter(category__iexact="семена")

#     return render(request, "allproducts.html", myContext)


def homepage_view(request, *agrs, **kwargs):
    syncPosts()
    request.session['initialized'] = True
    # thisCart = u_cart(request)
    cookies = request.COOKIES

    productsRows, categories = getProductsCatrows()

    withDiscount = []
    catsWithDisct = []
    betterDisc = [0, productsRows[categories[0]][0], 0]

    counter = 0
    for cat in productsRows:
        for pr in productsRows[cat]:
            if not pr.discount == 0:
                if pr.discount > betterDisc[0]:
                    betterDisc[0] = pr.discount
                    betterDisc[1] = pr
                    betterDisc[2] = counter
                withDiscount.append(pr)
                if pr.category.lower() not in catsWithDisct:
                    catsWithDisct.append(pr.category.lower())
                counter += 1

    # Removing object with the best discount from the 'withDiscount' list:
    withDiscount.remove(withDiscount[betterDisc[2]])

    print("BD", betterDisc)
    
    name = request.session.get('name', "!")

    myContext = {
        "title": "Главная",
        "products": productsRows,
        "discProducts": withDiscount,
        "catsWithDisct": catsWithDisct,
        "betterDisc": [betterDisc[1], ],
        "name": name,
        'form': FeedbackForm()
    }

    reponse = render(request, "home.html", myContext)

    return reponse


def page404_view(request, *args, **kwargs):
    return render(request, "page_not_found.html")
