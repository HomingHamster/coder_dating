from django import forms

from dating.models import Location, CodeSnippet


class LocationForm(forms.Form):
    location_string = forms.CharField(widget=forms.TextInput())


class SnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ["code", "language", "repository_url"]
