# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from  django.core import serializers
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
#     # print(productRows)

#     # for avpr in avProducts:
#     #     if avpr.category.lower() == "семена":
#     #         myContext["seeds"].append(avpr)

#     myContext["seeds"] = avProducts.filter(category__iexact="семена")

#     return render(request, "allproducts.html", myContext)


def homepage_view(request, *agrs, **kwargs):
    if request.get_host() == "http://дачник33.site" or request.get_host() == "http://xn--33-6kcpvmt3f.site":
        return HttpResponseRedirect('http://dachnik33.site/')
    syncPosts()
    request.session['initialized'] = True
    print("Fuck", request.session['initialized'])
    request.COOKIES['asdasd'] = 'asdasd'
    # thisCart = u_cart(request)

    productsRows, categories = getProductsCatrows()

    withDiscount = []
    catsWithDisct = []
    betterDisc = [0, productsRows[categories[0]][0], 0]

    counter = 0
    for cat in productsRows:
        for pr in productsRows[cat]:
            if not pr.discount == 0:
                pr_serialized = repr_product_dct(pr)
                if pr.discount > betterDisc[0]:
                    betterDisc[0] = pr.discount
                    betterDisc[1] = pr_serialized
                    betterDisc[2] = counter
                withDiscount.append(pr_serialized)
                if pr.category.lower() not in catsWithDisct:
                    catsWithDisct.append(pr.category.lower())
                counter += 1

    # Removing object with the best discount from the 'withDiscount' list:
    withDiscount.remove(withDiscount[betterDisc[2]])
    
    name = request.session.get('name', "-1")

    myContext = {
        "title": "Главная",
        "categories": categories,
        "catsWithDisct": catsWithDisct,
        "discProducts": withDiscount,
        "betterDisc": betterDisc[1], # it is already serialized
        "name": name
    }

    response_str = json.dumps(myContext, ensure_ascii=False)
    response = HttpResponse(response_str)
    response.set_cookie('asd', 'asdasd')
    response["Access-Control-Allow-Origin"] = "*"

    return response


def page404_view(request, *args, **kwargs):
    return render(request, "404.html")

def favicon_view(request, *args, **kwargs):
    return HttpResponseRedirect("/static/imgs/favicon.ico")

def order_help_view(request):
    return render(request, "order_help.html")