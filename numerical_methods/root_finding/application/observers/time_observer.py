from typing import List
from ..observers.iteration_observer import IterationObserver
from ...domain.models.iteration import Iteration
from ...infrastructure.timing.timer import Timer


class TimeObserver(IterationObserver):
    def __init__(self, timer: Timer):
        self._timer = timer
        self.times: List[float] = []
        self._start_time = None

    def on_iteration(self, iteration: Iteration) -> None:
        now = self._timer.now()
        if self._start_time is None:
            self._start_time = now

        self.times.append(self._timer.now() - self._start_time)
