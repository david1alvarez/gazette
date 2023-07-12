from rest_framework import serializers
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


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["name"]


class FactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faction
        fields = [
            "name",
            "tier",
            "hold",
            "turf",
            "headquarters",
            "assets",
            "quirks",
            "city",
            "is_active",
        ]


class FactionFactionRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactionFactionRelation
        fields = [
            "source_faction",
            "target_faction",
            "target_reputation",
        ]


class FactionClockSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactionClock
        fields = [
            "name",
            "max_segments",
            "completed_segments",
            "completed",
            "objective_type",
            "faction",
            "target_faction",
        ]


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = [
            "name",
            "description",
            "scene",
            "streets_description",
            "streets",
            "buildings_description",
            "traits",
            "city",
        ]


class DistrictFactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictFaction
        fields = [
            "district",
            "faction",
        ]


class LandmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landmark
        fields = [
            "name",
            "description",
            "district",
        ]


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            "name",
            "description",
            "adjectives",
            "district",
            "faction",
            "is_active",
        ]


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = World
        fields = ["step"]
