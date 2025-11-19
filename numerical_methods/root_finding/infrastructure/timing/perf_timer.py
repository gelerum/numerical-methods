from time import perf_counter

from .timer import Timer


class PerfTimer(Timer):
    def now(self) -> float:
        return perf_counter()
