from django.urls import path
from . import views

urlpatterns = [
    path("cities", views.CityApiView.as_view()),
    path("cities/<str:city_name>/", views.CityDetailApiView.as_view()),
    path("factions", views.FactionApiView.as_view()),
    path("factions/<str:faction_name>/", views.FactionDetailApiView.as_view()),
    path("faction_faction_relations", views.FactionFactionRelationApiView.as_view()),
    path(
        "faction_faction_relations/<str:source_faction_name>/<str:target_faction_name>/",
        views.FactionFactionRelationDetailApiView.as_view(),
    ),
    path("faction_clocks", views.FactionClockApiView.as_view()),
    path(
        "faction_clocks/<str:faction_name>/<str:clock_name>/",
        views.FactionClockDetailApiView.as_view(),
    ),
    path("districts", views.DistrictApiView.as_view()),
    path("districts/<str:district_name>/", views.DistrictDetailApiView.as_view()),
    path("district_factions", views.DistrictFactionApiView.as_view()),
    path(
        "district_factions/<str:district_name>/<str:faction_name>/",
        views.DistrictFactionDetailApiView.as_view(),
    ),
    path("landmarks", views.LandmarkApiView.as_view()),
    path(
        "landmarks/<str:landmark_name>/<str:district_name>/",
        views.LandmarkDetailApiView.as_view(),
    ),
    path("people", views.PersonApiView.as_view()),
    path("people/<str:person_name>/", views.PersonDetailApiView.as_view()),
    path("calendars", views.CalendarApiView.as_view()),
    path("calendars/<int:step>/", views.CalendarDetailApiView.as_view()),
]
