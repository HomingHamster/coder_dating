from django import forms

from dating.models import Location


class LocationForm(forms.Form):
    location_string = forms.CharField(widget=forms.TextInput())
