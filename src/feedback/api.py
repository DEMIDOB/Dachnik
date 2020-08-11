import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from bot.fb import send_fb
from customers.get import getCustomerForRequest

import pickle

# Create your views here.
@csrf_exempt
def process_feedback_view(request, *args, **kwargs):
	if request.method == "GET":

		userData = getCustomerForRequest(request)
		if not userData["ok"]:
			return HttpResponse(json.dumps({
				"ok": False,
				"msg": userData["msg"]
			}))
		thisCustomer = userData["user"]

		if True:
			response = HttpResponse("0")

			name = request.GET['name']
			topic = request.GET['topic']
			body = request.GET['body']
			email = request.GET['email']
			send_fb(name, topic, body, email)

			thisCustomer.name = f"{name}"
			thisCustomer.save()
			return response

	errorResponse = HttpResponse("-1")
	errorResponse.status_code = 400

	return errorResponse
