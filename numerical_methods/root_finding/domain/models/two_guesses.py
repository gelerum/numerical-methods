from dataclasses import dataclass


@dataclass
class TwoGuesses:
    x0: float
    x1: float

    def __post_init__(self):
        if self.x0 == self.x1:
            ValueError("x1, x2 must be different")
