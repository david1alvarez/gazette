from django.urls import path
from .views import CityListView

urlpatterns = [
    # path("", views.index, name="index"),
    path("cities", CityListView.as_view()),
]
