# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
import urllib2 as url
import json
import re

def index(request):
	return HttpResponse("LOL PHP")
	
