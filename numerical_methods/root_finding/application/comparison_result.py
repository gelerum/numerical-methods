from dataclasses import dataclass
from typing import Dict, List

from ..application.dto import ResidualCurveDTO


@dataclass
class ComparisonResultElement:
    method_name: str
    root: float
    residual_curve: ResidualCurveDTO
    iterations: int


@dataclass
class ComparisonResult:
    comparison: list[ComparisonResultElement]
