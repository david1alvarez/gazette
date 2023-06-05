from __future__ import annotations
from django.db import models
from django_jsonform.models.fields import ArrayField
from enum import Enum


class Calendar(models.Model):
    step = models.PositiveIntegerField(default=0)


class City(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    # calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name


class FactionManager(models.Manager):
    def active(self) -> models.QuerySet[Faction]:
        return self.filter(is_dead_or_deleted=False)


class Faction(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    tier = models.PositiveIntegerField(default=0)
    HOLD_STRENGTH = [("w", "weak"), ("s", "strong")]
    hold = models.CharField(max_length=1, choices=HOLD_STRENGTH, default="w")
    category = models.CharField(null=True, blank=True, max_length=100)
    turf = ArrayField(models.CharField(max_length=100), default=list)
    headquarters = models.CharField(max_length=100, null=True, blank=True)
    assets = ArrayField(models.CharField(max_length=100), default=list)
    quirks = models.TextField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    is_dead_or_deleted = models.BooleanField(default=False)

    objects = FactionManager()

    class Meta:
        indexes = [models.Index(fields=["is_dead_or_deleted"])]

    def __str__(self):
        return self.name


class FactionFactionRelation(models.Model):
    source_faction = models.ForeignKey(
        Faction,
        on_delete=models.CASCADE,
        related_name="relation_source_faction",
    )
    target_faction = models.ForeignKey(
        Faction,
        on_delete=models.CASCADE,
        related_name="relation_target_faction",
    )
    target_reputation = models.IntegerField(default=0)

    class Meta:
        unique_together = [["source_faction", "target_faction"]]
        indexes = [models.Index(fields=["source_faction"])]


class ClockObjectiveType(Enum):
    # TODO: Update this to be integer fields (e.g. ClockObjectiveType.ACQUIRE_ASSET = 1) to improve db query times
    ACQUIRE_ASSET = "ACQ"
    CONTEST_RIVAL = "CON"
    AID_ALLY = "AID"
    REMOVE_RIVAL = "REM"
    EXPAND_GANG = "EXP"
    CLAIM_TERRITORY = "CLA"

    def __str__(self):
        """String method override to allow database queries to use the three-letter abbreviation.

        Returns:
            Literal["ACQ", "CON", "AID", "REM", "EXP", "CLA"]: Three-letter abbreviation of the objective types
        """
        return self.value


class FactionClockManager(models.Manager):
    def active(self) -> models.QuerySet[FactionClock]:
        return self.filter(completed=False)


class FactionClock(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    max_segments = models.PositiveIntegerField(default=4)
    completed_segments = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    OBJECTIVE_TYPES: list[(ClockObjectiveType, str)] = [
        (ClockObjectiveType.ACQUIRE_ASSET, "acquire asset"),
        (ClockObjectiveType.CONTEST_RIVAL, "contest rival"),
        (ClockObjectiveType.AID_ALLY, "aid ally"),
        (ClockObjectiveType.REMOVE_RIVAL, "remove rival"),
        (ClockObjectiveType.EXPAND_GANG, "expand gang"),
        (ClockObjectiveType.CLAIM_TERRITORY, "claim territory"),
    ]
    objective_type = models.CharField(
        choices=OBJECTIVE_TYPES,
        max_length=3,
        default=ClockObjectiveType.ACQUIRE_ASSET,
    )
    faction = models.ForeignKey(
        Faction,
        on_delete=models.CASCADE,
        related_name="clock_source_faction",
    )
    target_faction = models.ForeignKey(
        Faction,
        on_delete=models.SET_NULL,
        related_name="clock_target_faction",
        null=True,
        blank=True,
    )

    objects = FactionClockManager()

    class Meta:
        indexes = [models.Index(fields=["completed"]), models.Index(fields=["faction"])]

    def __str__(self) -> str:
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    scene = models.TextField(null=True, blank=True)
    streets_description = models.TextField(null=True, blank=True)
    streets = ArrayField(models.CharField(max_length=100))
    buildings_description = models.TextField(null=True, blank=True)
    traits = ArrayField(ArrayField(models.CharField(max_length=100)))
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class DistrictFaction(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    faction = models.ForeignKey(Faction, on_delete=models.CASCADE)

    class Meta:
        unique_together = [["district", "faction"]]


class Landmark(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class PersonManager(models.Manager):
    def active(self) -> models.QuerySet[Person]:
        return self.filter(is_dead_or_deleted=False)


class Person(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    adjectives = ArrayField(
        models.CharField(max_length=100),
        default=list,
        null=True,
        blank=True,
    )
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    faction = models.ForeignKey(
        Faction,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    is_dead_or_deleted = models.BooleanField(default=False)

    objects = PersonManager()

    class Meta:
        verbose_name_plural = "people"
        indexes = [models.Index(fields=["is_dead_or_deleted"])]

    def __str__(self):
        return self.name
