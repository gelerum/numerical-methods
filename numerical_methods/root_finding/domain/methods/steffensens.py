from collections.abc import Iterable

from ..models.iteration import Iteration
from .root_solver import RootSolver
from ..models.problem import Problem


class SteffensensSolver(RootSolver):
    def iterate(self, problem: Problem) -> Iterable[Iteration]:
        if problem.one_guess is None:
            raise ValueError("one initial guess must be set")

        f = problem.f
        x0 = problem.one_guess.x0

        max_iterations = self.config.max_iterations
        eps = self.config.eps

        iterations = 0

        while True:
            fx0 = f(x0)
            x1 = x0 - fx0 * fx0 / (f(x0 + fx0) - fx0)

            iterations += 1

            it = Iteration(index=iterations, x=x1, fx=f(x1))
            self._notify_observers(it)
            yield it

            if abs(x0 - x1) < eps or (
                iterations >= max_iterations and max_iterations != -1
            ):
                break
            x0 = x1
