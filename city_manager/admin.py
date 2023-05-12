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

admin.site.register(City)
admin.site.register(Faction)
admin.site.register(District)
admin.site.register(DistrictFaction)
admin.site.register(FactionFactionRelation)
admin.site.register(Landmark)
admin.site.register(NonPlayerCharacter)
