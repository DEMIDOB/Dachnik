# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from  django.core import serializers
from products.models import Product

from products.gets import *
from feedback.forms import FeedbackForm
from customers.get import *
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
    # try:
    #     syncPosts()
    # except:
    #     try:
    #         syncPosts()
    #     except:
    #         print("Could not sync posts")
    # syncPosts()
    # thisCart = u_cart(request)
    userData = getCustomerForRequest(request)
    if not userData["ok"]:
        return HttpResponse(json.dumps({
            "ok": False,
            "msg": userData["msg"]
        }))
    thisCustomer = userData["user"]

    productsRows, categories = getProductsCatrows()

    withDiscount = []
    catsWithDisct = []
    betterDisc = [0, productsRows[categories[0]][0], 0]

    counter = 0
    for cat in productsRows:
        for pr in productsRows[cat]:
            if not pr.discount == 0:
                pr_serialized = repr_product_dct(pr, request=request)
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

    myContext = {
        "title": "Главная",
        "categories": categories,
        "catsWithDisct": catsWithDisct,
        "discProducts": withDiscount,
        "betterDisc": betterDisc[1], # it is already serialized
        "user": thisCustomer.getRepr()
    }

    response_str = json.dumps(myContext, ensure_ascii=False)
    response = HttpResponse(response_str)
    response["Access-Control-Allow-Origin"] = "*"

    return response


def page404_view(request, *args, **kwargs):
    return render(request, "404.html")

def favicon_view(request, *args, **kwargs):
    return HttpResponseRedirect("/static/imgs/favicon.ico")

def order_help_view(request):
    return render(request, "order_help.html")
