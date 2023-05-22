from city_manager.exceptions import RecordNotFoundException
from city_manager.api.open_ai_client import OpenAIClient
from models import (
    City,
    Faction,
    Calendar,
)
import random


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
            try:
                is_completed = faction.roll_clock()
            except RecordNotFoundException:
                # warn that no records were found
                # attempt to create new faction clocks
                pass
            client = OpenAIClient()
            client.create_faction_clock()
