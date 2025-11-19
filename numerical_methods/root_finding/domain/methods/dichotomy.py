from typing import Iterable
from ..models.iteration import Iteration
from .root_solver import RootSolver
from ...domain.models.problem import Problem


class DichotomySolver(RootSolver):
    def iterate(self, problem: Problem) -> Iterable[Iteration]:
        if problem.interval is None:
            raise ValueError("interval (a, b) must be set")

        f = problem.f
        a = problem.interval.a
        b = problem.interval.b

        max_iterations = self.config.max_iterations
        eps = self.config.eps

        if f(a) * f(b) > 0:
            raise ValueError("f(a) and f(b) must have opposite signs")

        iterations = 0

        while b - a > eps and (max_iterations == -1 or iterations < max_iterations):
            c = (b + a) / 2

            iterations += 1

            fa, fc = f(a), f(c)

            it = Iteration(index=iterations, x=c, fx=fc)
            self._notify_observers(it)
            yield it

            match (
                fa * fc < 0,
                fa * fc > 0,
                fa * fc == 0,
            ):
                case (True, False, False):
                    b = c
                case (False, True, False):
                    a = c
                case (False, False, True):
                    break
                case _:
                    pass
