from django.db import models
from django_jsonform.models.fields import ArrayField

# from city_manager.managers import FactionClockManager


class City(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class FactionClock(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    max_segments = models.PositiveIntegerField(default=4)
    completed_segments = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    OBJECTIVE_TYPES = [
        ("ACQ", "acquire asset"),
        ("CON", "contest rival"),
        ("AID", "aid ally"),
        ("REM", "remove rival"),
        ("EXP", "expand gang"),
        ("CLA", "claim territory"),
    ]
    objective_type = models.CharField(
        choices=OBJECTIVE_TYPES,
        max_length=3,
        default="ACQ",
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

    # objects = FactionClockManager()

    def advance(self, amount) -> bool:
        """Adjust the faction clock up or down by the amount provided. If the threshold for completion is crossed
        (`FactionClock.completed_segments` meeting or exceeding `FactionClock.max_segments`), update `FactionClock.completed`

        Args:
            amount (int): the amount for incrementing or decrementing the clock.

        Returns:
            bool: whether the clock is completed
        """
        current_segments = self.completed_segments
        self.completed_segments = current_segments + amount

        self.completed = self.completed_segments >= self.max_segments

        self.save()

        return self.completed


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


class Landmark(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class NonPlayerCharacter(models.Model):
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

    def __str__(self):
        return self.name


class Calendar(models.Model):
    step = models.AutoField(primary_key=True)
