from typing import Optional
from dataclasses import dataclass

from ..models.root_multiplicity import RootMultiplicity
from ..models.two_guesses import TwoGuesses
from ..models.function import Function
from ..models.interval import Interval
from ..models.one_guess import OneGuess


@dataclass
class Problem:
    f: Function
    interval: Optional[Interval] = None
    one_guess: Optional[OneGuess] = None
    two_guesses: Optional[TwoGuesses] = None
    root_multiplicity: Optional[RootMultiplicity] = None

    def __post_init__(self):
        if (
            self.interval is None
            and self.one_guess is None
            and self.two_guesses is None
        ):
            raise ValueError("Define interval or initial guesses")
