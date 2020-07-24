import json

from django import template
from products.models import Product

from decimal import Decimal

register = template.Library()


@register.filter
def length(arr):
    return len(arr)


@register.filter
def calc_price(pr):
    return Decimal("{:.2f}".format(pr.price - pr.price * pr.discount / 100))


@register.filter
def calc_final_price(pr, cart):
	amount = cart[str(pr.article)]
	print(amount)
	return Decimal("{:.2f}".format(pr.price - pr.price * pr.discount / 100)) * amount

def calc_total_price(cartData: str, cartObjects: [Product]):
	res = 0
	for cartObject in cartObjects:
		res += calc_final_price(cartObject, cartData)
	return res