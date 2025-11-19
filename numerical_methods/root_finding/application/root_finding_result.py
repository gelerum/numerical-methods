from dataclasses import dataclass
from typing import List


@dataclass
class RootFindingResult:
    root: float
    iterations: int
    approximations: List[float]
    residuals: List[float]
    times: List[float]
