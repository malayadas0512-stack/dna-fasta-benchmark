import json
import csv
from pathlib import Path

# Locate the repository root
BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = BASE_DIR / "results" / "raw"
OUTPUT_DIR = BASE_DIR / "results" / "analysis"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Dataset sizes in millions of nucleotide bases
experiments = {
    "1M": ("benchmark_1m.json", 1),
    "10M": ("benchmark_10m.json", 10),
    "50M": ("benchmark_50m.json", 50),
    "50M_repeat": ("benchmark_50m_repeat.json", 50),
    "100M": ("benchmark_100m.json", 100),
}

all_results = []

for experiment, (filename, bases_millions) in experiments.items():

    filepath = RAW_DIR / filename

    with open(filepath, "r") as file:
        data = json.load(file)

    cpp = None
    python = None

    for result in data["results"]:
        command = result["command"]

        if "dna_bench analyze" in command:
            cpp = result
        elif "dna_benchmark.py" in command:
            python = result

    if cpp is None or python is None:
        raise ValueError(f"Missing C++ or Python result in {filename}")

    speedup = python["mean"] / cpp["mean"]

    cpp_throughput = bases_millions / cpp["mean"]
    python_throughput = bases_millions / python["mean"]

    cpp_cv = (cpp["stddev"] / cpp["mean"]) * 100
    python_cv = (python["stddev"] / python["mean"]) * 100

    row = {
        "experiment": experiment,
        "dataset_Mbases": bases_millions,
        "cpp_mean_s": cpp["mean"],
        "cpp_median_s": cpp["median"],
        "cpp_stddev_s": cpp["stddev"],
        "cpp_min_s": cpp["min"],
        "cpp_max_s": cpp["max"],
        "cpp_throughput_Mbases_s": cpp_throughput,
        "cpp_cv_percent": cpp_cv,
        "python_mean_s": python["mean"],
        "python_median_s": python["median"],
        "python_stddev_s": python["stddev"],
        "python_min_s": python["min"],
        "python_max_s": python["max"],
        "python_throughput_Mbases_s": python_throughput,
        "python_cv_percent": python_cv,
        "cpp_speedup": speedup,
    }

    all_results.append(row)

output_file = OUTPUT_DIR / "benchmark_analysis.csv"

with open(output_file, "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=all_results[0].keys()
    )
    writer.writeheader()
    writer.writerows(all_results)

print("\nDNA FASTA BENCHMARK ANALYSIS")
print("=" * 75)

print(f"{'Dataset':<15}{'C++ (s)':<15}{'Python (s)':<15}{'Speedup':<12}")
print("-" * 75)

for row in all_results:
    print(
        f"{row['experiment']:<15}"
        f"{row['cpp_mean_s']:<15.4f}"
        f"{row['python_mean_s']:<15.4f}"
        f"{row['cpp_speedup']:<12.2f}x"
    )

print("\nTHROUGHPUT (MILLION BASES/SECOND)")
print("=" * 75)

for row in all_results:
    print(
        f"{row['experiment']:<15}"
        f"C++: {row['cpp_throughput_Mbases_s']:.2f} | "
        f"Python: {row['python_throughput_Mbases_s']:.2f}"
    )

print("\nAnalysis completed successfully.")
print(f"CSV saved to: {output_file}")
