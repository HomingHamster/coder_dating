import uuid

import requests
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, DetailView, DeleteView, UpdateView
from django.contrib.gis.geoip2 import GeoIP2

from dating.forms import LocationForm, SnippetForm
from dating.models import Location, Opinion, CodeSnippet


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    #return ip
    return "208.67.222.222"


g = GeoIP2()


class LocationAutocomplete(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "partial_location_suggestions.html", context={"form": LocationForm})

    def post(self, request, *args, **kwargs):
        form = LocationForm(request.POST)
        if form.is_valid():
        #     requests.get("http://127.0.0.1:2233")
            # return fake suggestions for location until geocoding available
            if not form.cleaned_data['location_string'] == "1 may way":
                return render(request, "partial_location_suggestions.html", context={"form": form})
            else:
                location = Point(x=g.lat_lon(get_client_ip(request))[0], y=g.lat_lon(get_client_ip(request))[1])
                Location(user=request.user, location=location).save()
                return render(request, "partial_location_chosen.html", context={"location": location})
        return HttpResponseBadRequest()


class Browse(LoginRequiredMixin, TemplateView):
    template_name = "browse.html"

    def get_context_data(self, *args, **kwargs):
        location = Location.objects.filter(user=self.request.user)
        if location.exists():
            return {"profile": self.request.user.profile, "location": True}
        else:
            return {"profile": self.request.user.profile, "location": False}


class PersonBrowsePartial(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.GET.get("id") and request.GET.get("like"):
            action_target = get_object_or_404(User, pk=request.GET.get("id"))
            if request.GET.get("like").lower() is "true":
                Opinion(by=request.user, on=action_target, opinion_type=1).save()
            elif request.GET.get("like").lower() is "false":
                Opinion(by=request.user, on=action_target, opinion_type=0).save()
            else:
                return HttpResponseBadRequest()
        location = Location.objects.filter(user=request.user).order_by('-date')
        if location.exists():
            location = location[0].location
            existing_opinion_users = [x.on.pk for x in Opinion.objects.filter(by=request.user).values("on")]

            locations = Location.objects.filter(
                # location__dwithin=(location, 0.02),
                # location__distance_lte=(location, D(m=2000))
            ).annotate(distance=Distance('location', location)).order_by('distance')
            if locations.exists():
                return render(request, "partial_person.html",
                              context={"location": location, "user": locations[0].user})
        else:
            return render(request, "partial_person.html",
                          context={"location": location,"user": None, "time": timezone.now})


# class CodeView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         form = SnippetForm()
#         return render(request, "code_form_set.html", context={"profile": request.user.profile, "form": form})


class CodeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        snippets = CodeSnippet.objects.filter(user=request.user)
        forms = [SnippetForm(instance__in=x, uid=x.uid) for x in snippets]
        return render(request, "code_form_set.html", context={
            "profile": request.user.profile, "forms": forms})


class CodeDeleteView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        get_object_or_404(CodeSnippet.objects.filter(user=self.request.user), id=kwargs.get('pk', None)).delete()
        messages.success(self.request, "Snippet deleted")
        return HttpResponse()



class CodeFormView(LoginRequiredMixin, CreateView):
    template_name = "code_form.html"
    form = SnippetForm
    fields = ["code", "language", "repository_url"]
    model = CodeSnippet

    def get_context_data(self, **kwargs):
        uid=uuid.uuid4()
        return {"form": SnippetForm(uid=uid), "uuid": uid, "exists": False}

    def form_valid(self, form):
        form.instance.user = self.request.user
        print(form.cleaned_data)
        form.save()
        return super().form_valid(form)


class CodeFormUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "code_form.html"
    form = SnippetForm
    fields = ["code", "language", "repository_url"]

    def get_queryset(self):
        return CodeSnippet.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        self.redirect_url = reverse("code_form_update", uuid)
        uid=self.queryset.objects.filter(user=self.request.user, uid=uuid).first().uid
        return {"form": SnippetForm(uid=uid), "uuid": uid, "exists": False}

    def form_valid(self, form):
        form.instance.user = self.request.user
        print(form.cleaned_data)
        form.save()
        return super().form_valid(form)



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        return {"profile": self.request.user.profile}


#class OldMatchesPartial(LoginRequiredMixin, View):
