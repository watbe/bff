# Create your views here.
import datetime
import json
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
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

def menu_exists(date, delta_days):
	"""
	Returns True if there is a menu in the database
	for the given day, plus (or minus) delta_days
	"""
	del_date = date + datetime.timedelta(days=delta_days)
	return Menu.objects.filter(date=del_date).exists()


def stats(request, year, month, day):
	try:
		date = datetime.date(int(year), int(month), int(day))
	except ValueError:
		return HttpResponseNotFound("That is not a valid date")
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
		},
		'date':date,
	}
	if(menu_exists(date, -1)):
		res_dict['prev'] = date - datetime.timedelta(1)
	if(menu_exists(date, 1)):
		res_dict['next'] = date + datetime.timedelta(1)

	return render_to_response('stats.html', res_dict, context_instance = RequestContext(request))


def stats_index(request):
	return stats_index_page(request, 1)


def stats_index_page(request, page):
	all_menus = Menu.objects.order_by('-date')
	paginator = Paginator(all_menus, 30)
	page_num = int(page)

	try:
		menus = paginator.page(page_num)
	except EmptyPage:
		menus = paginator.page(paginator.num_pages)

	return render_to_response('stats_index.html', {'menus':menus}, context_instance = RequestContext(request))