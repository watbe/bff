# Create your views here.
import datetime
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template.context import RequestContext
from bff.vote.forms import LoginForm, RatingFormSet, valid_room, already_voted, SearchForm
from bff.vote.models import Menu, VoteEvent, Meal

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
			return render_to_response('finished.html',context_instance = RequestContext(request))
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
		positive = meal.ratings.filter(rating=2).count()
		neutral  = meal.ratings.filter(rating=1).count()
		negative = meal.ratings.filter(rating=0).count()

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

	total_votes = total_neutral + total_pos + total_neg

	average = 0.0

	if total_votes:
		average = float(float(total_pos) / float(total_votes)) * 100

	if average > 49:
		color = "positive"
	else:
		color = "negative"

	res_dict = {
		'meals':results,
		'totals': {
			'positive':total_pos,
			'neutral':total_neutral,
			'negative':total_neg,
			'total':total_pos + total_neutral + total_neg,
		},
		'date':date,
		'average':int(average),
		'color':color,

	}
	if(menu_exists(date, -1)):
		res_dict['prev'] = date - datetime.timedelta(1)
	if(menu_exists(date, 1)):
		res_dict['next'] = date + datetime.timedelta(1)

	res_dict['menus'] = get_menus()
	res_dict['form'] = SearchForm()

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

	search_form = SearchForm()

	return render_to_response('stats_index.html', {'menus':menus, 'form':search_form}, context_instance = RequestContext(request))

def get_menus():

	all_menus = Menu.objects.order_by('-date')
	paginator = Paginator(all_menus, 30)
	page_num = int(0)

	try:
		menus = paginator.page(page_num)
	except EmptyPage:
		menus = paginator.page(paginator.num_pages)

	return menus

def stats_search(request):

	res_dict = {}

	if 'query' in request.GET and 'category' in request.GET:
		#Do search
		form = SearchForm(request.GET)
		queryset = Meal.objects.select_related().order_by('-menu__date')
		query_ = request.GET['query']
		if query_:
			queryset = queryset.filter(name__icontains =query_)
		category_ = request.GET['category']
		if category_:
			queryset = queryset.filter(categories__id =category_)

		paginator = Paginator(queryset, 100) #Change to a smaller number (3?) for testing
		if 'page' in request.GET:
			page_num = request.GET['page']
		else:
			page_num = 1

		try:
			meals = paginator.page(page_num)
		except EmptyPage:
			meals = paginator.page(paginator.num_pages)

		#meals.

		#queryset = queryset.select_related()
		results = []
		for meal in meals:
			count_queryset = meal.ratings.all()
			positive = count_queryset.filter(rating=2).count()
			neutral = count_queryset.filter(rating=1).count()
			negative = count_queryset.filter(rating=0).count()
			total = positive + neutral + negative
			meal_dict = {
				'meal':meal,
				'date':meal.menu.date,
				'positive': positive,
				'neutral': neutral,
				'negative': negative,
				'total': total,
			}
			if total > 0:
				meal_dict['pos_pc'] = int(round(positive * float(300) / total))
				meal_dict['neu_pc'] = int(round(neutral * float(300) / total))
				meal_dict['neg_pc'] = 300 - meal_dict['pos_pc'] - meal_dict['neu_pc']

			results.append(meal_dict)
		res_dict['results'] = results
		res_dict['paginator'] = meals
		res_dict['query'] = query_
		res_dict['category'] = category_
	else:
		form = SearchForm() #Clear the form to prevent error messages

	res_dict['menus'] = get_menus()
	res_dict['form'] = SearchForm()

	return render_to_response('stats_search.html', res_dict, context_instance = RequestContext(request))