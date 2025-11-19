from dataclasses import dataclass
from typing import List


@dataclass
class ResidualCurveDTO:
    residuals: List[float]
    times: List[float]


@dataclass
class FunctionAtApproximationsCurveDTO:
    f_at_approximations: list[float]
    approximations: List[float]
