import requests
from allauth.account.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from dating.forms import LocationForm


class LocationAutocomplete(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        form = LocationForm(request.POST)
        if form.is_valid():
            requests.get("http://127.0.0.1:2233")


# Browse
# BrowseOldMatches
# ViewMatches
# PersonPartial
# NewOpinion
