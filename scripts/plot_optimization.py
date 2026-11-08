import csv
from pathlib import Path
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[1]

CSV_FILE = BASE_DIR / "results" / "analysis" / "optimization_50m.csv"
FIGURE_DIR = BASE_DIR / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

optimization = []
execution_times = []
std_deviations = []

with open(CSV_FILE, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        optimization.append(row["Optimization"])
        execution_times.append(float(row["Mean_seconds"]))
        std_deviations.append(float(row["Std_dev_seconds"]))

plt.figure(figsize=(9, 6))

bars = plt.bar(
    optimization,
    execution_times,
    yerr=std_deviations,
    capsize=7,
    error_kw={"elinewidth": 1.5}
)

plt.title("Effect of Compiler Optimization on DNA Analysis")
plt.xlabel("Compiler Optimization Level")
plt.ylabel("Mean Execution Time (seconds)")
plt.grid(axis="y", alpha=0.3)

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.04,
        f"{height:.3f} s",
        ha="center",
        va="bottom"
    )

plt.ylim(
    0,
    max(
        mean + sd
        for mean, sd in zip(execution_times, std_deviations)
    ) + 0.25
)

plt.tight_layout()

output_file = FIGURE_DIR / "compiler_optimization_50m.png"

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"Optimization figure saved to: {output_file}")
