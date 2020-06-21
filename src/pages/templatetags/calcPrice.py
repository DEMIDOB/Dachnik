from django import template

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
	print(cart)
	amount = cart[str(pr.article)]
	print(amount)
	return Decimal("{:.2f}".format(pr.price - pr.price * pr.discount / 100)) * amount
