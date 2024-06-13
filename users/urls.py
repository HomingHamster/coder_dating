from django.urls import path

from users import views

urlpatterns = [
    path("", views.ProfileView.as_view(), name="profile"),
    path("edit", views.ProfileEditView.as_view(), name="edit-profile"),
    path("onboarding", views.ProfileEditView.as_view(), name="profile-onboarding"),
    path("settings", views.ProfileSettingsView.as_view(), name="profile-settings"),
    path("emailchange", views.profile_emailchange, name="profile-emailchange"),
    path("emailverify", views.profile_emailverify, name="profile-emailverify"),
    path("delete", views.ProfileDeleteView.as_view(), name="profile-delete"),
]