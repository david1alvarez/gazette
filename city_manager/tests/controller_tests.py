from django.test import TestCase

from city_manager.controllers.faction_faction_relation import (
    FactionFactionRelationController,
)
from city_manager.models import Faction, FactionFactionRelation
from city_manager.tests.factory import FactionFactory


class FactionFactionRelationControllerTestCase(TestCase):
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
