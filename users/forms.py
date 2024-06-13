from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Field, Row, HTML

from users.models import Profile


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'inline-block text-gray-700 text-sm font-bold gap-5'
        self.helper.field_class = ''
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
            Fieldset( "Interested in",
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
            HTML('<button type="submit">Submit</button><a class="button button-gray ms-2" href="{{ request.META.HTTP_REFERER }}">Cancel</a>')
        )

    class Meta:
        model = Profile
        exclude = ['user']