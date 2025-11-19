from dataclasses import dataclass
from typing import List


@dataclass
class ResidualCurveDTO:
    residuals: List[float]
    times: List[float]
