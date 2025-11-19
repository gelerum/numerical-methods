from typing import Iterable

from ...domain.models.iteration import Iteration
from ...domain.methods.root_solver import RootSolver
from ...domain.models.problem import Problem


class NewtonRefinedSolver(RootSolver):
    def iterate(self, problem: Problem) -> Iterable[Iteration]:
        if problem.one_guess is None:
            raise ValueError("one initial guess must be set")
        if problem.root_multiplicity is None:
            raise ValueError("root exponent must be set")

        f = problem.f
        x0 = problem.one_guess.x0
        m = problem.root_multiplicity.m

        max_iterations = self.config.max_iterations
        eps = self.config.eps

        iterations = 0

        while True:
            x1 = x0 - m * f(x0) / f.derivative(x0)

            iterations += 1

            it = Iteration(index=iterations, x=x1, fx=f(x1))
            self._notify_observers(it)
            yield it

            if abs(x0 - x1) < eps or (
                iterations >= max_iterations and max_iterations != -1
            ):
                break
            x0 = x1
