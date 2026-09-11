"""
Boyer-Moore String Matching Algorithm Implementation
Course: Design and Analysis of Algorithms (DAA) - CIA 3 Component 1
Topic: Unit-4 String Matching

This module implements:
1. Bad Character Heuristic (Boyer-Moore)
2. Good Suffix Heuristic (Strong Good Suffix Rule + Prefix Border Matching)
3. Full Boyer-Moore Algorithm (combining both heuristics)
4. Step-by-Step Tracer for Simulation & Visualization
5. Baseline Comparison Algorithms (Naive Brute-Force & Knuth-Morris-Pratt (KMP))
"""

from typing import List, Dict, Tuple, Any
import time


class BoyerMoore:
    def __init__(self, pattern: str):
        """
        Initializes the Boyer-Moore pattern matcher and precomputes
        both Bad Character and Good Suffix heuristic shift tables.
        """
        self.pattern = pattern
        self.m = len(pattern)
        if self.m > 0:
            self.bad_char_table = self.build_bad_char_table(pattern)
            self.good_suffix_table = self.build_good_suffix_table(pattern)
        else:
            self.bad_char_table = {}
            self.good_suffix_table = []

    @staticmethod
    def build_bad_char_table(pattern: str) -> Dict[str, int]:
        """
        Builds the Bad Character heuristic table (Last Occurrence Function).
        L(c) returns the rightmost index of character c in pattern (0 <= L(c) < m).
        For characters not present, lookup defaults to -1.
        """
        table = {}
        for idx, char in enumerate(pattern):
            table[char] = idx
        return table

    @staticmethod
    def build_good_suffix_table(pattern: str) -> List[int]:
        """
        Builds the Strong Good Suffix shift table using border-position preprocessing.
        Handles both:
          - Case 1: Matching suffix occurs elsewhere in the pattern preceded by a different character.
          - Case 2: A prefix of the pattern matches a suffix of the matched portion.
        Returns a list of size m + 1, where good_suffix_table[j + 1] gives the shift
        when mismatch occurs at index j (i.e. pattern[j+1 ... m-1] matched successfully).
        """
        m = len(pattern)
        shift = [0] * (m + 1)
        bpos = [0] * (m + 1)

        # Preprocessing Case 1 (Strong Good Suffix Rule)
        i = m
        j = m + 1
        bpos[i] = j

        while i > 0:
            while j <= m and pattern[i - 1] != pattern[j - 1]:
                if shift[j] == 0:
                    shift[j] = j - i
                j = bpos[j]
            i -= 1
            j -= 1
            bpos[i] = j

        # Preprocessing Case 2 (Prefix Border Rule for unmatched suffixes)
        j = bpos[0]
        for i in range(m + 1):
            if shift[i] == 0:
                shift[i] = j
            if i == j:
                j = bpos[j]

        return shift

    def search(self, text: str) -> Tuple[List[int], int, int]:
        """
        Standard Boyer-Moore search returning (matches, total_comparisons, total_shifts).
        Matches is a list of 0-based starting indices where pattern occurs in text.
        """
        n = len(text)
        m = self.m
        matches = []
        comparisons = 0
        shifts = 0

        if m == 0 or n < m:
            return matches, comparisons, shifts

        s = 0  # s is the shift of the pattern with respect to text
        while s <= n - m:
            j = m - 1

            # Right-to-left scan
            while j >= 0:
                comparisons += 1
                if self.pattern[j] == text[s + j]:
                    j -= 1
                else:
                    break

            if j < 0:
                # Pattern found at index s
                matches.append(s)
                # Shift pattern so the next occurrence can be found
                shift_amount = self.good_suffix_table[0] if self.good_suffix_table[0] > 0 else 1
                s += shift_amount
                shifts += 1
            else:
                mismatched_char = text[s + j]
                last_occurrence = self.bad_char_table.get(mismatched_char, -1)
                bc_shift = max(1, j - last_occurrence)
                gs_shift = self.good_suffix_table[j + 1]

                shift_amount = max(bc_shift, gs_shift)
                s += shift_amount
                shifts += 1

        return matches, comparisons, shifts

    def search_with_trace(self, text: str) -> Dict[str, Any]:
        """
        Executes Boyer-Moore search and records every comparison and shift
        for simulation and visualization purposes.
        """
        n = len(text)
        m = self.m
        matches = []
        comparisons = 0
        shifts = 0
        steps = []

        if m == 0 or n < m:
            return {
                "matches": matches,
                "total_comparisons": 0,
                "total_shifts": 0,
                "steps": steps,
                "bad_char_table": self.bad_char_table,
                "good_suffix_table": self.good_suffix_table,
            }

        s = 0
        step_number = 1

        while s <= n - m:
            j = m - 1
            matched_chars_in_alignment = []
            mismatch_info = None

            # Right-to-left scan
            while j >= 0:
                comparisons += 1
                t_idx = s + j
                t_char = text[t_idx]
                p_char = self.pattern[j]

                if p_char == t_char:
                    matched_chars_in_alignment.append({"p_idx": j, "t_idx": t_idx, "char": p_char})
                    j -= 1
                else:
                    mismatch_info = {
                        "p_idx": j,
                        "t_idx": t_idx,
                        "p_char": p_char,
                        "t_char": t_char,
                    }
                    break

            is_match = (j < 0)

            if is_match:
                matches.append(s)
                gs_shift = self.good_suffix_table[0] if self.good_suffix_table[0] > 0 else 1
                bc_shift = 1
                chosen_shift = gs_shift
                rule_used = "Good Suffix Rule (full match shift)"
            else:
                t_char = mismatch_info["t_char"]
                last_occ = self.bad_char_table.get(t_char, -1)
                bc_shift = max(1, j - last_occ)
                gs_shift = self.good_suffix_table[j + 1]

                if bc_shift >= gs_shift:
                    chosen_shift = bc_shift
                    rule_used = "Bad Character Heuristic"
                else:
                    chosen_shift = gs_shift
                    rule_used = "Good Suffix Heuristic"

            steps.append({
                "step_number": step_number,
                "alignment_index": s,
                "matched_positions": matched_chars_in_alignment,
                "mismatch": mismatch_info,
                "is_match": is_match,
                "bc_shift": bc_shift,
                "gs_shift": gs_shift,
                "chosen_shift": chosen_shift,
                "rule_used": rule_used,
                "total_comparisons_so_far": comparisons,
            })

            s += chosen_shift
            shifts += 1
            step_number += 1

        return {
            "text": text,
            "pattern": self.pattern,
            "matches": matches,
            "total_comparisons": comparisons,
            "total_shifts": shifts,
            "steps": steps,
            "bad_char_table": self.bad_char_table,
            "good_suffix_table": self.good_suffix_table,
        }


