# Create your views here.
import datetime
import json
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from bff.vote.forms import LoginForm, RatingFormSet, valid_room, already_voted
from bff.vote.models import Menu, VoteEvent

def login(request):
	if Menu.objects.filter(date=datetime.date.today()).exists():
		if request.method == 'POST':
			form = LoginForm(request.POST)
			if form.is_valid():
				request.session['room'] = form.cleaned_data['room_number']
				return HttpResponseRedirect(reverse('vote'))
				#return HttpResponse("Your room number is %s" % form.cleaned_data['room_number'])
		else:
			form = LoginForm()
		return render(request, 'login.html', {
			'form': form,
		})
	else :
		return HttpResponse("Sorry, the menu has not been added today!")


def vote(request):
	menu = Menu.objects.get(date=datetime.date.today())
	if not 'room' in request.session:
		#Double check there is a room number
		return HttpResponseRedirect('/')

	room = request.session['room']
	if request.method == 'POST':
		formset = RatingFormSet(request.POST)

		if formset.is_valid():
			#Double check that the room is valid
			if (not valid_room(room)) or already_voted(str(room)):
				return HttpResponse("You have already voted. How did you manage that?")

			for form in formset:
				form.save()
			#Create VoteEvent to log the vote
			VoteEvent.objects.create(room_number = room, menu=menu)
			del request.session['room']
			return HttpResponse("Saved your ratings")
	else:
		initial_data = []

		for meal in menu.meal_set.all():
			#Need to provide both the entire meal (used to show name) and the meal id (transmitted as a hidden field)
			initial_data.append({'meal':meal, 'meal_id':meal.id})

		formset = RatingFormSet(initial=initial_data)

	return render_to_response('vote.html', {'formset':formset}, context_instance = RequestContext(request))


def stats(request, year, month, day):
	date = datetime.date(int(year), int(month), int(day))

	menu = get_object_or_404(Menu, date=date)
	results = []
	total_pos = 0
	total_neutral= 0
	total_neg = 0
	for meal in menu.meal_set.all():
		positive = meal.vote_set.filter(rating=2).count()
		neutral  = meal.vote_set.filter(rating=1).count()
		negative = meal.vote_set.filter(rating=0).count()

		meal_res = {
			'meal':meal,
			'positive':positive,
			'neutral':neutral,
			'negative':negative,
			'total':positive + neutral + negative
		}
		total_pos += positive
		total_neutral += neutral
		total_neg += negative

		results.append(meal_res)

	res_dict = {
		'meals':results,
		'totals': {
			'positive':total_pos,
			'neutral':total_neutral,
			'negative':total_neg,
			'total':total_pos + total_neutral + total_neg,
		}
	}

	return render_to_response('stats.html', res_dict, context_instance = RequestContext(request))