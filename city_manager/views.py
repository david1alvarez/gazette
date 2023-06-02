from django.shortcuts import get_object_or_404
from city_manager.serializers import CitySerializer
from .models import City
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


class CityApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {"name": request.data.get("name")}
        serializer = CitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CityDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, city_name, *args, **kwargs):
        city = get_object_or_404(City, name=city_name)
        serializer = CitySerializer(city)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, city_name, *args, **kwargs):
        city_instance = get_object_or_404(City, name=city_name)
        data = {"name": request.data.get("name")}
        serializer = CitySerializer(instance=city_instance, data=data, partial=True)

        if serializer.is_valid():
            city_instance.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, city_name, *args, **kwargs):
        city_instance = get_object_or_404(City, name=city_name)
        city_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
