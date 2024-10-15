from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Row, HTML, Div
from django.contrib.auth.models import User

from coder_dating import settings
from dating import models
from users.models import Profile, InterestedIn


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for role in ["f", "l"]:
            for gender in settings.genders:
                self.fields[role+"_"+gender[0]] = forms.BooleanField(required=False, initial=True, label=gender[1])

        self.helper = FormHelper()
        self.helper.label_class = 'inline-block text-gray-700 text-sm font-bold'
        self.helper.field_class = ' '
        self.helper.layout = Layout(
            HTML('<div class="card my-4"><div class="card-header pt-3"><h3>About You</h3></div><div class="card-body">'),
            HTML('<p class="text-secondary text-sm mb-1">If you do not fill these in you will only get '
                 'matches who have also not filled them in.</p>'),
            Div("gender", "age", css_id="about", css_class="d-flex flex-row flex-wrap gap-3 mt-1"),
            HTML("</div></div>"),

            HTML('<div class="card my-4"><div class="card-header pt-3"><h3>Profile Details</h3></div><div class="card-body">'),
            Div('display_name', 'image', 'bio', css_id="profile", css_class="mt-1"),

            HTML("</div></div>"),

            HTML('<div class="card my-4"><div class="card-header pt-3"><h3>Looking for and Interested In</h3></div><div class="card-body">'),
            HTML('<p class="mt-1 mb-1 fs-5"><b>Looking for</b></p>'),
            HTML('<p class="text-secondary m-0">You will not get any matches if you dont chose '
                 'at least one of these.</p>'),
            Div(
                 "friendship", "love", "working", "hiring",
                 css_class="d-flex flex-row flex-wrap my-3",
             ),
            HTML('<p class="mt-4 mb-1 fs-5"><b>Interested In (for friendship)</b></p>'),
            HTML('<p class="text-secondary m-0">Feel free to tick everything, but if you '
                 'tick nothing there will be no matches for friendship.</p>'),
            Div(
                *["f_"+i[0] for i in settings.genders],
                     css_class="d-flex flex-row flex-wrap my-3",
            ),
            HTML('<p class="mt-4 mb-1 fs-5"><b>Interested In (for love)</b></p>'),
            HTML('<p class="text-secondary m-0">Feel free to tick everything, but if you '
                 'tick nothing there will be no matches for love.</p>'),
            Div(

                *["l_"+i[0] for i in settings.genders],
                     css_class="d-flex flex-row flex-wrap my-3",
            ),

            HTML("</div></div>"),
            HTML('<div class="w-100 text-center"><button class="btn btn-lg btn-success" type="submit">Submit</button>'
                 '{% if onboarding %}<a class="btn btn-secondary btn-lg ms-2" '
                 'href="{% url "home" %}">Skip</a>{% else %}<a class="btn btn-lg btn-secondary ms-2" '
                 'href="{{ request.META.HTTP_REFERER }}">Cancel</a>{% endif %}</div>')
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

        def save_interest(interest_short, interest, role):
            if (not interests.filter(interest=interest_short).exists()) and self.cleaned_data[interest]:
                InterestedIn(user=profile.user, interest=interest_short, role=role).save()
            elif (not self.cleaned_data[interest]) and interests.filter(interest=interest_short).exists():
                interests.filter(interest=interest_short, role=role).delete()

        for role in ["f", "l"]:
            for gender in settings.genders:
                save_interest(gender[0], role+"_"+gender[0], role)

        return profile


class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email"]
