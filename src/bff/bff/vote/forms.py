from django import forms

class LoginForm(forms.Form):
	room_number = forms.CharField(max_length=3)