# =====================================================================
# Baseline Algorithms for Comparative Analysis
# =====================================================================

def naive_string_match(text: str, pattern: str) -> Tuple[List[int], int, int]:
    """
    Naive (Brute-Force) String Matching Algorithm.
    Returns (matches, total_comparisons, total_shifts).
    """
    n = len(text)
    m = len(pattern)
    matches = []
    comparisons = 0
    shifts = 0

    if m == 0 or n < m:
        return matches, comparisons, shifts

    for s in range(n - m + 1):
        shifts += 1
        match = True
        for j in range(m):
            comparisons += 1
            if pattern[j] != text[s + j]:
                match = False
                break
        if match:
            matches.append(s)

    return matches, comparisons, shifts


def compute_kmp_lps(pattern: str) -> List[int]:
    """
    Computes Longest Prefix Suffix (LPS) array for Knuth-Morris-Pratt (KMP).
    """
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_string_match(text: str, pattern: str) -> Tuple[List[int], int, int]:
    """
    Knuth-Morris-Pratt (KMP) String Matching Algorithm.
    Returns (matches, total_comparisons, total_shifts).
    """
    n = len(text)
    m = len(pattern)
    matches = []
    comparisons = 0
    shifts = 0

    if m == 0 or n < m:
        return matches, comparisons, shifts

    lps = compute_kmp_lps(pattern)
    i = 0  # index for text
    j = 0  # index for pattern

    while i < n:
        comparisons += 1
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
            shifts += 1
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
                shifts += 1
            else:
                i += 1
                shifts += 1

    return matches, comparisons, shifts
