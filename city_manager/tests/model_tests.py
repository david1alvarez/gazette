from django.db.utils import DataError
from city_manager.exceptions import InvalidInputsException
from django.test import TestCase

from city_manager.models import (
    Calendar,
    City,
    District,
    DistrictFaction,
    Faction,
    FactionClock,
    ClockObjectiveType,
    FactionFactionRelation,
    Landmark,
    Person,
)


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


class ClockObjectiveTypeTestCase(TestCase):
    def test_string_representation(self):
        self.assertEqual("ACQ", str(ClockObjectiveType.ACQUIRE_ASSET))
        self.assertEqual("CON", str(ClockObjectiveType.CONTEST_RIVAL))
        self.assertEqual("AID", str(ClockObjectiveType.AID_ALLY))
        self.assertEqual("REM", str(ClockObjectiveType.REMOVE_RIVAL))
        self.assertEqual("EXP", str(ClockObjectiveType.EXPAND_GANG))
        self.assertEqual("CLA", str(ClockObjectiveType.CLAIM_TERRITORY))


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
        target_faction = Faction.objects.create(
            name="Emperor Supreme",
            tier=5,
            hold="s",
            category="Lord",
            turf=["Life", "The Universe", "Everything"],
            headquarters="Earth 2",
            assets=["Three heads"],
            quirks="Owns everything",
            city=test_city,
        )
        FactionClock.objects.create(
            name="Assassinate the emperor",
            objective_type=ClockObjectiveType.REMOVE_RIVAL,
            faction=faction,
            target_faction=target_faction,
        )
        FactionClock.objects.create(
            name="Overthrow the candy store",
            objective_type=ClockObjectiveType.CLAIM_TERRITORY,
            max_segments=4,
            completed_segments=4,
            completed=True,
            faction=faction,
        )

    def test_setup(self):
        self.assertEqual(len(FactionClock.objects.all()), 2)

    def test_str_method(self):
        clock = FactionClock.objects.get(name="Assassinate the emperor")
        self.assertEqual(str(clock), clock.name)

    def test_active(self):
        faction = Faction.objects.get(name="The McGuffins")
        self.assertEqual(
            FactionClock.objects.active().filter(faction=faction).count(), 1
        )


class DistrictTestCase(TestCase):
    def setUp(self):
        city = City.objects.create(name="Rome")
        District.objects.create(
            name="Test District",
            description="Low buildings with thatched roofs crowd small winding streets in this quiet neighborhood.",
            scene="Olive-seller tending to a cart with freshly harvested olives and local olive oil.",
            streets_description="Winding poorly-lit cobblestone streets create a mazelike network.",
            streets=["trottoria"],
            buildings_description="Low thatched-roof buildings with narrow wooden doors.",
            traits=[
                ["Wealth", 1],
                ["Security and Safety", 3],
                ["Criminal Influence", 0],
                ["Occult Influence", 3],
            ],
            city=city,
        )

    def test_setup(self):
        self.assertEqual(len(District.objects.all()), 1)

    def test_str_method(self):
        district = District.objects.get(name="Test District")
        self.assertEqual(str(district), district.name)


class DistrictFactionTestCase(TestCase):
    def setUp(self):
        city = city = City.objects.create(name="Rome")
        district = District.objects.create(
            name="Test District",
            description="Low buildings with thatched roofs crowd small winding streets in this quiet neighborhood.",
            scene="Olive-seller tending to a cart with freshly harvested olives and local olive oil.",
            streets_description="Winding poorly-lit cobblestone streets create a mazelike network.",
            streets=["trottoria"],
            buildings_description="Low thatched-roof buildings with narrow wooden doors.",
            traits=[
                ["Wealth", 1],
                ["Security and Safety", 3],
                ["Criminal Influence", 0],
                ["Occult Influence", 3],
            ],
            city=city,
        )
        faction = Faction.objects.create(
            name="The Fates",
            tier=2,
            hold="s",
            category="Witches",
            turf=["The house at the end of the road", "seventy olive trees"],
            headquarters="The basement underneath the old town hall",
            assets=["Eyes", "Cauldrons"],
            quirks="They preach respect for one's elders.",
            city=city,
        )
        DistrictFaction.objects.create(district=district, faction=faction)

    def test_setup(self):
        self.assertEqual(len(DistrictFaction.objects.all()), 1)


class LandmarkTestCase(TestCase):
    def setUp(self):
        city = city = City.objects.create(name="Rome")
        district = District.objects.create(
            name="Test District",
            description="Low buildings with thatched roofs crowd small winding streets in this quiet neighborhood.",
            scene="Olive-seller tending to a cart with freshly harvested olives and local olive oil.",
            streets_description="Winding poorly-lit cobblestone streets create a mazelike network.",
            streets=["trottoria"],
            buildings_description="Low thatched-roof buildings with narrow wooden doors.",
            traits=[
                ["Wealth", 1],
                ["Security and Safety", 3],
                ["Criminal Influence", 0],
                ["Occult Influence", 3],
            ],
            city=city,
        )
        Landmark.objects.create(
            name="The old townhouse",
            description="An old run-down building that housed the local government before The Collapse.",
            district=district,
        )

    def test_setup(self):
        self.assertEqual(len(Landmark.objects.all()), 1)

    def test_str_method(self):
        landmark = Landmark.objects.get(name="The old townhouse")
        self.assertEqual(str(landmark), landmark.name)


class PersonTestCase(TestCase):
    def setUp(self):
        city = city = City.objects.create(name="Rome")
        district = District.objects.create(
            name="Test District",
            description="Low buildings with thatched roofs crowd small winding streets in this quiet neighborhood.",
            scene="Olive-seller tending to a cart with freshly harvested olives and local olive oil.",
            streets_description="Winding poorly-lit cobblestone streets create a mazelike network.",
            streets=["trottoria"],
            buildings_description="Low thatched-roof buildings with narrow wooden doors.",
            traits=[
                ["Wealth", 1],
                ["Security and Safety", 3],
                ["Criminal Influence", 0],
                ["Occult Influence", 3],
            ],
            city=city,
        )
        faction = Faction.objects.create(
            name="The Fates",
            tier=2,
            hold="s",
            category="Witches",
            turf=["The house at the end of the road", "seventy olive trees"],
            headquarters="The basement underneath the old town hall",
            assets=["Eyes", "Cauldrons"],
            quirks="They preach respect for one's elders.",
            city=city,
        )
        Person.objects.create(
            name="Hecate",
            description="An ancient witch with unknowable occult plans.",
            adjectives=["cunning", "ancient", "powerful"],
            district=district,
            faction=faction,
        )

    def test_setup(self):
        self.assertEqual(len(Person.objects.all()), 1)

    def test_str_method(self):
        person = Person.objects.get(name="Hecate")
        self.assertEqual(str(person), person.name)


class CalendarTestCase(TestCase):
    def setUp(self):
        Calendar.objects.create()

    def test_setup(self):
        self.assertEqual(len(Calendar.objects.all()), 1)
