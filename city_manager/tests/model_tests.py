from django.db.utils import DataError
from city_manager.exceptions import InvalidInputsException
from django.test import TestCase

from city_manager.models import City, Faction, FactionClock, FactionFactionRelation


class CityTestCase(TestCase):
    def setUp(self):
        City.objects.create(name="paris")
        City.objects.create(name="tokyo")

    # TODO check if teardown step is needed or automatic

    def test_setup(self):
        self.assertEqual(len(City.objects.all()), 2)

    def test_str_method(self):
        city = City.objects.get(name="paris")
        self.assertEqual(str(city), city.name)

    def test_name_length_exception(self):
        too_long_name = "abcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghij"
        with self.assertRaises(DataError):
            City.objects.create(name=too_long_name)


class FactionTestCase(TestCase):
    def setUp(self):
        test_city = City.objects.create(name="test city")
        # TODO: Investigate Faker, or other mock wrappers
        Faction.objects.create(
            name="The McGuffins",
            tier=2,
            hold="s",
            category="Testers",
            turf=["The testcase", "Not the real world"],
            headquarters="FactionTestCase",
            assets=["test 1", "test 2"],
            quirks="They don't actually exist",
            city=test_city,
        )

    def test_setup(self):
        self.assertEqual(len(City.objects.all()), 1)
        self.assertEqual(len(Faction.objects.all()), 1)

    def test_str_method(self):
        faction = Faction.objects.get(name="The McGuffins")
        self.assertEqual(str(faction), faction.name)

    def test_not_deleted_default(self):
        faction = Faction.objects.get(name="The McGuffins")
        self.assertFalse(faction.is_dead_or_deleted)


class FactionFactionRelationTestCase(TestCase):
    def setUp(self):
        test_city = City.objects.create(name="test city")
        faction_1 = Faction.objects.create(
            name="The McGuffins",
            tier=2,
            hold="s",
            category="Testers",
            turf=["The testcase", "Not the real world"],
            headquarters="FactionTestCase",
            assets=["test 1", "test 2"],
            quirks="They don't actually exist",
            city=test_city,
        )
        faction_2 = Faction.objects.create(
            name="The Unobtanium Seekers",
            tier=1,
            hold="w",
            category="Testers",
            turf=["The other testcase", "Not the real world"],
            headquarters="FactionTestCase2",
            assets=["test 1", "test 2"],
            quirks="They don't actually exist",
            city=test_city,
        )
        faction_3 = Faction.objects.create(
            name="Why do you exist?",
            tier=1,
            hold="w",
            category="?",
            headquarters="Nullspace",
            assets=["a great empty void"],
            quirks="Unsurprisingly, they also don't actually exist",
            city=test_city,
        )
        FactionFactionRelation.objects.create_symmetric(
            factions=[faction_1, faction_2],
            reputation=2,
        )
        FactionFactionRelation.objects.create(
            source_faction=faction_1,
            target_faction=faction_3,
            target_reputation=1,
        )
        FactionFactionRelation.objects.create(
            source_faction=faction_3,
            target_faction=faction_1,
            target_reputation=-1,
        )

    def test_setup(self):
        self.assertEqual(len(FactionFactionRelation.objects.all()), 4)
        self.assertEqual(len(Faction.objects.all()), 3)

    def test_create_symmetric_faction_length_error(self):
        factions = list(Faction.objects.all())
        with self.assertRaises(InvalidInputsException):
            FactionFactionRelation.objects.create_symmetric(factions)

    def test_create_symmetric(self):
        faction_1 = Faction.objects.get(name="The McGuffins")
        faction_2 = Faction.objects.get(name="The Unobtanium Seekers")
        relation_1 = FactionFactionRelation.objects.get(
            source_faction=faction_1,
            target_faction=faction_2,
        )
        relation_2 = FactionFactionRelation.objects.get(
            source_faction=faction_2,
            target_faction=faction_1,
        )
        self.assertEqual(relation_1.target_reputation, relation_2.target_reputation)

    def test_create_asymmetric(self):
        faction_1 = Faction.objects.get(name="The McGuffins")
        faction_2 = Faction.objects.get(name="Why do you exist?")
        relation_1 = FactionFactionRelation.objects.get(
            source_faction=faction_1,
            target_faction=faction_2,
        )
        relation_2 = FactionFactionRelation.objects.get(
            source_faction=faction_2,
            target_faction=faction_1,
        )
        self.assertNotEqual(relation_1.target_reputation, relation_2.target_reputation)


class FactionClockTestCase(TestCase):
    def setUp(self):
        test_city = City.objects.create(name="test city")
        faction = Faction.objects.create(
            name="The McGuffins",
            tier=2,
            hold="s",
            category="Testers",
            turf=["The testcase", "Not the real world"],
            headquarters="FactionTestCase",
            assets=["test 1", "test 2"],
            quirks="They don't actually exist",
            city=test_city,
        )
        FactionClock.objects.create(
            name="Assassinate the emperor",
            objective_type="REM",
        )
