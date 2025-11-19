from abc import ABC, abstractmethod
from typing import Iterable

from ...application.observers.iteration_observer import IterationObserver
from ..models.iteration import Iteration
from ..models.problem import Problem
from ..models.solver_config import SolverConfig


class RootSolver(ABC):
    def __init__(self, config: SolverConfig):
        self.config = config
        self._observers = []

    @abstractmethod
    def iterate(self, problem: Problem) -> Iterable[Iteration]:
        pass

    def add_observer(self, observer: IterationObserver) -> None:
        self._observers.append(observer)

    def _notify_observers(self, iteration: Iteration) -> None:
        for observer in self._observers:
            observer.on_iteration(iteration)
