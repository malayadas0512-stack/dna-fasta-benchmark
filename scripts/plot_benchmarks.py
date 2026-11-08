import csv
from pathlib import Path
import matplotlib.pyplot as plt

# Locate repository directories
BASE_DIR = Path(__file__).resolve().parents[1]
CSV_FILE = BASE_DIR / "results" / "analysis" / "benchmark_analysis.csv"
FIGURE_DIR = BASE_DIR / "figures"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# Read benchmark data
with open(CSV_FILE, "r", newline="") as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Exclude repeated 50M experiment from scaling plots
data = [
    row for row in data
    if row["experiment"] != "50M_repeat"
]

data.sort(key=lambda row: float(row["dataset_Mbases"]))

sizes = [float(row["dataset_Mbases"]) for row in data]

cpp_times = [float(row["cpp_mean_s"]) for row in data]
python_times = [float(row["python_mean_s"]) for row in data]

cpp_throughput = [
    float(row["cpp_throughput_Mbases_s"]) for row in data
]
python_throughput = [
    float(row["python_throughput_Mbases_s"]) for row in data
]

# Graph 1: Execution time vs dataset size
plt.figure(figsize=(9, 6))

plt.plot(sizes, cpp_times, marker="o", label="C++")
plt.plot(sizes, python_times, marker="s", label="Python")

plt.xlabel("Dataset Size (Million Bases)")
plt.ylabel("Mean Execution Time (seconds)")
plt.title("C++ vs Python: Execution Time")

plt.yscale("log")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(FIGURE_DIR / "execution_time_vs_dataset.png", dpi=300)
plt.close()

# Graph 2: Throughput vs dataset size
plt.figure(figsize=(9, 6))

plt.plot(sizes, cpp_throughput, marker="o", label="C++")
plt.plot(sizes, python_throughput, marker="s", label="Python")

plt.xlabel("Dataset Size (Million Bases)")
plt.ylabel("Throughput (Million Bases/Second)")
plt.title("C++ vs Python: Processing Throughput")

plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(FIGURE_DIR / "throughput_vs_dataset.png", dpi=300)
plt.close()

# Graph 3: Input growth vs execution time growth
transitions = ["1M to 10M", "10M to 50M", "50M to 100M"]
input_ratios = [10, 5, 2]

cpp_ratios = []
python_ratios = []

for i in range(1, len(sizes)):
    cpp_ratios.append(cpp_times[i] / cpp_times[i - 1])
    python_ratios.append(python_times[i] / python_times[i - 1])

x = list(range(len(transitions)))
width = 0.25

plt.figure(figsize=(10, 6))

plt.bar(
    [i - width for i in x],
    input_ratios,
    width,
    label="Input Size Ratio"
)

plt.bar(x, cpp_ratios, width, label="C++ Time Ratio")

plt.bar(
    [i + width for i in x],
    python_ratios,
    width,
    label="Python Time Ratio"
)

plt.xticks(x, transitions)
plt.xlabel("Dataset Size Transition")
plt.ylabel("Growth Ratio")
plt.title("Input Growth vs Execution Time Growth")

plt.legend()
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(FIGURE_DIR / "scaling_ratios.png", dpi=300)
plt.close()

print("\nAll three benchmark graphs generated successfully!")
print("\nSaved figures:")

for file in sorted(FIGURE_DIR.glob("*.png")):
    print(file)
