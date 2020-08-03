from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import *
from bot.fb import send_fb

import pickle

# Create your views here.
def process_feedback_view(request, *args, **kwargs):
	if request.method == "POST":
		form = FeedbackForm(request.POST)
		if form.is_valid():
			response = HttpResponseRedirect("/")
			
			name = request.POST['name']
			topic = request.POST['topic']
			body = request.POST['body']
			email = request.POST['email']
			send_fb(name, topic, body, email)

			request.session['name'] = f",<br>{name}!"
			return response
	
	return HttpResponse('Error')