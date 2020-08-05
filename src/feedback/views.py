from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from bot.fb import send_fb

import pickle

# Create your views here.
@csrf_exempt
def process_feedback_view(request, *args, **kwargs):
	if request.method == "POST":
		form = FeedbackForm(request.POST)
		if form.is_valid():
			response = HttpResponse("{0}")

			name = request.POST['name']
			topic = request.POST['topic']
			body = request.POST['body']
			email = request.POST['email']
			send_fb(name, topic, body, email)

			request.session['name'] = f",<br>{name}!"
			return response

	errorResponse = HttpResponse("{-1}")
	errorResponse.status_code = 400

	return errorResponse