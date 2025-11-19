from dataclasses import dataclass


@dataclass
class SolverConfig:
    eps: float
    max_iterations: int = -1
