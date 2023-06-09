import factory

# list of providers: https://faker.readthedocs.io/en/master/providers.html

from city_manager.models import (
    City,
    District,
    DistrictFaction,
    Faction,
    FactionClock,
    FactionFactionRelation,
    Landmark,
    Person,
    World,
)
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")


class WorldFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = World

    name = factory.Faker("sentence", nb_words=2)
    owner = factory.SubFactory(UserFactory)
    clock_ticks = factory.Faker("random_int", min=0)


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = factory.Faker("city")
    world = factory.SubFactory(WorldFactory)


class FactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Faction

    name = factory.Faker("sentence", nb_words=2)
    tier = factory.Faker("random_int", min=0, max=5)
    hold = factory.Faker("random_element", elements=(0, 1))
    turf = factory.Faker("sentences")
    headquarters = factory.Faker("sentence")
    assets = factory.Faker("texts", max_nb_chars=50)
    quirks = factory.Faker("paragraph")
    city = factory.SubFactory(CityFactory)


class FactionFactionRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FactionFactionRelation

    source_faction = factory.SubFactory(FactionFactory)
    target_faction = factory.SubFactory(FactionFactory)
    target_reputation = factory.Faker("random_int", min=-3, max=3)


class FactionClockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FactionClock

    # values required for lazy evaluation of `completed`
    class Params:
        completed_segments = factory.Faker("random_int", min=0, max=8)
        max_segments = factory.Faker("random_int", min=0, max=8, step=2)

    name = factory.Faker("sentence")
    objective_type = factory.Faker("enum", enum_cls=FactionClock.ObjectiveTypes)
    completed = factory.LazyAttribute(lambda o: o.max_segments <= o.completed_segments)
    faction = factory.SubFactory(FactionFactory)


class DistrictFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = District

    name = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    scene = factory.Faker("paragraph")
    streets_description = factory.Faker("paragraph")
    streets = factory.Faker("texts", max_nb_chars=50)
    buildings_description = factory.Faker("paragraph")
    traits = [
        ["Wealth", factory.Faker("random_int", min=0, max=4)],
        ["Security and Safety", factory.Faker("random_int", min=0, max=4)],
        ["Criminal Influence", factory.Faker("random_int", min=0, max=4)],
        ["Occult Influence", factory.Faker("random_int", min=0, max=4)],
    ]
    city = factory.SubFactory(CityFactory)


class DistrictFactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DistrictFaction

    district = factory.SubFactory(DistrictFactory)
    faction = factory.SubFactory(FactionFactory)


class LandmarkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Landmark

    name = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    district = factory.SubFactory(DistrictFactory)
    city = factory.SubFactory(CityFactory)


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person

    name = factory.Faker("name")
    description = factory.Faker("paragraph")
    adjectives = factory.Faker("words")
