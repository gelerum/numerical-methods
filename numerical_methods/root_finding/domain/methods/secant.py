from collections.abc import Iterable

from ..models.iteration import Iteration
from .root_solver import RootSolver
from ..models.problem import Problem


class SecantSolver(RootSolver):
    def iterate(self, problem: Problem) -> Iterable[Iteration]:
        if problem.two_guesses is None:
            raise ValueError("two initial guesses must be set")

        f = problem.f
        x0 = problem.two_guesses.x0
        x1 = problem.two_guesses.x1

        max_iterations = self.config.max_iterations
        eps = self.config.eps
        iterations = 0

        while True:
            fx0 = f(x0)

            fx1 = f(x1)

            x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)

            iterations += 1

            it = Iteration(index=iterations, x=x2, fx=f(x2))
            self._notify_observers(it)
            yield it

            if abs(x2 - x1) < eps or (
                iterations >= max_iterations and max_iterations != -1
            ):
                break

            x0 = x1

            x1 = x2
