"""
Empirical Benchmark and Complexity Analysis of Boyer-Moore Algorithm
Course: Design and Analysis of Algorithms (DAA) - CIA 3 Component 1
Topic: Unit-4 String Matching

This script performs empirical experiments comparing:
1. Boyer-Moore (BM)
2. Knuth-Morris-Pratt (KMP)
3. Naive Brute-Force Matching

Experiments:
- Exp 1: Number of Comparisons vs. Pattern Length (Sublinear Property: O(n/m))
- Exp 2: Wall-Clock Execution Time vs. Text Length (Scalability)
- Exp 3: Impact of Alphabet Size (|Σ|) on Comparisons
- Exp 4: Best-Case, Average-Case, and Worst-Case Comparison Ratios

Generates scientific plots saved in 'results/' directory.
"""

import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
import random
import string
import time
import csv
import matplotlib.pyplot as plt
import numpy as np

from boyer_moore import BoyerMoore, naive_string_match, kmp_string_match


# Ensure output directory exists
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# Set random seed for reproducible academic results
random.seed(42)
np.random.seed(42)

# Set matplotlib aesthetic styles
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.4
plt.rcParams["grid.linestyle"] = "--"


def generate_random_string(length: int, alphabet: str) -> str:
    return "".join(random.choices(alphabet, k=length))


