from django.urls import path

from . import views

urlpatterns = [
    path("", views.diet_form_view, name="diet_form"),
]
