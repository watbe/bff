# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from bff.vote.forms import LoginForm

import urllib2 as url
import json
import re

def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			return HttpResponse("Your room number is %s" % form.cleaned_data['room_number'])
	else:
		form = LoginForm()
	return render(request, 'login.html', {
		'form': form,
	})	

def vote(request):
		return HttpResponseRedirect('/')

