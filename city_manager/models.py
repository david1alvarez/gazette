from __future__ import annotations
from django.db import models
from django.utils import timezone
from django_jsonform.models.fields import ArrayField
from enum import Enum
import uuid


class HistoricalModel(models.Model):
    created = models.DateTimeField(default=timezone.now, blank=True, editable=False)
    modified = models.DateTimeField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class World(HistoricalModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default="")
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    clock_ticks = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<World: {self.name}>"


class City(HistoricalModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default="")
    world = models.ForeignKey(World, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<City: {self.name}>"


class FactionManager(models.Manager):
    def active(self) -> models.QuerySet[Faction]:
        return self.filter(is_active=True)


class Faction(HistoricalModel):
    class HoldStrength(models.IntegerChoices):
        WEAK = 0
        STRONG = 1

        def __str__(self):
            return self.text

        @property
        def text(self):
            match (self.value):
                case 0:
                    return "weak"
                case 1:
                    return "strong"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default="")
    description = models.TextField(default="", blank=True)
    tier = models.PositiveIntegerField(default=0)
    hold = models.IntegerField(
        choices=HoldStrength.choices, default=HoldStrength.STRONG
    )
    turf = models.TextField(default="", blank=True)
    headquarters = models.CharField(default="", blank=True)
    assets = models.TextField(default="", blank=True)
    quirks = models.TextField(default="", blank=True)
    current_situation = models.TextField(default="", blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    objects = FactionManager()

    class Meta:
        indexes = [models.Index(fields=["is_active"])]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Faction: {self.name}>"


class FactionFactionRelation(HistoricalModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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


class FactionClockManager(models.Manager):
    def active(self) -> models.QuerySet[FactionClock]:
        return self.filter(completed=False)


class FactionClock(HistoricalModel):
    class ObjectiveTypes(models.IntegerChoices):
        ACQUIRE_ASSET = 1
        CONTEST_RIVAL = 2
        AID_ALLY = 3
        REMOVE_RIVAL = 4
        EXPAND_GANG = 5
        CLAIM_TERRITORY = 6

        def __str__(self):
            return self.text

        @property
        def text(self):
            match (self.value):
                case 1:
                    return "acquire asset"
                case 2:
                    return "contest rival"
                case 3:
                    return "aid ally"
                case 4:
                    return "remove rival"
                case 5:
                    return "expand gang"
                case 6:
                    return "claim territory"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default="")
    max_segments = models.PositiveIntegerField(default=4)
    completed_segments = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    objective_type = models.IntegerField(
        choices=ObjectiveTypes.choices,
        default=ObjectiveTypes.ACQUIRE_ASSET,
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
        return self.name[:30]

    def __repr__(self):
        return f"<FactionClock: {self.name[:30]}>"


class District(HistoricalModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default="")
    description = models.TextField(default="", blank=True)
    scene = models.TextField(default="", blank=True)
    streets_description = models.TextField(default="", blank=True)
    streets = ArrayField(models.CharField(), null=True, blank=True)
    buildings_description = models.TextField(default="", blank=True)
    traits = ArrayField(ArrayField(models.CharField()))
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<District: {self.name}>"


class DistrictFaction(HistoricalModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    faction = models.ForeignKey(Faction, on_delete=models.CASCADE)

    class Meta:
        unique_together = [["district", "faction"]]


class Landmark(HistoricalModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default="")
    description = models.TextField(default="", blank=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, null=True, blank=True
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Landmark: {self.name}>"


class PersonManager(models.Manager):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def active(self) -> models.QuerySet[Person]:
        return self.filter(is_active=True)


class Person(HistoricalModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default="")
    description = models.TextField(default="", blank=True)
    adjectives = ArrayField(
        models.CharField(),
        default=list,
        null=True,
        blank=True,
    )
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    faction = models.ForeignKey(
        Faction,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)

    objects = PersonManager()

    class Meta:
        verbose_name_plural = "people"
        indexes = [models.Index(fields=["is_active"])]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Person: {self.name}>"
