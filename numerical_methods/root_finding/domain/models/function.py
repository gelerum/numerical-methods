from typing import Callable


class DerivateIsNotDefined(Exception):
    pass


class Function:
    def __init__(
        self,
        name: str,
        f: Callable[[float], float],
        df: Callable[[float], float] = None,
    ) -> None:
        self.name = name
        self.f = f
        self.df = df

    def __call__(self, x: float) -> float:
        return self.f(x)

    def derivative(self, x: float) -> float:
        if self.df is not None:
            return self.df(x)
        else:
            raise DerivateIsNotDefined(f"For function {self.name}")
