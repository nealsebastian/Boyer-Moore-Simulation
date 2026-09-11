# Boyer–Moore String Matching Algorithm
### Design and Analysis of Algorithms (DAA) — CIA 3 Component 1 (Unit 4: String Matching)

This repository contains a complete, rigorous implementation of the **Boyer–Moore String Matching Algorithm**, including:
- **Dual Heuristic Implementation**: Bad Character Heuristic and Good Suffix Heuristic (Strong Good Suffix Rule + Prefix Border Matching).
- **Interactive Step-by-Step Terminal Simulation**: Visual ASCII alignment and right-to-left scan tracking.
- **Interactive Web Visualizer (`interactive_visualizer.html`)**: Rich standalone browser application featuring animations, play/pause controls, step history, and live heuristic calculations.
- **Empirical Benchmarking & Complexity Analysis (`benchmark_analysis.py`)**: Comparative evaluation against **Knuth-Morris-Pratt (KMP)** and **Naive Brute-Force**, evaluating pattern lengths, text scalability, alphabet sizes, and complexity cases.
- **Comprehensive Academic Report (`CIA3_Report_Boyer_Moore.md`)**: Full report covering theoretical foundations, mathematical derivations, complexities, simulation traces, and experimental graphs.

---

## Project Directory Structure

```
DAA CIA 3/
├── index.html                  # All-in-One Web Application Portal (Visualizer, Empirical Results, Live Lab, Theory, Report)
├── boyer_moore.py              # Core Boyer-Moore algorithm, tracer & baseline matchers (KMP, Naive)
├── simulation.py               # Interactive terminal step-by-step simulator
├── interactive_visualizer.html # Standalone interactive browser visualizer
├── benchmark_analysis.py       # Empirical benchmarking suite (generates plots & CSV)
├── test_boyer_moore.py         # Unit tests covering standard and edge cases
├── CIA3_Report_Boyer_Moore.md  # Comprehensive academic project report
├── README.md                   # Project documentation and execution instructions
└── results/                    # Generated empirical analysis plots and CSV
    ├── comparisons_vs_pattern_length.png
    ├── runtime_vs_text_length.png
    ├── alphabet_size_impact.png
    ├── efficiency_summary.png
    └── benchmark_summary.csv
```

---

## Quick Start & Execution Guide

### 1. Launch the All-in-One Website Portal (Recommended)
Double-click **`index.html`** or run:
```powershell
start index.html
```
*(Or host locally with `py -m http.server 8000` and open `http://localhost:8000`).*

It includes:
- 🎮 **Interactive Visualizer Tab**: Right-to-left character scanning animation, step-by-step navigation, Bad Character & Good Suffix live breakdown.
- 📊 **Empirical Results Tab**: Pre-rendered scientific comparison plots with analysis data tables.
- 🧪 **Live Lab Tab**: Benchmark Boyer-Moore vs KMP vs Naive on dynamically generated random strings directly in browser.
- 📖 **Theory Tab**: Formal derivations of Bad Character, Strong Good Suffix, and complexity tables.
- 📄 **Report Tab**: Full academic report with 1-click Print/PDF export.

### 2. Run Unit Tests
Verifies algorithmic correctness against Naive matching and Python native substring search across standard examples and edge cases:
```powershell
py -m unittest test_boyer_moore.py
```

### 3. Run Step-by-Step Terminal Simulation
Launches the console simulator with preset educational examples or custom text/pattern inputs:
```powershell
py simulation.py
```

### 3. Open the Interactive Web Visualizer
Double-click `interactive_visualizer.html` or open it in any modern web browser (Edge, Chrome, Firefox).
- **Features**:
  - Live right-to-left scanning animation.
  - Step-by-step navigation (First, Prev, Next, Last, Auto-play).
  - Green/Red tiles for character matches and mismatches.
  - Real-time display of Bad Character and Good Suffix calculations.
  - Live comparison counter comparing Boyer-Moore vs Naive vs KMP.

### 4. Run the Empirical Benchmark Suite
Re-runs the multi-variable benchmark suite and regenerates high-resolution publication plots:
```powershell
py benchmark_analysis.py
```
Outputs generated in `results/`:
- `comparisons_vs_pattern_length.png`: Demonstrates sublinear $O(n/m)$ comparison reduction as pattern length increases.
- `runtime_vs_text_length.png`: Shows wall-clock scaling from 2,000 to 80,000 characters.
- `alphabet_size_impact.png`: Demonstrates efficiency boost on larger alphabets (DNA vs English vs ASCII).
- `efficiency_summary.png`: Compares Best-Case, Average-Case, and Worst-Case scenarios.
- `benchmark_summary.csv`: Tabular raw data.

---

## Algorithm Summary

| Algorithm | Preprocessing Time | Matching Time (Best) | Matching Time (Average) | Matching Time (Worst) | Space Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Naive Brute-Force** | None ($O(1)$) | $\Omega(n)$ | $\Theta(n)$ | $O((n - m + 1) \cdot m)$ | $O(1)$ |
| **Knuth-Morris-Pratt (KMP)** | $\Theta(m)$ | $\Omega(n)$ | $\Theta(n)$ | $O(n + m)$ | $\Theta(m)$ |
| **Boyer–Moore (BM)** | $\Theta(m + \|\Sigma\|)$ | **$\Omega(n/m)$** *(Sublinear)* | **$O(n/m)$ to $O(n)$** | $O(n \cdot m)$ or $O(n+m)^*$ | $\Theta(m + \|\Sigma\|)$ |

*\* With strong Good Suffix rule, worst-case comparisons can be bounded to $O(n)$ on non-periodic patterns.*

---

## Submission Details
- **Student Name**: [Your Name]
- **Roll Number / Reg No**: [Your Roll No]
- **Course**: Design and Analysis of Algorithms (DAA)
- **Assignment**: CIA–3 Component–1 (Unit–4: String Matching)
- **Topic**: Boyer–Moore Algorithm for String Matching
