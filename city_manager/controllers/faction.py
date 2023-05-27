from city_manager.controllers.faction_clock import FactionClockController
from city_manager.controllers.probability import Outcome
from city_manager.models import Faction, FactionClock
from city_manager.exceptions import RecordNotFoundException
from logging import error


class FactionController:
    def __init__(self, faction: Faction):
        self.faction = faction

    def active_clocks(self) -> list[FactionClock]:
        clocks = FactionClock.objects.filter(faction=self, completed=False)
        return list(clocks)

    def roll_clock(self, dice=1, clock_id: int = None) -> bool:
        """Roll the advancement of one of the faction's clocks

        Args:
            dice (int, optional): The number of dice that will be simulated in rolling the faction's clock's advancement. Defaults to 1.
            clock_id (int, optional): The id of the clock to advance. Leave as None to select randomly. Defaults to None.

        Returns:
            bool: The True/False value of whether the clock was completed
        """
        if isinstance(clock_id, None):
            clock = (
                FactionClock.objects.active()
                .filter(faction=self.faction)
                .order_by("?")
                .first()
            )
        else:
            try:
                clock = FactionClock.objects.active().get(id=clock_id)
                if clock.faction != self.faction:
                    raise RecordNotFoundException(FactionClock)
            except:
                error(f"no faction clock found for id {clock_id}")
        if isinstance(clock, None):
            raise RecordNotFoundException(
                "Expected faction to have existing objectives, found none."
            )

        clock_controller = FactionClockController(faction_clock=clock)

        roll = Outcome.roll(dice)
        match roll:
            case Outcome.FAILURE:
                return clock_controller.increment_clock(1)
            case Outcome.PARTIAL_SUCCESS:
                return clock_controller.increment_clock(2)
            case Outcome.SUCCESS:
                return clock_controller.increment_clock(3)
            case Outcome.CRITICAL_SUCCESS:
                return clock_controller.increment_clock(5)
