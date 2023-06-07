import logging
from django.test import TestCase
from city_manager.controllers.faction import FactionController
from city_manager.controllers.faction_clock import FactionClockController

from city_manager.controllers.faction_faction_relation import (
    FactionFactionRelationController,
)
from city_manager.models import Faction, FactionClock, FactionFactionRelation
from city_manager.tests.factory import FactionClockFactory, FactionFactory
from unittest.mock import MagicMock


class FactionClockControllerTests(TestCase):
    def setUp(self):
        FactionClockFactory()
        # decrementing the clock below zero logs a warning
        logging.disable(logging.WARNING)
        return super().setUp()

    def tearDown(self) -> None:
        logging.disable(logging.NOTSET)
        return super().tearDown()

    def test_increment_clock(self):
        faction_clock = FactionClock.objects.first()
        clock_completed_segments = faction_clock.completed_segments
        faction_clock_controller = FactionClockController(faction_clock=faction_clock)
        faction_clock_controller.increment_clock(1)

        self.assertEqual(faction_clock.completed_segments, clock_completed_segments + 1)
        faction_clock.completed_segments = 0
        faction_clock.save()

    def test_decrement_below_zero_returns_zero(self):
        faction_clock = FactionClock.objects.first()
        clock_completed_segments = faction_clock.completed_segments
        faction_clock_controller = FactionClockController(faction_clock=faction_clock)
        faction_clock_controller.increment_clock(
            -1 - clock_completed_segments,  # ensure we go below 0
        )
        self.assertEqual(faction_clock.completed_segments, 0)


class FactionFactionRelationControllerTests(TestCase):
    def setUp(self):
        FactionFactory.create_batch(3)

    def test_create_symmetric(self):
        factions = list(Faction.objects.all())[:2]
        FactionFactionRelationController.create_symmetric(
            factions=factions, reputation=2
        )
        faction_relations = list(FactionFactionRelation.objects.all())

        self.assertEqual(len(faction_relations), 2)
        self.assertEqual(
            faction_relations[0].target_reputation,
            faction_relations[1].target_reputation,
        )

    def test_create_symmetric_faction_length_error(self):
        factions = list(Faction.objects.all())
        with self.assertRaises(ValueError):
            FactionFactionRelationController.create_symmetric(factions)


class FactionControllerTests(TestCase):
    def setUp(self):
        faction = FactionFactory(name="The McGuffins")
        FactionClockFactory(completed_segments=0, max_segments=4, faction=faction)

    def test_roll_clock(self):
        faction = Faction.objects.get(name="The McGuffins")
        faction = FactionController(faction=faction)

        # Exceed max_segments, complete clock every time
        faction._get_roll_increment = MagicMock(return_value=5)

        clock = faction.roll_clock()
        self.assertTrue(clock.completed)
