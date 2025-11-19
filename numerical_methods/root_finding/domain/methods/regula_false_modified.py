from collections.abc import Iterable

from ..models.iteration import Iteration
from ..methods.root_solver import RootSolver
from ..models.problem import Problem


class RegulaFalsiModifiedSolver(RootSolver):
    def iterate(self, problem: Problem) -> Iterable[Iteration]:
        if problem.interval is None:
            raise ValueError("interval (a, b) must be set")

        f = problem.f
        a = problem.interval.a
        b = problem.interval.b

        max_iterations = self.config.max_iterations
        eps = self.config.eps

        fa = f(a)
        fb = f(b)

        if fa * fb > 0:
            raise ValueError("f(a) and f(b) must have opposite signs")

        ea = 100.0
        c = b
        iterations_a = 0
        iterations_b = 0

        iterations = 0

        while max_iterations == -1 or iterations < max_iterations:
            c_prev = c
            c = b - fb * (a - b) / (fa - fb)
            fc = f(c)
            iterations += 1

            it = Iteration(index=iterations, x=c, fx=fc)
            self._notify_observers(it)
            yield it

            if c != 0:
                ea = abs(c - c_prev)

            test = fa * fc
            if test < 0:
                b = c
                fb = fc
                iterations_a = 0
                iterations_b += 1
                if iterations_b >= 2:
                    fa /= 2
            elif test > 0:
                a = c
                fa = fc
                iterations_b = 0
                iterations_a += 1
                if iterations_a >= 2:
                    fb /= 2
            else:
                ea = 0

            if ea < eps:
                break
