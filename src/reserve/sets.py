from .models import Reservation
from products.models import Product

def __getTargetProductAndReservationObject(article):
    # Whether a product with this article exists: (if does not, an according exception is thrown)
    TargetProduct = Product.objects.get(article=article)

    # Try to get the object from the DB:
    try:
        ReservationObject = Reservation.objects.get(article=article)
    except Reservation.DoesNotExist as e:
        ReservationObject = Reservation(article=article)

    return TargetProduct, ReservationObject

def reserve(article, amount):
    # Is amount an integer??
    amount = int(amount)

    TargetProduct, ReservationObject = __getTargetProductAndReservationObject(article)

    # Can we reserve such amount of products?
    if ReservationObject.amount + amount > TargetProduct.amount:
        raise("Can't reserve such amount of products!")

    ReservationObject.amount += amount
    ReservationObject.save()


def unreserve(article, amount):
    # Is amount an integer??
    amount = int(amount)

    TargetProduct, ReservationObject = __getTargetProductAndReservationObject(article)

    # Can we unreserve such amount of products?
    if ReservationObject.amount - amount < 0:
        raise("Can't unreserve such amount of products!")

    ReservationObject.amount -= amount
    ReservationObject.save()