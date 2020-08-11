import json

from django.http import HttpResponse

from .models import Customer
from .get import *

def myname_api(request):
    userData = getCustomerForRequest(request)
    if not userData["ok"]:
        return HttpResponse(json.dumps({
            "ok": False,
            "msg": userData["msg"]
        }))
    thisCustomer = userData["user"]

    respData = {
        "name": thisCustomer.name if not thisCustomer.name == "" else "-1",
        "exists": not thisCustomer.name == ""
    }

    respStr = json.dumps(respData, ensure_ascii=False)

    return HttpResponse(respStr)
