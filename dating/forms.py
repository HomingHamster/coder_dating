from django import forms

from dating.models import Location, CodeSnippet


class LocationForm(forms.Form):
    location_string = forms.CharField(widget=forms.TextInput())


class SnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ["uid", "code", "language", "repository_url"]

    def __init__(self, *args, uid=None, **kwargs):
        super(SnippetForm, self).__init__(*args, **kwargs)

        self.fields["language"].widget.attrs.update({"class": "select form-select", "onchange": "update_language(this, '"+str(uid)+"')"})
        self.fields["uid"].widget.attrs.update({"class": "hidden"})
