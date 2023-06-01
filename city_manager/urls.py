from django.urls import path
from . import views

urlpatterns = [
    path("api", views.CityApiView.as_view()),
]
