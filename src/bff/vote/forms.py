from django import forms

class LoginForm(forms.Form):
	room_number = forms.CharField(max_length=3)

	def clean_room_number(self):
		room_number = self.cleaned_data['room_number']
		if int(room_number) not in (range(101,140) + range(201,240) + range (301,340) + range (151,190) + range (251,290) + range (351,390)):
			raise forms.ValidationError("Invalid Room Number: %s" % room_number)
		else:
			return room_number

