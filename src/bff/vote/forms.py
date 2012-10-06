import datetime
from django import forms
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms.widgets import HiddenInput
from bff.vote.models import VoteEvent, Vote, VOTE_CHOICES

def already_voted(room_str):
	"""
	Takes a room number as a string, returns true if they have already voted today,
	or if the number is invalid
	"""
	return VoteEvent.objects.filter(menu__date=datetime.date.today(), room_number=room_str).exists()

def valid_room(room_str):
	"""
	Takes a room number as a string, returns true if the room number is valid.
	"""
	valid_rooms = range(101,141) + range(201,241) + range (301,341) + range (151,191) + range (251,291) + range (351,391)

	return int(room_str) in valid_rooms

class LoginForm(forms.Form):
	room_number = forms.CharField(max_length=3)

	def clean_room_number(self):

		room_num = self.cleaned_data['room_number']

		if not valid_room(int(room_num)):
			raise forms.ValidationError("Invalid Room Number: %s" % room_num)
		elif already_voted(room_num):
			raise forms.ValidationError("You have already voted today.")
		else:
			return room_num



FULL_CHOICES = (('', 'No rating'),) + VOTE_CHOICES

class RatingForm(forms.ModelForm):
	"""
	A form representing a rating for a single meal.
	Each RatingForm should be given a meal through
	the 'initial' keyword arg, which is kept
	and used to save the object.
	"""
	meal_id = forms.IntegerField(widget=HiddenInput)

	#Need to overwrite the default field to make it not required

	rating = forms.ChoiceField(choices=FULL_CHOICES, required=False, widget=forms.RadioSelect)

	class Meta:
		model = Vote
		fields = ("rating",) #We only want to be able to modify the rating

	def __init__(self, *args, **kwargs):
		"""
		Hijacks the initialisation of the form to ensure that the meal
		is not discarded.
		"""
		super(RatingForm, self).__init__ (*args, **kwargs)
		if 'initial' in kwargs:
			self.meal = kwargs['initial']['meal']

	def save(self, commit=True):

		if self.cleaned_data['rating'] != u'':
			db_rating = int(self.cleaned_data['rating'])
			Vote.objects.create(rating = db_rating, meal_id=int(self.cleaned_data['meal_id']))
		return

#Used to create several forms at once
RatingFormSet = formset_factory(RatingForm, extra=0)
