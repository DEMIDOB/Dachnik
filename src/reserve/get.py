from .models import Reservation


def getReservation(article):
    # Try to get the object from the DB:
    try:
        ReservationObject = Reservation.objects.get(article=article)
    except Reservation.DoesNotExist as e:
        return 0

    return ReservationObject.amount