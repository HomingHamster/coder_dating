from django.urls import path

from dating import views

urlpatterns = [
    path("", views.Browse.as_view(), name="browse"),
]