from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Row, HTML, Div
from django.contrib.auth.models import User

from users.models import Profile, InterestedIn


class ProfileForm(forms.ModelForm):
    interested_in_transfem = forms.BooleanField(required=False, initial=True, label="Transfem")
    interested_in_transmasc = forms.BooleanField(required=False, initial=True, label="Transmasc")
    interested_in_men = forms.BooleanField(required=False, initial=True, label="Men")
    interested_in_women = forms.BooleanField(required=False, initial=True, label="Women")
    interested_in_nonbinary = forms.BooleanField(required=False, initial=True, label="Non-binary")

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'inline-block text-gray-700 text-sm font-bold'
        self.helper.field_class = ' '
        self.helper.layout = Layout(
            HTML("<h2>About you</h2>"),
            HTML('<p class="text-secondary text-sm mb-1">If you do not fill these in you will only get '
                 'matches who have also not filled them in.</p>'),
            Div("gender", "age", css_class="d-flex flex-row flex-wrap gap-3"),
            HTML("<h2>Profile Details</h2>"),
            Div('display_name', 'image', 'bio', css_class="my-3"),
            HTML("<h2>Interested In</h2>"),
            HTML('<p class="text-secondary text-sm mb-1">Feel free to tick everything, but if you '
                 'tick nothing there will be no matches.</p>'),
            Div(
                     "interested_in_transfem",
                     "interested_in_transmasc",
                     "interested_in_men",
                     "interested_in_women",
                     "interested_in_nonbinary",
                     css_class="d-flex flex-row flex-wrap my-3",
            ),
            HTML("<h2>Looking for</h2>"),
            HTML('<p class="text-secondary text-sm mb-1">You will not get any matches if you dont chose '
                 'at least one of these.</p>'),
            Div(
                 "friendship", "love", "working", "hiring",
                 css_class="d-flex flex-row flex-wrap my-3",
             ),
            HTML('<button class="btn btn-lg btn-success" type="submit">Submit</button>'
                 '{% if onboarding %}<a class="btn btn-secondary btn-lg ms-2" '
                 'href="{% url "home" %}">Skip</a>{% else %}<a class="btn btn-lg btn-secondary ms-2" '
                 'href="{{ request.META.HTTP_REFERER }}">Cancel</a>{% endif %}')
        )

    class Meta:
        model = Profile
        exclude = ['user']

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)

        if profile.age < 18:
            profile.love = False

        profile.save()

        interests = InterestedIn.objects.filter(user=profile.user)

        if (not interests.filter(interest="tf").exists()) and self.cleaned_data['interested_in_transfem']:
            InterestedIn(user=profile.user, interest="tf").save()
        elif (not self.cleaned_data['interested_in_transfem']) and interests.filter(interest="tf").exists():
            interests.filter(interest="tf").delete()

        if (not interests.filter(interest="tm").exists()) and self.cleaned_data['interested_in_transmasc']:
            InterestedIn(user=profile.user, interest="tm").save()
        elif (not self.cleaned_data['interested_in_transmasc']) and interests.filter(interest="tm").exists():
            interests.filter(interest="tm").delete()

        if (not interests.filter(interest="m").exists()) and self.cleaned_data['interested_in_men']:
            InterestedIn(user=profile.user, interest="m").save()
        elif (not self.cleaned_data['interested_in_men']) and interests.filter(interest="m").exists():
            interests.filter(interest="m").delete()

        if (not interests.filter(interest="w").exists()) and self.cleaned_data['interested_in_women']:
            InterestedIn(user=profile.user, interest="w").save()
        elif (not self.cleaned_data['interested_in_women']) and interests.filter(interest="w").exists():
            interests.filter(interest="w").delete()

        if (not interests.filter(interest="nb").exists()) and self.cleaned_data['interested_in_nonbinary']:
            InterestedIn(user=profile.user, interest="nb").save()
        elif (not self.cleaned_data['interested_in_nonbinary']) and interests.filter(interest="nb").exists():
            interests.filter(interest="nb").delete()

        return profile


class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email"]
