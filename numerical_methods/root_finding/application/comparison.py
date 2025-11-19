from typing import Dict

from .comparison_result import ComparisonResult, ComparisonResultElement
from .dto import FunctionAtApproximationsCurveDTO, ResidualCurveDTO
from .root_finding import RootFindingService

from ..domain.methods.root_solver import RootSolver
from ..domain.models.problem import Problem
from ..infrastructure.timing.timer import Timer


class ComparisonService:
    def __init__(self, timer: Timer):
        self._timer = timer

    def compare(
        self, methods: Dict[str, RootSolver], problem: Problem
    ) -> ComparisonResult:
        comparison: list[ComparisonResultElement] = []
        for solver_name, solver in methods.items():
            result = RootFindingService(solver, self._timer).find_root(problem)
            residual_curve = ResidualCurveDTO(
                residuals=result.residuals,
                times=result.times,
            )
            f_approximation_curve = FunctionAtApproximationsCurveDTO(
                f_at_approximations=[problem.f(x) for x in result.approximations],
                approximations=result.approximations,
            )
            comparison.append(
                ComparisonResultElement(
                    method_name=solver_name,
                    root=result.root,
                    residual_curve=residual_curve,
                    iterations=result.iterations,
                    f_approximation_curve=f_approximation_curve,
                )
            )

        return ComparisonResult(comparison)
