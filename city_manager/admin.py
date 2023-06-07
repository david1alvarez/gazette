from django.contrib import admin

from city_manager.models import (
    City,
    District,
    Faction,
    FactionClock,
    DistrictFaction,
    FactionFactionRelation,
    Landmark,
    Person,
    World,
)


@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "clock_ticks", "created")
    ordering = ["created"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "world", "created")
    ordering = ["created"]


@admin.register(Faction)
class FactionAdmin(admin.ModelAdmin):
    list_display = ("name", "tier", "hold", "city", "is_active", "created")
    ordering = ["created"]


@admin.register(FactionClock)
class FactionClockAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "faction",
        "objective_type",
        "max_segments",
        "completed_segments",
        "completed",
        "created",
    )
    ordering = ["created"]


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "created")
    ordering = ["created"]


@admin.register(DistrictFaction)
class DistrictFactionAdmin(admin.ModelAdmin):
    list_display = ("district", "faction", "created")
    ordering = ["created"]


@admin.register(FactionFactionRelation)
class FactionFactionRelationAdmin(admin.ModelAdmin):
    list_display = ("source_faction", "target_faction", "target_reputation", "created")
    ordering = ["created"]


@admin.register(Landmark)
class LandmarkAdmin(admin.ModelAdmin):
    list_display = ("name", "district", "created")
    ordering = ["created"]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "district", "faction", "is_active", "created")
    ordering = ["created"]
