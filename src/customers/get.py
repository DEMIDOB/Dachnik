from django.http import HttpRequest

from .models import Customer

def getCustomerForRequest(request: HttpRequest):
    if request.method == "GET":
        queryDict = request.GET
    elif request.method == "POST":
        queryDict = request.POST
    else:
        return {
            'ok': False,
            'msg': f"Wrong request method {request.method}"
        }

    existed = True

    if 'uid' in request.COOKIES:
        queryDict['uid'] = request.COOKIES['uid']

    if not 'uid' in queryDict:
        thisCustomer = Customer()
        existed = False
    else:
        requestedUID = queryDict['uid']
        try:
            thisCustomer = Customer.objects.get(id=requestedUID)
        except:
            thisCustomer = Customer(id=requestedUID)
            existed = False

    if 'name' in queryDict:
        thisCustomer.name = queryDict['name']

    thisCustomer.save()

    _mutable = (
        request.GET._mutable,
        request.POST._mutable
    )

    request.GET._mutable = True
    request.POST._mutable = True

    if request.method == "GET":
        request.GET['uid'] = thisCustomer.id
    elif request.method == "POST":
        request.POST['uid'] = thisCustomer.id

    request.GET._mutable = _mutable[0]
    request.POST._mutable = _mutable[1]

    return {
        'ok': True,
        'justCreated': existed,
        'user': thisCustomer
    }
