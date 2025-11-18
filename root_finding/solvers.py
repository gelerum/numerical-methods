from abc import ABC, abstractmethod
from time import perf_counter
from typing import Any, List

import numpy as np
from root_finding.base import SolveResult
from root_finding.function import Function


class RootSolver(ABC):
    def __init__(self, f: Function, eps: float, max_iterations: int = -1):
        self.f = f
        self.eps = eps
        self.max_iterations = max_iterations

    @abstractmethod
    def solve(self, *args: Any, **kwargs: Any) -> SolveResult:
        pass


class DichotomySolver(RootSolver):
    def solve(self, a: float, b: float) -> SolveResult:
        if self.f(a) * self.f(b) > 0:
            raise ValueError("f(a) and f(b) must have opposite signs")

        iterations = 0
        approximations: List[float] = []
        residuals: List[float] = []
        times: List[float] = []

        start = perf_counter()

        while b - a > self.eps and (
            self.max_iterations == -1 or iterations < self.max_iterations
        ):
            c = (b + a) / 2

            iterations += 1
            approximations.append(c)
            residuals.append(np.abs(self.f(c)))
            end = perf_counter()
            times.append(end - start)
            fa, fc = self.f(a), self.f(c)

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
                    return SolveResult(
                        root=c,
                        iterations=iterations,
                        approximations=approximations,
                        residuals=residuals,
                        times=times,
                    )
                case _:
                    pass

        return SolveResult(
            root=a,
            iterations=iterations,
            approximations=approximations,
            residuals=residuals,
            times=times,
        )


class RegulaFalsiSolver(RootSolver):
    def solve(self, a: float, b: float) -> SolveResult:
        fa = self.f(a)
        fb = self.f(b)

        if fa * fb > 0:
            raise ValueError("f(a) and f(b) must have opposite signs")

        ea = 100.0
        c = b

        iterations = 0
        approximations: List[float] = []
        residuals: List[float] = []
        times: List[float] = []

        start = perf_counter()

        while self.max_iterations == -1 or iterations < self.max_iterations:
            c_prev = c
            c = b - fb * (a - b) / (fa - fb)
            fc = self.f(c)
            iterations += 1
            approximations.append(c)
            residuals.append(np.abs(self.f(c)))
            end = perf_counter()
            times.append(end - start)

            if c != 0:
                ea = np.abs(c - c_prev)

            test = fa * fc
            if test < 0:
                b = c
                fb = fc
            elif test > 0:
                a = c
                fa = fc
            else:
                ea = 0

            if ea < self.eps:
                break

        return SolveResult(
            root=c,
            iterations=iterations,
            approximations=approximations,
            residuals=residuals,
            times=times,
        )


class RegulaFalsiModifiedSolver(RootSolver):
    def solve(self, a: float, b: float) -> SolveResult:
        fa = self.f(a)
        fb = self.f(b)

        if fa * fb > 0:
            raise ValueError("f(a) and f(b) must have opposite signs")

        ea = 100.0
        c = b
        iterations_a = 0
        iterations_b = 0

        iterations = 0
        approximations: List[float] = []
        residuals: List[float] = []
        times: List[float] = []

        start = perf_counter()

        while self.max_iterations == -1 or iterations < self.max_iterations:
            c_prev = c
            c = b - fb * (a - b) / (fa - fb)
            fc = self.f(c)
            iterations += 1
            approximations.append(c)
            residuals.append(np.abs(self.f(c)))
            end = perf_counter()
            times.append(end - start)

            if c != 0:
                ea = np.abs(c - c_prev)

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

            if ea < self.eps:
                break

        return SolveResult(
            root=c,
            iterations=iterations,
            approximations=approximations,
            residuals=residuals,
            times=times,
        )


class NewtonSolver(RootSolver):
    def solve(self, x0: float) -> SolveResult:
        iterations = 0
        approximations: List[float] = []
        residuals: List[float] = []
        times: List[float] = []

        start = perf_counter()

        while True:
            x1 = x0 - self.f(x0) / self.f.derivative(x0)

            iterations += 1
            approximations.append(x1)
            residuals.append(np.abs(self.f(x1)))
            end = perf_counter()
            times.append(end - start)

            if np.abs(x0 - x1) < self.eps or (
                iterations >= self.max_iterations and self.max_iterations != -1
            ):
                break
            x0 = x1

        return SolveResult(
            root=x1,
            iterations=iterations,
            approximations=approximations,
            residuals=residuals,
            times=times,
        )


class SecantSolver(RootSolver):
    def solve(self, x0: float, x1: float) -> SolveResult:
        iterations = 0
        approximations: List[float] = []
        residuals: List[float] = []
        times: List[float] = []

        start = perf_counter()

        while True:
            fx0 = self.f(x0)
            fx1 = self.f(x1)

            x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)

            iterations += 1
            approximations.append(x1)
            residuals.append(np.abs(self.f(x2)))
            end = perf_counter()
            times.append(end - start)

            if np.abs(x2 - x1) < self.eps or (
                iterations >= self.max_iterations and self.max_iterations != -1
            ):
                break
            x0 = x1
            x1 = x2

        return SolveResult(
            root=x2,
            iterations=iterations,
            approximations=approximations,
            residuals=residuals,
            times=times,
        )


class SteffensensSolver(RootSolver):
    def solve(self, x0: float) -> SolveResult:
        iterations = 0
        approximations: List[float] = []
        residuals: List[float] = []
        times: List[float] = []

        start = perf_counter()

        while True:
            fx0 = self.f(x0)
            x1 = x0 - self.f(x0) * self.f(x0) / (self.f(x0 + fx0) - fx0)

            iterations += 1
            approximations.append(x1)
            residuals.append(np.abs(self.f(x1)))
            end = perf_counter()
            times.append(end - start)

            if np.abs(x0 - x1) < self.eps or (
                iterations >= self.max_iterations and self.max_iterations != -1
            ):
                break
            x0 = x1

        return SolveResult(
            root=x1,
            iterations=iterations,
            approximations=approximations,
            residuals=residuals,
            times=times,
        )
