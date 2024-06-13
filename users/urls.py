from django.urls import path

from users import views

urlpatterns = [
    path("", views.ProfileView.as_view(), name="profile"),
    path("edit", views.ProfileEditView.as_view(), name="edit-profile"),
]