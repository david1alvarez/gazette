from city_manager.exceptions import RecordNotFoundException
from city_manager.api import OpenAIClient
from city_manager.controllers import FactionController
from city_manager.models import (
    City,
    Faction,
    Calendar,
)


class TimeController:
    city: City

    def __init__(self, city=None):
        if isinstance(city, None):
            self.City = City.objects.first()
        self.city = city

    # advance the clocks for the city's factions
    def next(self):
        current_date = Calendar.objects.latest()

        for faction in Faction.objects.all():
            faction_controller = FactionController(faction=faction)
            try:
                is_completed = faction_controller.roll_clock()
            except RecordNotFoundException:
                # warn that no records were found
                # attempt to create new faction clocks
                pass
            client = OpenAIClient()
            client.create_faction_clock()
