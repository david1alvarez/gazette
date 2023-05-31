# from django.http import HttpResponse
# from .models import City


# def index(request):
#     return HttpResponse("Welcome to the City Manager")


# def cities(request):
#     return HttpResponse(City.objects.all())

from django.shortcuts import render
from rest_framework import generics, status
from .serializers import CitySerializer

from .models import City


class CityListView(generics.ListAPIView):
    model = City
    serializer_class = CitySerializer
