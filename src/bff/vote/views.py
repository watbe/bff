# Create your views here.
import datetime
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from bff.vote.forms import LoginForm, RatingFormSet
from bff.vote.models import Menu

def login(request):
	if Menu.objects.filter(date=datetime.date.today()).exists():
		if request.method == 'POST':
			form = LoginForm(request.POST)
			if form.is_valid():
				return HttpResponseRedirect("/vote/")
				#return HttpResponse("Your room number is %s" % form.cleaned_data['room_number'])
		else:
			form = LoginForm()
		return render(request, 'login.html', {
			'form': form,
		})
	else :
		return HttpResponse("Sorry, the menu has not been added today!")


def vote(request):
	if request.method == 'POST':
		formset = RatingFormSet(request.POST)

		if formset.is_valid():
			for form in formset:
				form.save()
			return HttpResponse("Saved your ratings")
	else:
		initial_data = []
		menu = Menu.objects.get(date=datetime.date.today())
		for meal in menu.meal_set.all():
			#Need to provide both the entire meal (used to show name) and the meal id (transmitted as a hidden field)
			initial_data.append({'meal':meal, 'meal_id':meal.id})

		formset = RatingFormSet(initial=initial_data)

	return render_to_response('vote.html', {'formset':formset}, context_instance = RequestContext(request))

