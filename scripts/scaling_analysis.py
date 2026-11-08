import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CSV_FILE = BASE_DIR / "results" / "analysis" / "benchmark_analysis.csv"

with open(CSV_FILE, "r") as file:
    data = list(csv.DictReader(file))

# Exclude repeated 50M experiment from scaling analysis
data = [
    row for row in data
    if row["experiment"] != "50M_repeat"
]

print("\nDNA FASTA SCALING ANALYSIS")
print("=" * 85)

previous = None

for row in data:
    size = float(row["dataset_Mbases"])
    cpp_time = float(row["cpp_mean_s"])
    python_time = float(row["python_mean_s"])

    cpp_normalized = cpp_time / size
    python_normalized = python_time / size

    print(f"\nDataset: {row['experiment']}")
    print(f"C++ time per million bases: {cpp_normalized:.5f} s")
    print(f"Python time per million bases: {python_normalized:.5f} s")

    if previous is not None:
        cpp_scale = cpp_time / previous[1]
        python_scale = python_time / previous[2]
        size_scale = size / previous[0]

        print(f"Input size increase: {size_scale:.2f}x")
        print(f"C++ execution increase: {cpp_scale:.2f}x")
        print(f"Python execution increase: {python_scale:.2f}x")

    previous = (size, cpp_time, python_time)

print("\nScaling analysis completed.")
