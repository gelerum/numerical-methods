from .observers.time_observer import TimeObserver
from .root_finding_result import RootFindingResult
from ..domain.methods.root_solver import RootSolver
from ..domain.models.problem import Problem
from ..infrastructure.timing.timer import Timer


class RootFindingService:
    def __init__(self, solver: RootSolver, timer: Timer) -> None:
        self.solver: RootSolver = solver
        self.timer: Timer = timer

    def find_root(self, problem: Problem) -> RootFindingResult:
        time_observer = TimeObserver(self.timer)
        self.solver.add_observer(time_observer)

        approximations: list[float] = []
        residuals: list[float] = []

        for i in self.solver.iterate(problem):
            approximations.append(i.x)
            residuals.append(abs(i.fx))

        return RootFindingResult(
            root=approximations[-1],
            iterations=len(approximations),
            approximations=approximations,
            residuals=residuals,
            times=time_observer.times,
        )
