import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView
from django.contrib.gis.geoip2 import GeoIP2

from dating.forms import LocationForm
from dating.models import Location


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class LocationAutocomplete(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        form = LocationForm(request.POST)
        if form.is_valid():
        #     requests.get("http://127.0.0.1:2233")
            # return fake suggestions for location until geocoding available
            if not form.cleaned_data['location'] == "1 may way":
                return render(request, "partial_location_suggestions.html", context={"locations": ["1 may way"]})
            else:
                g = GeoIP2()
                location = g.lat_lon(get_client_ip(request))
                Location(user=request.user, location=location).save()
                return render(request, "partial_location_chosen.html", context={"location": [location]})


class Browse(LoginRequiredMixin, TemplateView):
    template_name = "browse.html"
    def get_context_data(self, **kwargs):
        output = '''
            <html>
                <head>
                    <title>Hey mum!</title>
                </head>
            </html>'''
        return {"html": output}


class PersonBrowsePartial(LoginRequiredMixin, ListView):
    paginate_by = 1
    template_name = "partial_person.html"
    def get_queryset(self, request, *args, **kwargs):
        location = Location.objects.filter(user=request.user).order_by('-date')[0]
        users = User.objects.filter(location__dwithin=(location, 0.02)).filter(
            location__distance_lte=(location, D(m=2000))
        ).annotate(distance=Distance('location', location)).order_by('distance')
        return users


#class OldMatchesPartial(LoginRequiredMixin, View):


# class ViewMatches(LoginRequiredMixin, View):
#
#
# class NewOpinion(LoginRequiredMixin, View):


