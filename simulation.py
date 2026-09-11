"""
Boyer-Moore String Matching: Step-by-Step Interactive Simulation
Course: Design and Analysis of Algorithms (DAA) - CIA 3 Component 1
Topic: Unit-4 String Matching

Demonstrates the inner mechanics of the Boyer-Moore algorithm:
- Bad Character Heuristic calculation
- Good Suffix Heuristic calculation
- Alignment shifting with right-to-left character scanning
- Comparative efficiency metrics vs. Naive and KMP
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
from boyer_moore import BoyerMoore, naive_string_match, kmp_string_match


def print_banner():
    banner = """
================================================================================
          BOYER-MOORE STRING MATCHING ALGORITHM - STEP-BY-STEP SIMULATION
                       DAA CIA-3 COMPONENT-1 (UNIT-4)
================================================================================
"""
    print(banner)


def render_step(step: dict, text: str, pattern: str, m: int, n: int):
    step_num = step["step_number"]
    s = step["alignment_index"]
    mismatch = step["mismatch"]
    matched = step["matched_positions"]
    is_match = step["is_match"]

    print(f"\n--- STEP {step_num} (Alignment shift s = {s}) ---")

    # Display Text with index ruler
    # Ruler line
    ruler = "".join(f"{i % 10}" for i in range(n))
    print(f"Index: {ruler}")
    print(f"Text:  {text}")

    # Display Pattern aligned at s
    pattern_line = [" "] * n
    for idx, ch in enumerate(pattern):
        pattern_line[s + idx] = ch
    print(f"Patt:  {''.join(pattern_line)}")

    # Comparison visualization line
    status_line = [" "] * n
    for m_pos in matched:
        status_line[m_pos["t_idx"]] = "M"  # Matched
    if mismatch:
        status_line[mismatch["t_idx"]] = "X"  # Mismatched

    print(f"Scan:  {''.join(status_line)}   (M = Match, X = Mismatch)")

    # Detailed Scan Information
    print("\n[Right-to-Left Comparison Details]")
    if matched:
        matched_str = ", ".join([f"P[{p['p_idx']}]=='{p['char']}' == T[{p['t_idx']}]" for p in matched])
        print(f"  Matches:   {matched_str}")

    if is_match:
        print(f"  Result:    FULL PATTERN MATCH FOUND at index {s}!")
        print(f"  Heuristic: Good Suffix Rule dictates shift of {step['chosen_shift']}.")
    else:
        p_idx = mismatch["p_idx"]
        t_idx = mismatch["t_idx"]
        p_char = mismatch["p_char"]
        t_char = mismatch["t_char"]
        print(f"  Mismatch:  P[{p_idx}]='{p_char}' != T[{t_idx}]='{t_char}'")

        # Heuristic calculations
        bc_shift = step["bc_shift"]
        gs_shift = step["gs_shift"]
        chosen = step["chosen_shift"]
        rule = step["rule_used"]

        print(f"  Bad Character Rule:  shift = max(1, {p_idx} - L('{t_char}')) = {bc_shift}")
        print(f"  Good Suffix Rule:    shift = {gs_shift}")
        print(f"  Decision:            max({bc_shift}, {gs_shift}) -> Shift by {chosen} [{rule}]")

    print(f"  Comparisons so far: {step['total_comparisons_so_far']}")


def run_simulation(text: str, pattern: str, interactive: bool = False):
    print("=" * 80)
    print(f"TARGET TEXT:    \"{text}\" (Length: {len(text)})")
    print(f"SEARCH PATTERN: \"{pattern}\" (Length: {len(pattern)})")
    print("=" * 80)

    bm = BoyerMoore(pattern)

    print("\n[PREPROCESSING TABLES]")
    print(f"1. Bad Character Last Occurrence Table: {bm.bad_char_table}")
    print(f"2. Good Suffix Shift Table:             {bm.good_suffix_table}")

    trace = bm.search_with_trace(text)
    steps = trace["steps"]

    for step in steps:
        render_step(step, text, pattern, len(pattern), len(text))
        if interactive:
            input("\n[Press Enter to advance to next step...]")

    # Run baselines
    naive_matches, naive_comps, naive_shifts = naive_string_match(text, pattern)
    kmp_matches, kmp_comps, kmp_shifts = kmp_string_match(text, pattern)

    print("\n" + "=" * 80)
    print("FINAL SIMULATION SUMMARY & COMPARATIVE ANALYSIS")
    print("=" * 80)
    print(f"Occurrences found at indices: {trace['matches']}")
    print("-" * 80)
    print(f"{'Algorithm':<25} | {'Comparisons':<15} | {'Shifts/Steps':<15}")
    print("-" * 80)
    print(f"{'Boyer-Moore (BM)':<25} | {trace['total_comparisons']:<15} | {trace['total_shifts']:<15}")
    print(f"{'Knuth-Morris-Pratt (KMP)':<25} | {kmp_comps:<15} | {kmp_shifts:<15}")
    print(f"{'Naive (Brute Force)':<25} | {naive_comps:<15} | {naive_shifts:<15}")
    print("-" * 80)

    if naive_comps > 0:
        savings = ((naive_comps - trace["total_comparisons"]) / naive_comps) * 100
        print(f"Boyer-Moore comparison reduction vs. Naive: {savings:.2f}%")
    print("=" * 80 + "\n")


def main():
    print_banner()

    presets = [
        ("DNA Sequence Search (Classic Textbook)", "GCAATGCAGAGAG", "GCAGAGAG"),
        ("Natural English Search", "HERE IS A SIMPLE EXAMPLE", "EXAMPLE"),
        ("Sublinear Best Case (Character Not Present)", "ABCDEFGHIJKLMNO", "XYZW"),
        ("Overlapping Substring Search", "ABRACADABRA", "ABRA"),
    ]

    print("Choose an option to simulate:")
    for idx, (name, t, p) in enumerate(presets, 1):
        print(f"  {idx}. {name} (Text: '{t}', Pattern: '{p}')")
    print(f"  {len(presets) + 1}. Custom Text and Pattern Input")
    print(f"  {len(presets) + 2}. Run All Preset Simulations Automatically")

    choice = input(f"\nEnter choice (1-{len(presets) + 2}) [default: 1]: ").strip()
    if not choice:
        choice = "1"

    try:
        choice_idx = int(choice)
    except ValueError:
        choice_idx = 1

    if 1 <= choice_idx <= len(presets):
        name, t, p = presets[choice_idx - 1]
        run_simulation(t, p, interactive=False)
    elif choice_idx == len(presets) + 1:
        custom_text = input("Enter Text: ").strip()
        custom_patt = input("Enter Pattern: ").strip()
        if not custom_patt or not custom_text:
            print("Text or pattern cannot be empty. Running preset 1.")
            name, t, p = presets[0]
            run_simulation(t, p)
        else:
            run_simulation(custom_text, custom_patt)
    elif choice_idx == len(presets) + 2:
        for name, t, p in presets:
            run_simulation(t, p, interactive=False)
    else:
        print("Invalid choice. Running default preset.")
        name, t, p = presets[0]
        run_simulation(t, p)


if __name__ == "__main__":
    main()
