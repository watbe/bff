import datetime
from django import forms
from bff.vote.models import VoteEvent 

class LoginForm(forms.Form):
	room_number = forms.CharField(max_length=3)

	def clean_room_number(self):
		valid_rooms = range(101,140) + range(201,240) + range (301,340) + range (151,190) + range (251,290) + range (351,390) 
		room_num = self.cleaned_data['room_number']

		if int(room_num) not in valid_rooms:
			raise forms.ValidationError("Invalid Room Number: %s" % room_num)
		elif VoteEvent.objects.filter(menu__date=datetime.date.today(), room_number=room_num).exists():
			raise forms.ValidationError("You have already voted today.")
		else:
			return room_num

