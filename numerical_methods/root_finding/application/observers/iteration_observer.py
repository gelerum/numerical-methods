from abc import ABC, abstractmethod

from ...domain.models.iteration import Iteration


class IterationObserver(ABC):
    @abstractmethod
    def on_iteration(self, iteration: Iteration) -> None:
        pass
