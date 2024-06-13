from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Field, Row, HTML, BaseInput

from users.models import Profile, InterestedIn


class ProfileForm(forms.ModelForm):
    interested_in_transfem = forms.BooleanField(required=False)
    interested_in_transmasc = forms.BooleanField(required=False)
    interested_in_men = forms.BooleanField(required=False)
    interested_in_women = forms.BooleanField(required=False)
    interested_in_nonbinary = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'inline-block text-gray-700 text-sm font-bold'
        self.helper.field_class = ' '
        self.helper.layout = Layout(
            Fieldset("About you",
                     HTML('<p class="text-gray-700 text-sm mb-1">If you do not fill these in you will only get '
                          'matches who have also not filled them in.</p>'),
                     Row("gender", "age", css_class="columns-2"),
                     wrapper_class="p-3"
                     ),
            Fieldset(
                'Profile Details',
                'display_name',
                'image',
                'bio',
            ),
            Fieldset("Interested In",
                     HTML('<p class="text-gray-700 text-sm mb-1">Feel free to tick everything, but if you '
                          'tick nothing there will be no matches</p>'),
                     Field("interested_in_transfem", wrapper_class="p-0 m-0 pe-5"),
                     Field("interested_in_transmasc", wrapper_class="p-0 m-0 pe-5"),
                     Field("interested_in_men", wrapper_class="p-0 m-0 pe-5"),
                     Field("interested_in_women", wrapper_class="p-0 m-0 pe-5"),
                     Field("interested_in_nonbinary", wrapper_class="p-0 m-0 "),
                     css_class="flex flex-wrap"),
            Fieldset( "Looking for",
                HTML('<p class="text-gray-700 text-sm mb-1">You will not get any matches if you dont chose '
                     'at least one of these.</p>'),
                Row(
                        Field("friendship", wrapper_class="pe-5"),
                        Field("love", wrapper_class="pe-5"),
                        Field("working", wrapper_class="pe-5"),
                        "hiring",
                        css_class="flex flex-wrap"
                ), wrapper_class="p-3"
            ),
            HTML('<button type="submit">Submit</button><a class="button button-gray ms-2" '
                 'href="{{ request.META.HTTP_REFERER }}">Cancel</a>')
        )

    class Meta:
        model = Profile
        exclude = ['user']

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=commit)

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