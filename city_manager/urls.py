from django.urls import path
from . import views

urlpatterns = [
    path("cities", views.CityApiView.as_view()),
    path("cities/<str:city_name>/", views.CityDetailApiView.as_view()),
]