# =====================================================================
# Experiment 1: Number of Comparisons vs. Pattern Length (m)
# =====================================================================
def experiment_pattern_length():
    print("\n--- Running Experiment 1: Comparisons vs. Pattern Length ---")
    text_len = 8000
    pattern_lengths = [4, 8, 12, 16, 20, 25, 30, 40, 50]
    alphabet = string.ascii_lowercase
    num_trials = 10

    bm_comps_avg = []
    kmp_comps_avg = []
    naive_comps_avg = []

    for m in pattern_lengths:
        bm_trials = []
        kmp_trials = []
        naive_trials = []

        for _ in range(num_trials):
            text = generate_random_string(text_len, alphabet)
            # Pick a pattern guaranteed to appear or random
            start_pos = random.randint(0, text_len - m)
            pattern = text[start_pos : start_pos + m]

            bm = BoyerMoore(pattern)
            _, bm_c, _ = bm.search(text)
            _, naive_c, _ = naive_string_match(text, pattern)
            _, kmp_c, _ = kmp_string_match(text, pattern)

            bm_trials.append(bm_c)
            kmp_trials.append(kmp_c)
            naive_trials.append(naive_c)

        bm_comps_avg.append(np.mean(bm_trials))
        kmp_comps_avg.append(np.mean(kmp_trials))
        naive_comps_avg.append(np.mean(naive_trials))

        print(f"Pattern Length m={m:2d} | BM: {bm_comps_avg[-1]:6.1f} | KMP: {kmp_comps_avg[-1]:6.1f} | Naive: {naive_comps_avg[-1]:6.1f}")

    # Plotting
    plt.figure(figsize=(9, 5.5), dpi=300)
    plt.plot(pattern_lengths, bm_comps_avg, "o-", color="#1d4ed8", linewidth=2.5, markersize=7, label="Boyer-Moore (Sublinear O(n/m))")
    plt.plot(pattern_lengths, kmp_comps_avg, "s--", color="#16a34a", linewidth=2, markersize=6, label="Knuth-Morris-Pratt (Linear O(n))")
    plt.plot(pattern_lengths, naive_comps_avg, "^:", color="#dc2626", linewidth=2, markersize=6, label="Naive Brute-Force (O(n·m))")

    plt.title("Impact of Pattern Length (m) on Character Comparisons\n(Fixed Text Length n = 8,000, English Alphabet |Σ|=26)", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Pattern Length (m)", fontsize=11, fontweight="bold")
    plt.ylabel("Average Number of Comparisons", fontsize=11, fontweight="bold")
    plt.legend(frameon=True, facecolor="white", edgecolor="#cbd5e1", fontsize=10)
    plt.tight_layout()

    out_path = os.path.join(RESULTS_DIR, "comparisons_vs_pattern_length.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Plot saved to: {out_path}")

    return {
        "pattern_lengths": pattern_lengths,
        "bm": bm_comps_avg,
        "kmp": kmp_comps_avg,
        "naive": naive_comps_avg,
    }


# =====================================================================
# Experiment 2: Execution Time vs. Text Length (n)
# =====================================================================
def experiment_text_length():
    print("\n--- Running Experiment 2: Runtime vs. Text Length ---")
    text_lengths = [2000, 5000, 10000, 20000, 40000, 80000]
    pattern_len = 12
    alphabet = string.ascii_lowercase
    num_trials = 5

    bm_times = []
    kmp_times = []
    naive_times = []

    for n in text_lengths:
        bm_trial_times = []
        kmp_trial_times = []
        naive_trial_times = []

        for _ in range(num_trials):
            text = generate_random_string(n, alphabet)
            pattern = generate_random_string(pattern_len, alphabet)

            # Benchmark Boyer-Moore
            t0 = time.perf_counter()
            bm = BoyerMoore(pattern)
            bm.search(text)
            t1 = time.perf_counter()
            bm_trial_times.append((t1 - t0) * 1000)  # ms

            # Benchmark KMP
            t0 = time.perf_counter()
            kmp_string_match(text, pattern)
            t1 = time.perf_counter()
            kmp_trial_times.append((t1 - t0) * 1000)  # ms

            # Benchmark Naive
            t0 = time.perf_counter()
            naive_string_match(text, pattern)
            t1 = time.perf_counter()
            naive_trial_times.append((t1 - t0) * 1000)  # ms

        bm_times.append(np.mean(bm_trial_times))
        kmp_times.append(np.mean(kmp_trial_times))
        naive_times.append(np.mean(naive_trial_times))

        print(f"Text Length n={n:5d} | BM: {bm_times[-1]:6.3f} ms | KMP: {kmp_times[-1]:6.3f} ms | Naive: {naive_times[-1]:6.3f} ms")

    # Plotting
    plt.figure(figsize=(9, 5.5), dpi=300)
    plt.plot(text_lengths, bm_times, "o-", color="#1d4ed8", linewidth=2.5, markersize=7, label="Boyer-Moore")
    plt.plot(text_lengths, kmp_times, "s--", color="#16a34a", linewidth=2, markersize=6, label="Knuth-Morris-Pratt")
    plt.plot(text_lengths, naive_times, "^:", color="#dc2626", linewidth=2, markersize=6, label="Naive Brute-Force")

    plt.title("Execution Time (ms) vs. Text Length (n)\n(Fixed Pattern Length m = 12, English Alphabet |Σ|=26)", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Text Length (n)", fontsize=11, fontweight="bold")
    plt.ylabel("Execution Time (milliseconds)", fontsize=11, fontweight="bold")
    plt.legend(frameon=True, facecolor="white", edgecolor="#cbd5e1", fontsize=10)
    plt.tight_layout()

    out_path = os.path.join(RESULTS_DIR, "runtime_vs_text_length.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Plot saved to: {out_path}")

    return {
        "text_lengths": text_lengths,
        "bm_times": bm_times,
        "kmp_times": kmp_times,
        "naive_times": naive_times,
    }


# =====================================================================
# Experiment 3: Impact of Alphabet Size (|Sigma|)
# =====================================================================
def experiment_alphabet_size():
    print("\n--- Running Experiment 3: Impact of Alphabet Size ---")
    alphabets = [
        ("Binary (|Sigma|=2)", "01"),
        ("DNA (|Sigma|=4)", "ACGT"),
        ("Decimal (|Sigma|=10)", string.digits),
        ("English (|Sigma|=26)", string.ascii_lowercase),
        ("ASCII Alphanum (|Sigma|=62)", string.ascii_letters + string.digits),
    ]

    text_len = 5000
    pattern_len = 10
    num_trials = 10

    labels = []
    bm_comps = []
    kmp_comps = []
    naive_comps = []

    for name, alpha in alphabets:
        bm_trials, kmp_trials, naive_trials = [], [], []
        for _ in range(num_trials):
            text = generate_random_string(text_len, alpha)
            start_pos = random.randint(0, text_len - pattern_len)
            pattern = text[start_pos : start_pos + pattern_len]

            bm = BoyerMoore(pattern)
            _, bc, _ = bm.search(text)
            _, nc, _ = naive_string_match(text, pattern)
            _, kc, _ = kmp_string_match(text, pattern)

            bm_trials.append(bc)
            naive_trials.append(nc)
            kmp_trials.append(kc)

        labels.append(name)
        bm_comps.append(np.mean(bm_trials))
        kmp_comps.append(np.mean(kmp_trials))
        naive_comps.append(np.mean(naive_trials))

        print(f"Alphabet: {name:<22} | BM: {bm_comps[-1]:6.1f} | KMP: {kmp_comps[-1]:6.1f} | Naive: {naive_comps[-1]:6.1f}")

    # Grouped bar chart
    x = np.arange(len(labels))
    width = 0.25

    plt.figure(figsize=(10, 5.5), dpi=300)
    plt.bar(x - width, bm_comps, width, label="Boyer-Moore", color="#1d4ed8")
    plt.bar(x, kmp_comps, width, label="Knuth-Morris-Pratt", color="#16a34a")
    plt.bar(x + width, naive_comps, width, label="Naive Brute-Force", color="#dc2626")

    plt.title("Impact of Alphabet Size (|$\\Sigma$|) on Total Character Comparisons\n(n = 5,000, m = 10, Averaged across 10 trials)", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Alphabet Type & Size", fontsize=11, fontweight="bold")
    plt.ylabel("Total Character Comparisons", fontsize=11, fontweight="bold")
    plt.xticks(x, labels, fontsize=9.5)
    plt.legend(frameon=True, facecolor="white", edgecolor="#cbd5e1", fontsize=10)
    plt.tight_layout()

    out_path = os.path.join(RESULTS_DIR, "alphabet_size_impact.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Plot saved to: {out_path}")

    return {
        "labels": labels,
        "bm_comps": bm_comps,
        "kmp_comps": kmp_comps,
        "naive_comps": naive_comps,
    }


# =====================================================================
# Experiment 4: Best-Case, Average-Case, and Worst-Case Analysis
# =====================================================================
def experiment_case_analysis():
    print("\n--- Running Experiment 4: Best-Case vs Worst-Case vs Average ---")
    n = 2000
    m = 10

    # 1. Best Case: Characters in pattern never appear in text -> BM makes n/m comparisons
    text_best = "A" * n
    patt_best = "B" * m

    # 2. Average Case: Random English alphabet
    text_avg = generate_random_string(n, string.ascii_lowercase)
    patt_avg = generate_random_string(m, string.ascii_lowercase)

    # 3. Worst Case: All characters identical except first or last
    text_worst = "A" * n
    patt_worst = "A" * (m - 1) + "B"

    cases = [
        ("Best Case (Disjoint Alphabet)", text_best, patt_best),
        ("Average Case (Random English)", text_avg, patt_avg),
        ("Worst Case (Repetitive Strings)", text_worst, patt_worst),
    ]

    results = []
    for case_name, t, p in cases:
        bm = BoyerMoore(p)
        _, bm_c, _ = bm.search(t)
        _, naive_c, _ = naive_string_match(t, p)
        _, kmp_c, _ = kmp_string_match(t, p)

        results.append({
            "case": case_name,
            "bm_comps": bm_c,
            "kmp_comps": kmp_c,
            "naive_comps": naive_c,
            "bm_ratio": bm_c / n,
        })
        print(f"Case: {case_name:<30} | BM: {bm_c:5d} ({bm_c/n:.2f}n) | KMP: {kmp_c:5d} | Naive: {naive_c:5d}")

    # Plotting summary
    labels = [r["case"].split(" (")[0] for r in results]
    x = np.arange(len(labels))
    width = 0.25

    plt.figure(figsize=(9, 5.5), dpi=300)
    plt.bar(x - width, [r["bm_comps"] for r in results], width, label="Boyer-Moore", color="#1d4ed8")
    plt.bar(x, [r["kmp_comps"] for r in results], width, label="Knuth-Morris-Pratt", color="#16a34a")
    plt.bar(x + width, [r["naive_comps"] for r in results], width, label="Naive Brute-Force", color="#dc2626")

    plt.title("Comparison Count across Best, Average, and Worst Cases\n(Fixed Text Length n = 2,000, Pattern Length m = 10)", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Algorithmic Complexity Scenario", fontsize=11, fontweight="bold")
    plt.ylabel("Total Character Comparisons (Log Scale)", fontsize=11, fontweight="bold")
    plt.yscale("log")
    plt.xticks(x, labels, fontsize=10, fontweight="bold")
    plt.legend(frameon=True, facecolor="white", edgecolor="#cbd5e1", fontsize=10)
    plt.tight_layout()

    out_path = os.path.join(RESULTS_DIR, "efficiency_summary.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Plot saved to: {out_path}")

    return results


# =====================================================================
# Main Benchmark Runner and CSV Exporter
# =====================================================================
def main():
    print("=" * 80)
    print("STARTING COMPREHENSIVE BENCHMARK EVALUATION FOR BOYER-MOORE ALGORITHM")
    print("=" * 80)

    res1 = experiment_pattern_length()
    res2 = experiment_text_length()
    res3 = experiment_alphabet_size()
    res4 = experiment_case_analysis()

    # Save summary CSV
    csv_path = os.path.join(RESULTS_DIR, "benchmark_summary.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Experiment", "Variable", "Boyer-Moore", "KMP", "Naive"])

        # Exp 1 rows
        for m, b, k, n in zip(res1["pattern_lengths"], res1["bm"], res1["kmp"], res1["naive"]):
            writer.writerow(["Pattern_Length_Comparisons", f"m={m}", f"{b:.2f}", f"{k:.2f}", f"{n:.2f}"])

        # Exp 2 rows
        for l, b, k, n in zip(res2["text_lengths"], res2["bm_times"], res2["kmp_times"], res2["naive_times"]):
            writer.writerow(["Runtime_ms", f"n={l}", f"{b:.4f}", f"{k:.4f}", f"{n:.4f}"])

        # Exp 3 rows
        for lbl, b, k, n in zip(res3["labels"], res3["bm_comps"], res3["kmp_comps"], res3["naive_comps"]):
            writer.writerow(["Alphabet_Size_Comparisons", lbl, f"{b:.2f}", f"{k:.2f}", f"{n:.2f}"])

        # Exp 4 rows
        for item in res4:
            writer.writerow(["Scenario_Comparisons", item["case"], item["bm_comps"], item["kmp_comps"], item["naive_comps"]])

    print(f"\nBenchmark results successfully compiled to: {csv_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
