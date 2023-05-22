from __future__ import annotations
import random
from enum import Enum


class Outcome(Enum):
    FAILURE = 1
    PARTIAL_SUCCESS = 2
    SUCCESS = 3
    CRITICAL_SUCCESS = 4

    def roll(dice_count: int) -> Outcome:
        """Simulate dice rolls and calculate the roll's success category

        Args:
            dice_count (int): The number of dice rolled. dice_count < 1 results in a roll with disadvantage.

        Returns:
            Outcome: The success category of the roll
        """
        roll: int
        num_sixes: int
        if dice_count <= 0:
            results = [random.randint(1, 6), random.randint(1, 6)]
            roll = min(results)
            if roll == 6:
                num_sixes = 1
            else:
                num_sixes = 0
        else:
            results = [random.randint(1, 6) for _ in range(dice_count)]
            num_sixes = results.count(6)
            roll = max(results)

        if roll > 0 and roll <= 3:
            return Outcome.FAILURE
        elif roll > 3 and roll <= 5:
            return Outcome.PARTIAL_SUCCESS
        else:
            if num_sixes > 1:
                return Outcome.CRITICAL_SUCCESS
            else:
                return Outcome.SUCCESS
