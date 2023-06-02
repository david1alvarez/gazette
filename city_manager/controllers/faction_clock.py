from city_manager.models import FactionClock
from logging import warning


class FactionClockController:
    def __init__(self, faction_clock: FactionClock):
        self.faction_clock = faction_clock

    def increment_clock(self, amount: int) -> bool:
        """Increment or decrement the faction clock by the amount entered. Values below 0 are not supported.
        If the faction clock is set to be below 0 the new value of the clock will be 0

        Args:
            amount (int): the amount to increment or decrement the clock by

        Returns:
            bool: Whether this action completed the faction's clock
        """
        new_amount = self.faction_clock.completed_segments + amount
        if new_amount < 0:
            warning(
                f"Setting a faction clock to below 0 is not permitted. Updating clock '{self.faction_clock.name}' progress to 0"
            )
            new_amount = 0
        self.faction_clock.completed_segments = new_amount
        self.faction_clock.completed = (
            self.faction_clock.completed_segments >= self.faction_clock.max_segments
        )
        self.faction_clock.save()
        return self.faction_clock.completed
