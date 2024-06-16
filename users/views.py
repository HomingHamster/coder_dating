from allauth.account.utils import send_email_confirmation
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from users.forms import ProfileForm, EmailForm


class ProfileView(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        return {"profile": self.request.user.profile}


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if reverse("profile-onboarding") == request.path:
            onboarding = True
        else:
            onboarding = False
        return render(request, "profile_edit.html",
                      {"form": ProfileForm(instance=request.user.profile),
                       "onboarding": onboarding})

    def post(self, request, *args, **kwargs):
        if reverse("profile-onboarding") == request.path:
            onboarding = True
        else:
            onboarding = False
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            if form.love and form.age < 18:
                if not form.friendship and not form.working and not form.hiring:
                    messages.error(request, "We have changed looking for love to looking for friendship"
                                            "because you are under 18.")
                    form.friendship = True
                else:
                    messages.error(request, "We have unset love from what you are "
                                            "looking for because you are under 18.")
            form.save()
            redirect("profile")
        return render(request, "profile_edit.html", {"form": form, "onboarding": onboarding})


class ProfileSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "profile_settings.html"


@login_required
def profile_emailchange(request):
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, "partials/email_form.html", {"form": form})
    if request.method == "POST":
        form = EmailForm(request.POST, instance=request.user)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data["email"]).exclude(id=request.user.id).exists():
                messages.error(request, "Email already exists.")
                return redirect("profile-settings")
            form.save()

            send_email_confirmation(request, request.user)
        else:
            messages.warning(request, "Form is not valid!")
            return redirect("profile-settings")

    return redirect("home")


@login_required
def profile_emailverify(request):
    send_email_confirmation(request, request.user)
    return redirect("profile-settings")


class ProfileDeleteView(LoginRequiredMixin, TemplateView):
    template_name = "profile_delete.html"

    def post(self, request, **kwargs):
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Account deleted")
        return redirect("home")

