#include <iostream>
#include <fstream>
#include <string>
#include <random>
#include <cctype>
#include <cstdint>
#include <iomanip>

using namespace std;

struct DNAStats
{
    uint64_t A = 0;
    uint64_t T = 0;
    uint64_t G = 0;
    uint64_t C = 0;
    uint64_t N = 0;
    uint64_t other = 0;
};

// Analyse a DNA sequence
void countBases(const string& sequence, DNAStats& stats)
{
    for (unsigned char base : sequence)
    {
        switch (toupper(base))
        {
            case 'A': stats.A++; break;
            case 'T': stats.T++; break;
            case 'G': stats.G++; break;
            case 'C': stats.C++; break;
            case 'N': stats.N++; break;
            default: stats.other++; break;
        }
    }
}

// Generate a random DNA FASTA file
void generateDNA(uint64_t length, const string& filename)
{
    ofstream file(filename);

    if (!file)
    {
        cerr << "Error creating FASTA file.\n";
        return;
    }

    mt19937 rng(42);
    const char bases[] = {'A', 'T', 'G', 'C'};

    file << ">Random_DNA_Sequence\n";

    for (uint64_t i = 0; i < length; i++)
    {
        file << bases[rng() % 4];

        if ((i + 1) % 60 == 0)
            file << '\n';
    }

    file << '\n';

    cout << "Generated " << length
         << " DNA bases successfully.\n";

    cout << "Saved to: " << filename << '\n';
}

// Analyse a FASTA file
void analyseFASTA(const string& filename)
{
    ifstream file(filename);

    if (!file)
    {
        cerr << "Error opening FASTA file.\n";
        return;
    }

    DNAStats stats;
    string line;

    while (getline(file, line))
    {
        // Ignore FASTA header lines
        if (!line.empty() && line[0] == '>')
            continue;

        countBases(line, stats);
    }

    uint64_t total = stats.A + stats.T +
                     stats.G + stats.C + stats.N;

    uint64_t canonical = stats.A + stats.T +
                         stats.G + stats.C;

    double gcContent = 0.0;

    if (canonical > 0)
    {
        gcContent = (double)(stats.G + stats.C)
                    / canonical * 100.0;
    }

    cout << fixed << setprecision(2);

    cout << "\n===== DNA ANALYSIS RESULTS =====\n";

    cout << "Adenine (A):   " << stats.A << '\n';
    cout << "Thymine (T):   " << stats.T << '\n';
    cout << "Guanine (G):   " << stats.G << '\n';
    cout << "Cytosine (C):  " << stats.C << '\n';
    cout << "Ambiguous (N): " << stats.N << '\n';

    cout << "Other symbols: " << stats.other << '\n';

    cout << "Total bases:   " << total << '\n';

    cout << "GC Content:    "
         << gcContent << "%\n";

    cout << "===============================\n";
}

int main(int argc, char* argv[])
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (argc < 2)
    {
        cout << "Usage:\n";
        cout << "./dna_bench generate <length> <output.fasta>\n";
        cout << "./dna_bench analyze <input.fasta>\n";
        return 1;
    }

    string mode = argv[1];

    if (mode == "generate" && argc == 4)
    {
        uint64_t length = stoull(argv[2]);

        generateDNA(length, argv[3]);
    }
    else if (mode == "analyze" && argc == 3)
    {
        analyseFASTA(argv[2]);
    }
    else
    {
        cout << "Invalid arguments.\n";
        return 1;
    }

    return 0;
}
