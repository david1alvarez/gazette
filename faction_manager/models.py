from django.db import models
from django.contrib.postgres.fields import ArrayField


class Faction(models.Model):
    name = models.CharField(max_length=100)
    tier = models.IntegerField(default=0)
    HOLD_STRENGTH = [("w", "weak"), ("s", "strong")]
    hold = models.CharField(max_length=1, choices=HOLD_STRENGTH, default="w")
    category = models.CharField(max_length=100, null=True, blank=True)
    turf = ArrayField(models.CharField(max_length=100), default=list)
    headquarters = models.CharField(max_length=100, null=True, blank=True)
    assets: ArrayField(models.CharField(max_length=100))
    quirks: models.CharField(null=True, blank=True)


class District(models.Model):
    name: models.CharField(max_length=100, null=True, blank=True)
    description: models.CharField(null=True, blank=True)
    scene: models.CharField(null=True, blank=True)
    streets_description: models.CharField(null=True, blank=True)
    streets: ArrayField(models.CharField(max_length=100))
    buildings_description: models.CharField(null=True, blank=True)
    traits: ArrayField(
        ArrayField(models.CharField(max_length=100))
    )  # [[trait, strength],]


class DistrictFaction(models.Model):
    district: models.ForeignKey(District, on_delete=models.CASCADE)
    faction: models.ForeignKey(Faction, on_delete=models.CASCADE)


# join table, but this will require some constraints. Could do {source_faction, target_faction, relationship} and likely have duplicate
# relationship entries, could do {faction_a, faction_b, relationship} but you'd need some way to say "get me faction_c's relationships" and pull
# all of the relevant ones into the query
# class FactionFaction(models.Model):


# class Landmark(models.Model):
# name: text
# description: text
# district: fk.District

# class NonPlayerCharacter(models.Model):
# name: text
# description: text
# district: fk.District
# faction: fk.Faction
# adjectives: [text] (e.g. ["calculating", "confident", "calm"])
