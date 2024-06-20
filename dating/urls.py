from django.urls import path

from dating import views

urlpatterns = [
    path("", views.ProfileView.as_view(), name="profile"),
    path("browse-people", views.Browse.as_view(), name="browse"),
    path("api/person-partial", views.PersonBrowsePartial.as_view(), name="person-partial"),
    path("api/location-autocomplete", views.LocationAutocomplete.as_view(), name="location-autocomplete"),
    path("api/code-edit", views.CodeView.as_view(), name="code-edit-form"),
    path("api/code-delete", views.CodeDeleteView.as_view(), name="delete-snippet"),
    path("api/code-form", views.CodeFormView.as_view(), name="code-form"),
]