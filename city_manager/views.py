from django.shortcuts import get_object_or_404
from city_manager.controllers.faction_faction_relation import (
    FactionFactionRelationController,
)
from city_manager.serializers import (
    CalendarSerializer,
    CitySerializer,
    DistrictFactionSerializer,
    DistrictSerializer,
    FactionClockSerializer,
    FactionFactionRelationSerializer,
    FactionSerializer,
    LandmarkSerializer,
    PersonSerializer,
)
from .models import (
    City,
    District,
    DistrictFaction,
    Faction,
    FactionClock,
    FactionFactionRelation,
    Landmark,
    Person,
    World,
)
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


class FactionApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        factions = Faction.objects.active()
        serializer = FactionSerializer(factions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "name": request.data.get("name"),
            "tier": request.data.get("tier"),
            "hold": request.data.get("hold"),
            "turf": request.data.get("turf"),
            "headquarters": request.data.get("headquarters"),
            "assets": request.data.get("assets"),
            "quirks": request.data.get("quirks"),
            "city": request.data.get("city"),
        }
        data["city"] = get_object_or_404(City, name=data["city"])
        serializer = FactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FactionDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, faction_name, *args, **kwargs):
        faction = get_object_or_404(
            Faction,
            name=faction_name,
            is_active=True,
        )
        serializer = FactionSerializer(faction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, faction_name, *args, **kwargs):
        faction_instance = get_object_or_404(Faction, name=faction_name)
        data = {
            "name": request.data.get("name"),
            "tier": request.data.get("tier"),
            "hold": request.data.get("hold"),
            "turf": request.data.get("turf"),
            "headquarters": request.data.get("headquarters"),
            "assets": request.data.get("assets"),
            "quirks": request.data.get("quirks"),
            "city": request.data.get("city"),
            "is_active": request.data.get("is_active"),
        }
        serializer = FactionSerializer(
            instance=faction_instance, data=data, partial=True
        )

        if serializer.is_valid():
            faction_instance.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, faction_name, *args, **kwargs):
        faction_instance = get_object_or_404(Faction, name=faction_name)
        faction_instance.is_active = False
        faction_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FactionFactionRelationApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        faction_faction_relations = FactionFactionRelation.objects.all()
        serializer = FactionFactionRelationSerializer(
            faction_faction_relations, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        source_faction = get_object_or_404(
            Faction,
            name=request.data.get("source_faction_name"),
            is_active=True,
        )
        target_faction = get_object_or_404(
            Faction,
            name=request.data.get("target_faction_name"),
            is_active=True,
        )
        reputation = request.data.get("target_reputation")

        data = {
            "source_faction": source_faction,
            "target_faction": target_faction,
            "target_reputation": reputation,
        }

        serializer = FactionFactionRelationSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get("is_symmetric"):
            FactionFactionRelationController.create_symmetric(
                [source_faction, target_faction],
                reputation,
            )
            return Response(
                data={**serializer.data, "created_symmetric": True},
                status=status.HTTP_201_CREATED,
            )
        else:
            serializer.save()
            return Response(
                {**serializer.data, "created_symmetric": False},
                status=status.HTTP_201_CREATED,
            )


class FactionFactionRelationDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, source_faction_name, target_faction_name, *args, **kwargs):
        faction_faction_relation = get_object_or_404(
            FactionFactionRelation,
            source_faction__name=source_faction_name,
            target_faction__name=target_faction_name,
        )
        serializer = FactionFactionRelationSerializer(faction_faction_relation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, source_faction_name, target_faction_name, *args, **kwargs):
        faction_faction_relation = get_object_or_404(
            FactionFactionRelation,
            source_faction__name=source_faction_name,
            target_faction__name=target_faction_name,
        )
        data = {
            "source_faction": request.data.get("source_faction_name"),
            "target_faction": request.data.get("target_faction_name"),
            "target_reputation": request.data.get("target_reputation"),
        }
        serializer = FactionFactionRelationSerializer(
            instance=faction_faction_relation, data=data, partial=True
        )

        if serializer.is_valid():
            faction_faction_relation.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(
        self, request, source_faction_name, target_faction_name, *args, **kwargs
    ):
        faction_faction_relation = get_object_or_404(
            FactionFactionRelation,
            source_faction__name=source_faction_name,
            target_faction__name=target_faction_name,
        )
        faction_faction_relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FactionClockApiView(APIView):
    def get(self, request, *args, **kwargs):
        faction_clocks = FactionClock.objects.active()
        serializer = FactionClockSerializer(faction_clocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "name": request.data.get("name"),
            "max_segments": request.data.get("max_segments"),
            "completed_segments": request.data.get("completed_segments"),
            "completed": request.data.get("completed"),
            "objective_type": request.data.get("objective_type"),
            "faction": request.data.get("faction"),
            "target_faction": request.data.get("target_faction"),
        }
        data["completed"] = data["completed_segments"] >= data["max_segments"]
        data["faction"] = get_object_or_404(Faction, name=data["faction"])
        data["target_faction"] = get_object_or_404(Faction, name=data["target_faction"])

        serializer = FactionClockSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FactionClockDetailApiView(APIView):
    def get(self, request, clock_name, faction_name, *args, **kwargs):
        faction_clock = get_object_or_404(
            FactionClock,
            name=clock_name,
            faction__name=faction_name,
        )
        serializer = FactionClockSerializer(faction_clock)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, clock_name, faction_name, *args, **kwargs):
        faction_clock = get_object_or_404(
            FactionClock, name=clock_name, faction__name=faction_name
        )
        data = {
            "name": request.data.get("name"),
            "max_segments": request.data.get("max_segments"),
            "completed_segments": request.data.get("completed_segments"),
            "completed": request.data.get("completed"),
            "objective_type": request.data.get("objective_type"),
            "faction": request.data.get("faction"),
            "target_faction": request.data.get("target_faction"),
        }
        data["completed"] = data["completed_segments"] >= data["max_segments"]
        data["faction"] = get_object_or_404(Faction, name=data["faction"])
        data["target_faction"] = get_object_or_404(Faction, name=data["target_faction"])

        serializer = FactionClockSerializer(
            instance=faction_clock, data=data, partial=True
        )

        if serializer.is_valid():
            faction_clock.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, clock_name, faction_name, *args, **kwargs):
        faction_clock = get_object_or_404(
            FactionClock,
            name=clock_name,
            faction__name=faction_name,
        )
        faction_clock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DistrictApiView(APIView):
    def get(self, request, *args, **kwargs):
        districts = District.objects.all()
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "scene": request.data.get("scene"),
            "streets_description": request.data.get("streets_description"),
            "streets": request.data.get("streets"),
            "buildings_description": request.data.get("buildings_description"),
            "traits": request.data.get("traits"),
            "city": request.data.get("city"),
        }
        data["city"] = get_object_or_404(City, name=data["city"])

        serializer = DistrictSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DistrictDetailApiView(APIView):
    def get(self, request, district_name, *args, **kwargs):
        district = get_object_or_404(District, name=district_name)
        serializer = DistrictSerializer(district)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, district_name, *args, **kwargs):
        district = get_object_or_404(District, name=district_name)
        data = {
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "scene": request.data.get("scene"),
            "streets_description": request.data.get("streets_description"),
            "streets": request.data.get("streets"),
            "buildings_description": request.data.get("buildings_description"),
            "traits": request.data.get("traits"),
            "city": request.data.get("city"),
        }
        data["city"] = get_object_or_404(City, name=data["city"])

        serializer = DistrictSerializer(instance=district, data=data, partial=True)

        if serializer.is_valid():
            district.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, district_name, *args, **kwargs):
        district = get_object_or_404(District, name=district_name)
        district.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DistrictFactionApiView(APIView):
    def get(self, request, *args, **kwargs):
        district_factions = DistrictFaction.objects.all()
        serializer = DistrictFactionSerializer(
            district_factions,
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "district": request.data.get("district"),
            "faction": request.data.get("faction"),
        }
        data["district"] = get_object_or_404(District, name=data["district"])
        data["faction"] = get_object_or_404(Faction, name=data["faction"])

        serializer = DistrictFactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class DistrictFactionDetailApiView(APIView):
    def get(self, request, district_name, faction_name, *args, **kwargs):
        district_faction = get_object_or_404(
            DistrictFaction,
            district__name=district_name,
            faction__name=faction_name,
        )
        serializer = DistrictFactionSerializer(district_faction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, district_name, faction_name, *args, **kwargs):
        district_faction = get_object_or_404(
            DistrictFaction,
            district__name=district_name,
            faction__name=faction_name,
        )
        data = {
            "district": request.data.get("district_name"),
            "faction": request.data.get("district_name"),
        }
        data["district"] = get_object_or_404(District, name=data["district"])
        data["faction"] = get_object_or_404(Faction, name=data["faction"])

        serializer = DistrictFactionSerializer(
            instance=district_faction, data=data, partial=True
        )

        if serializer.is_valid():
            district_faction.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, district_name, faction_name, *args, **kwargs):
        district_faction = get_object_or_404(
            DistrictFaction,
            district__name=district_name,
            faction__name=faction_name,
        )
        district_faction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LandmarkApiView(APIView):
    def get(self, request, *args, **kwargs):
        landmarks = Landmark.objects.all()
        serializer = LandmarkSerializer(landmarks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "district": request.data.get("district"),
        }
        data["district"] = get_object_or_404(District, name=data["district"])

        serializer = LandmarkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LandmarkDetailApiView(APIView):
    def get(self, request, landmark_name, district_name, *args, **kwargs):
        landmark = get_object_or_404(
            Landmark, name=landmark_name, district__name=district_name
        )
        serializer = LandmarkSerializer(landmark)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, landmark_name, district_name, *args, **kwargs):
        landmark = get_object_or_404(
            Landmark, name=landmark_name, district__name=district_name
        )
        data = {
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "district": request.data.get("district"),
        }
        data["district"] = get_object_or_404(District, name=data["district"])

        serializer = LandmarkSerializer(instance=landmark, data=data, partial=True)
        if serializer.is_valid():
            landmark.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, landmark_name, district_name, *args, **kwargs):
        landmark = get_object_or_404(
            Landmark, name=landmark_name, district__name=district_name
        )
        landmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonApiView(APIView):
    def get(self, request, *args, **kwargs):
        people = Person.objects.active()
        serializer = PersonSerializer(people, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "adjectives": request.data.get("adjectives"),
            "district": request.data.get("district"),
            "faction": request.data.get("faction"),
        }
        data["district"] = get_object_or_404(District, name=data["district"])
        data["faction"] = get_object_or_404(Faction, name=data["faction"])

        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonDetailApiView(APIView):
    def get(self, request, name, district, *args, **kwargs):
        person = get_object_or_404(Person, name=name, district__name=district)
        serializer = PersonSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, name, district, *args, **kwargs):
        person = get_object_or_404(Person, name=name, district__name=district)
        data = {
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "adjectives": request.data.get("adjectives"),
            "district": request.data.get("district"),
            "faction": request.data.get("faction"),
            "is_active": request.data.get("is_active"),
        }
        data["district"] = get_object_or_404(District, name=data["district"])
        data["faction"] = get_object_or_404(Faction, name=data["faction"])

        serializer = PersonSerializer(instance=person, data=data, partial=True)
        if serializer.is_valid():
            person.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, district, *args, **kwargs):
        person = get_object_or_404(Person, name=name, district__name=district)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CalendarApiView(APIView):
    def get(self, request, *args, **kwargs):
        calendar = World.objects.all()
        serializer = CalendarSerializer(calendar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "step": request.data.get("step"),
        }

        serializer = CalendarSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CalendarDetailApiView(APIView):
    def get(self, request, step, new_step, *args, **kwargs):
        calendar = get_object_or_404(World, step=step)
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, step, *args, **kwargs):
        calendar = get_object_or_404(World, step=step)
        data = {
            "step": request.data.get("new_step"),
        }

        serializer = CalendarSerializer(instance=calendar, data=data, partial=True)
        if serializer.is_valid():
            calendar.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, step, *args, **kwargs):
        calendar = get_object_or_404(World, step=step)
        calendar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
