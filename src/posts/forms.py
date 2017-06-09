from django import forms


class Contact(forms.Form):
	name = forms.CharField()
	email = forms.EmailField()
	message = forms.CharField()