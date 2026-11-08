
import sys

def analyse_fasta(filename):
    counts = {
        "A": 0,
        "T": 0,
        "G": 0,
        "C": 0,
        "N": 0,
        "other": 0
    }

    with open(filename, "r") as fasta:
        for line in fasta:
            # Skip FASTA header lines
            if line.startswith(">"):
                continue

            # Count bases one character at a time
            for base in line.strip().upper():
                if base in counts:
                    counts[base] += 1
                else:
                    counts["other"] += 1

    # Total canonical and ambiguous bases, matching C++ logic
    total = (
        counts["A"] + counts["T"] +
        counts["G"] + counts["C"] +
        counts["N"]
    )

    canonical = (
        counts["A"] + counts["T"] +
        counts["G"] + counts["C"]
    )

    gc_content = (
        (counts["G"] + counts["C"]) / canonical * 100
        if canonical > 0 else 0.0
    )

    print(f"Adenine (A):   {counts['A']}")
    print(f"Thymine (T):   {counts['T']}")
    print(f"Guanine (G):   {counts['G']}")
    print(f"Cytosine (C):  {counts['C']}")
    print(f"Ambiguous (N): {counts['N']}")
    print(f"Other symbols: {counts['other']}")
    print(f"Total bases:   {total}")
    print(f"GC Content:    {gc_content:.2f}%")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 dna_benchmark.py <input.fasta>")
        sys.exit(1)

    analyse_fasta(sys.argv[1])
