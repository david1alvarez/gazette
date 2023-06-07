from city_manager.controllers.faction_clock import FactionClockController
from city_manager.controllers.probability import Outcome
from city_manager.models import Faction, FactionClock
from logging import error


class FactionController:
    def __init__(self, faction: Faction):
        self.faction = faction

    def _get_roll_increment(self, dice: int = 1) -> int:
        roll = Outcome.roll(dice)
        match roll:
            case Outcome.FAILURE:
                return 1
            case Outcome.PARTIAL_SUCCESS:
                return 2
            case Outcome.SUCCESS:
                return 3
            case Outcome.CRITICAL_SUCCESS:
                return 5

    def _get_active_clock(self) -> FactionClock:
        clock = (
            FactionClock.objects.active()
            .filter(faction=self.faction)
            .order_by("?")
            .first()
        )
        if clock is None:
            raise FactionClock.DoesNotExist(
                "Expected faction to have existing objectives, found none."
            )

    def roll_clock(self, dice=1) -> FactionClock:
        """Roll the advancement of one of the faction's clocks

        Args:
            dice (int, optional): The number of dice that will be simulated in rolling the faction's clock's advancement. Defaults to 1.
            clock_id (int, optional): The id of the clock to advance. Leave as None to select randomly. Defaults to None.

        Returns:
            FactionClock: The FactionClock that was rolled
        """
        clock = self._get_active_clock()

        clock_controller = FactionClockController(faction_clock=clock)

        increment = self._get_roll_increment(dice)
        clock_controller.increment_clock(increment)

        return clock
