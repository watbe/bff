import datetime
from django import forms
from django.forms.formsets import formset_factory
from django.forms.widgets import HiddenInput, RadioFieldRenderer, RadioInput, RadioSelect
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from bff.vote.models import VoteEvent, Vote, VOTE_CHOICES, Category

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

class BffRadioInput(RadioInput):
	def render(self, name=None, value=None, attrs=None, choices=()):
		name = name or self.name
		value = value or self.value
		attrs = attrs or self.attrs
		if 'id' in self.attrs:
			label_for = ' for="%s_%s"' % (self.attrs['id'], self.index)
		else:
			label_for = ''
		choice_label = conditional_escape(force_unicode(self.choice_label))
		return mark_safe(u'%s<label%s> %s</label>' % (self.tag(), label_for, choice_label))


class BffRadioFieldRenderer(RadioFieldRenderer):
	def __iter__(self):
		for i, choice in enumerate(self.choices):
			yield BffRadioInput(self.name, self.value, self.attrs.copy(), choice, i)

	def __getitem__(self, idx):
		choice = self.choices[idx] # Let the IndexError propogate
		return BffRadioInput(self.name, self.value, self.attrs.copy(), choice, idx)

class BffRadioSelect(RadioSelect):
	def __init__(self, *args, **kwargs):
		if not 'renderer' in kwargs:
			kwargs['renderer'] = BffRadioFieldRenderer
		super(BffRadioSelect, self).__init__(*args, **kwargs)


class RatingForm(forms.ModelForm):
	"""
	A form representing a rating for a single meal.
	Each RatingForm should be given a meal through
	the 'initial' keyword arg, which is kept
	and used to save the object.
	"""
	meal_id = forms.IntegerField(widget=HiddenInput)

	#Need to overwrite the default field to make it not required

	rating = forms.ChoiceField(choices=FULL_CHOICES, required=False, widget=BffRadioSelect)

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


class SearchForm(forms.Form):
	query = forms.CharField(label="Meal name", required=False)
	category = forms.ModelChoiceField(queryset=Category.objects.all(),
		empty_label="All Categories", label="Category", required=False)