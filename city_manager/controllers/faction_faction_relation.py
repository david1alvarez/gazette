from city_manager.models import Faction, FactionFactionRelation


class FactionFactionRelationController:
    def create_symmetric(
        factions: list[Faction],
        reputation: int = 0,
    ) -> list[FactionFactionRelation]:
        """Create a symmetrical relationship between factions. The reputation level will be
        the same in both directions.

        Args:
            factions (list[Faction]): A list of two Factions, in either order.
            reputation (int, optional): The reputation of the relationship. Defaults to 0.

        Raises:
            ValueError: Thrown if an invalid number of factions are entered.

        Returns:
            list[FactionFactionRelation]: Returns the list created FactionFactionRelation objects of length 2.
        """
        if len(factions) != 2:
            raise ValueError(factions)

        relation_1 = FactionFactionRelation.objects.create(
            source_faction=factions[0],
            target_faction=factions[1],
            target_reputation=reputation,
        )
        relation_2 = FactionFactionRelation.objects.create(
            source_faction=factions[1],
            target_faction=factions[0],
            target_reputation=reputation,
        )

        return [relation_1, relation_2]
