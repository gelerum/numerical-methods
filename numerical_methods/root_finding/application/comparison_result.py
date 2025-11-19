from dataclasses import dataclass

from ..application.dto import FunctionAtApproximationsCurveDTO, ResidualCurveDTO


@dataclass
class ComparisonResultElement:
    method_name: str
    root: float
    residual_curve: ResidualCurveDTO
    f_approximation_curve: FunctionAtApproximationsCurveDTO
    iterations: int


@dataclass
class ComparisonResult:
    comparison: list[ComparisonResultElement]
