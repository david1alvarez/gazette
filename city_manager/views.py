from django.http import HttpResponse
from .models import City


def index(request):
    return HttpResponse("Welcome to the City Manager")


def cities(request):
    return HttpResponse(City.objects.all())
