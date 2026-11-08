#!/usr/bin/env bash

set -euo pipefail

# Locate repository root
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

# Create output directories
mkdir -p build datasets/generated

echo "Compiling C++ DNA benchmark..."

g++ -O2 -std=c++17 -Wall -Wextra \
    src/dna_benchmark.cpp \
    -o build/dna_bench

echo "Generating random FASTA datasets..."

./build/dna_bench generate 1000000 datasets/generated/random_1m.fasta

./build/dna_bench generate 10000000 datasets/generated/random_10m.fasta

./build/dna_bench generate 50000000 datasets/generated/random_50m.fasta

./build/dna_bench generate 100000000 datasets/generated/random_100m.fasta

echo "All datasets generated successfully."
echo "Output directory: datasets/generated/"
