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
    return Decimal("{:.2f}".format(pr.price - pr.price * pr.discount / 100)) * cart[pr.article]
