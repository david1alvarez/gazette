from django.contrib import admin

from .models import (
    City,
    District,
    Faction,
    DistrictFaction,
    FactionFactionRelation,
    Landmark,
    NonPlayerCharacter,
)


@admin.register(City)
class AdminCity(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Faction)
class AdminFaction(admin.ModelAdmin):
    list_display = ("name", "tier", "hold", "city")


@admin.register(District)
class AdminDistrict(admin.ModelAdmin):
    list_display = ("id", "name", "city")


@admin.register(DistrictFaction)
class AdminDistrictFaction(admin.ModelAdmin):
    list_display = ("id", "district", "faction")


@admin.register(FactionFactionRelation)
class AdminFactionFactionRelation(admin.ModelAdmin):
    list_display = ("id", "source_faction", "target_faction", "target_reputation")


@admin.register(Landmark)
class AdminLandmark(admin.ModelAdmin):
    list_display = ("id", "name", "district")


@admin.register(NonPlayerCharacter)
class AdminNonPlayerCharacter(admin.ModelAdmin):
    list_display = ("id", "name", "district", "faction")
