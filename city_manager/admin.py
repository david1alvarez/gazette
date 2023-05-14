from django.contrib import admin

from .models import (
    City,
    District,
    Faction,
    FactionClock,
    DistrictFaction,
    FactionFactionRelation,
    Landmark,
    NonPlayerCharacter,
)


@admin.register(City)
class AdminCity(admin.ModelAdmin):
    list_display = ("name", "id")


@admin.register(Faction)
class AdminFaction(admin.ModelAdmin):
    list_display = ("name", "tier", "hold", "city", "id")


@admin.register(FactionClock)
class AdminFactionClock(admin.ModelAdmin):
    list_display = ("name", "faction", "objective_type", "id")


@admin.register(District)
class AdminDistrict(admin.ModelAdmin):
    list_display = ("name", "city", "id")


@admin.register(DistrictFaction)
class AdminDistrictFaction(admin.ModelAdmin):
    list_display = ("district", "faction", "id")


@admin.register(FactionFactionRelation)
class AdminFactionFactionRelation(admin.ModelAdmin):
    list_display = ("source_faction", "target_faction", "target_reputation", "id")


@admin.register(Landmark)
class AdminLandmark(admin.ModelAdmin):
    list_display = ("name", "district", "id")


@admin.register(NonPlayerCharacter)
class AdminNonPlayerCharacter(admin.ModelAdmin):
    list_display = ("name", "district", "faction", "id")
