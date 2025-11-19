from abc import ABC, abstractmethod


class Timer(ABC):
    @abstractmethod
    def now(self) -> float:
        pass
