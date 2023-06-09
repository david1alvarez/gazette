from city_manager.api import OpenAIClient
from city_manager.controllers import FactionController
from city_manager.models import (
    City,
    Faction,
    World,
    FactionClock,
)


class TimeController:
    city: City

    def __init__(self, city: City):
        self.city = city

    def advance_time(self) -> list[FactionClock]:
        """Advance time by one step, and roll the clocks for each faction in the city.

        Returns:
            list[FactionClock]: The list of clocks completed by the rolls.
        """
        current_date = World.objects.latest()
        current_date.step = current_date.step + 1
        current_date.save()

        factions = self.city.faction_set.all()
        newly_completed_clocks = []
        for faction in factions:
            controller = FactionController(faction=faction)
            clock = controller.roll_clock()
            if clock.completed:
                newly_completed_clocks.append(clock)

        return newly_completed_clocks
