from dataclasses import dataclass


@dataclass
class Iteration:
    index: int
    x: float
    fx: float
