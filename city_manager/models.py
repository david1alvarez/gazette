from django.db import models
from django.contrib.postgres.fields import ArrayField


class City(models.Model):
    name: models.CharField(max_length=100)


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
    city: models.ForeignKey(City, on_delete=models.PROTECT)


class District(models.Model):
    name: models.CharField(max_length=100, null=True, blank=True)
    description: models.CharField(null=True, blank=True)
    scene: models.CharField(null=True, blank=True)
    streets_description: models.CharField(null=True, blank=True)
    streets: ArrayField(models.CharField(max_length=100))
    buildings_description: models.CharField(null=True, blank=True)
    traits: ArrayField(ArrayField(models.CharField(max_length=100)))
    city: models.ForeignKey(City, on_delete=models.PROTECT)


class DistrictFaction(models.Model):
    district: models.ForeignKey(District, on_delete=models.CASCADE)
    faction: models.ForeignKey(Faction, on_delete=models.CASCADE)


class FactionFactionRelation(models.Model):
    source_faction: models.ForeignKey(Faction, on_delete=models.CASCADE)
    target_faction: models.ForeignKey(Faction, on_delete=models.CASCADE)
    target_reputation: models.IntegerField(default=0)


class Landmark(models.Model):
    name: models.CharField(max_length=100, null=True, blank=True)
    description: models.CharField(null=True, blank=True)
    district: models.ForeignKey(District, on_delete=models.PROTECT)


class NonPlayerCharacter(models.Model):
    name: models.CharField(max_length=100, null=True, blank=True)
    description: models.CharField(null=True, blank=True)
    adjectives: ArrayField(models.CharField(max_length=100), default=list)
    district: models.ForeignKey(District, on_delete=models.PROTECT)
