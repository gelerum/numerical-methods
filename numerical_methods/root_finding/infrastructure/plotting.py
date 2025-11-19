from ..application.dto import ResidualCurveDTO
import matplotlib.pyplot as plt


def plot_residual_vs_time(curves: dict[str, ResidualCurveDTO]) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    for method_name, curve in curves.items():
        ax1.plot(curve.times, curve.residuals, label=method_name, linewidth=2)
    ax1.set_title("Residual vs Time (linear scale)")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("|f(x)|")
    ax1.grid(True, linestyle="--", linewidth=0.5)
    ax1.legend()

    for method_name, curve in curves.items():
        ax2.plot(curve.times, curve.residuals, label=method_name, linewidth=2)
    ax2.set_yscale("log")
    ax2.set_title("Residual vs Time (log scale)")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("|f(x)|")
    ax2.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax2.legend()

    plt.tight_layout()
    plt.show()
