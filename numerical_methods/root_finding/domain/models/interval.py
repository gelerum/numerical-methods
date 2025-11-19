from dataclasses import dataclass


@dataclass
class Interval:
    a: float
    b: float

    def __post_init__(self):
        if self.a == self.b:
            ValueError("a, b must be different")
