from django.db.utils import DataError
from django.test import TestCase

from city_manager.models import (
    World,
    City,
    District,
    DistrictFaction,
    Faction,
    FactionClock,
    FactionFactionRelation,
    Landmark,
    Person,
)
from city_manager.tests.factory import (
    WorldFactory,
    CityFactory,
    DistrictFactionFactory,
    DistrictFactory,
    FactionClockFactory,
    FactionFactory,
    LandmarkFactory,
    PersonFactory,
)


class CalendarTests(TestCase):
    def setUp(self):
        WorldFactory()

    def test_setup(self):
        self.assertEqual(len(World.objects.all()), 1)


class CityTests(TestCase):
    def setUp(self):
        city = CityFactory(name="paris")
        CityFactory()
        FactionFactory.create_batch(2, city=city)

    def test_setup(self):
        self.assertEqual(len(City.objects.all()), 2)
        self.assertEqual(len(City.objects.get(name="paris").faction_set.all()), 2)

    def test_str_method(self):
        city = City.objects.get(name="paris")
        self.assertEqual(str(city), city.name)


class FactionTests(TestCase):
    def setUp(self):
        FactionFactory(name="The McGuffins")

    def test_setup(self):
        self.assertEqual(len(Faction.objects.all()), 1)

    def test_str_method(self):
        faction = Faction.objects.get(name="The McGuffins")
        self.assertEqual(str(faction), faction.name)

    def test_not_deleted_default(self):
        faction = Faction.objects.get(name="The McGuffins")
        self.assertTrue(faction.is_active)


class FactionFactionRelationTests(TestCase):
    def setUp(self):
        test_city = CityFactory(name="test city")
        faction_1 = FactionFactory(name="The McGuffins", city=test_city)
        faction_2 = FactionFactory(name="The Unobtanium Seekers", city=test_city)
        FactionFactionRelation.objects.create(
            source_faction=faction_1,
            target_faction=faction_2,
            target_reputation=1,
        )
        FactionFactionRelation.objects.create(
            source_faction=faction_2,
            target_faction=faction_1,
            target_reputation=-1,
        )

    def test_setup(self):
        self.assertEqual(len(FactionFactionRelation.objects.all()), 2)

    def test_create_asymmetric(self):
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
        self.assertNotEqual(relation_1.target_reputation, relation_2.target_reputation)


class FactionClockObjectiveTypesTests(TestCase):
    def test_string_representation(self):
        self.assertEqual(1, int(FactionClock.ObjectiveTypes.ACQUIRE_ASSET))
        self.assertEqual(2, int(FactionClock.ObjectiveTypes.CONTEST_RIVAL))
        self.assertEqual(3, int(FactionClock.ObjectiveTypes.AID_ALLY))
        self.assertEqual(4, int(FactionClock.ObjectiveTypes.REMOVE_RIVAL))
        self.assertEqual(5, int(FactionClock.ObjectiveTypes.EXPAND_GANG))
        self.assertEqual(6, int(FactionClock.ObjectiveTypes.CLAIM_TERRITORY))


class FactionClockTests(TestCase):
    def setUp(self):
        test_city = CityFactory()
        faction = FactionFactory(name="The McGuffins", city=test_city)
        target_faction = FactionFactory(name="Emperor Supreme", city=test_city)
        FactionClock.objects.create(
            name="Assassinate the emperor",
            objective_type=FactionClock.ObjectiveTypes.REMOVE_RIVAL,
            faction=faction,
            target_faction=target_faction,
        )
        FactionClockFactory(
            max_segments=4,
            completed_segments=4,
            completed=True,
            faction=faction,
        )

    def test_setup(self):
        self.assertEqual(len(FactionClock.objects.all()), 2)

    def test_str_method(self):
        clock = FactionClock.objects.get(name="Assassinate the emperor")
        self.assertEqual(str(clock), clock.name[:30])

    def test_active(self):
        faction = Faction.objects.get(name="The McGuffins")
        self.assertEqual(
            FactionClock.objects.active().filter(faction=faction).count(), 1
        )


class DistrictTests(TestCase):
    def setUp(self):
        DistrictFactory(
            name="Test District",
        )

    def test_setup(self):
        self.assertEqual(len(District.objects.all()), 1)

    def test_str_method(self):
        district = District.objects.get(name="Test District")
        self.assertEqual(str(district), district.name)


class DistrictFactionTests(TestCase):
    def setUp(self):
        DistrictFactionFactory()

    def test_setup(self):
        self.assertEqual(len(DistrictFaction.objects.all()), 1)


class LandmarkTests(TestCase):
    def setUp(self):
        LandmarkFactory(
            name="The old townhouse",
        )

    def test_setup(self):
        self.assertEqual(len(Landmark.objects.all()), 1)

    def test_str_method(self):
        landmark = Landmark.objects.get(name="The old townhouse")
        self.assertEqual(str(landmark), landmark.name)


class PersonTests(TestCase):
    def setUp(self):
        PersonFactory(
            name="Hecate",
        )

    def test_setup(self):
        self.assertEqual(len(Person.objects.all()), 1)

    def test_str_method(self):
        person = Person.objects.get(name="Hecate")
        self.assertEqual(str(person), person.name)
