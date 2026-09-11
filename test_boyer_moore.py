"""
Unit Tests for Boyer-Moore Algorithm Implementation
Tests correctness against Naive String Matching and Python's native substring search.
"""

import unittest
from boyer_moore import BoyerMoore, naive_string_match, kmp_string_match


class TestBoyerMoore(unittest.TestCase):
    def check_all_matchers(self, text: str, pattern: str):
        bm = BoyerMoore(pattern)
        bm_matches, bm_comps, bm_shifts = bm.search(text)
        naive_matches, naive_comps, naive_shifts = naive_string_match(text, pattern)
        kmp_matches, kmp_comps, kmp_shifts = kmp_string_match(text, pattern)

        # Python native find for reference
        expected_matches = []
        if pattern:
            start = 0
            while True:
                idx = text.find(pattern, start)
                if idx == -1:
                    break
                expected_matches.append(idx)
                start = idx + 1

        self.assertEqual(bm_matches, expected_matches, f"BM mismatch for T='{text}', P='{pattern}'")
        self.assertEqual(naive_matches, expected_matches, f"Naive mismatch for T='{text}', P='{pattern}'")
        self.assertEqual(kmp_matches, expected_matches, f"KMP mismatch for T='{text}', P='{pattern}'")

    def test_standard_textbooks_examples(self):
        # Classic textbook example
        self.check_all_matchers("GCAATGCAGAGAG", "GCAGAGAG")
        self.check_all_matchers("HERE IS A SIMPLE EXAMPLE", "EXAMPLE")
        self.check_all_matchers("FINDINAHAYSTACKNEEDLEINA", "NEEDLE")

    def test_beginning_and_end(self):
        self.check_all_matchers("PATTERN at the start", "PATTERN")
        self.check_all_matchers("at the end of text PATTERN", "PATTERN")
        self.check_all_matchers("PATTERN", "PATTERN")

    def test_multiple_occurrences(self):
        self.check_all_matchers("ABRACADABRA", "ABRA")
        self.check_all_matchers("BANANA", "ANA")
        self.check_all_matchers("AAAAAA", "AA")

    def test_not_found(self):
        self.check_all_matchers("THE QUICK BROWN FOX JUMPS", "CAT")
        self.check_all_matchers("ABCDEFGH", "XYZ")

    def test_edge_cases(self):
        # Single char
        self.check_all_matchers("ABCDEFG", "D")
        self.check_all_matchers("DDDDDDD", "D")
        # Pattern longer than text
        self.check_all_matchers("SHORT", "LONGER_PATTERN")
        # Empty text
        self.check_all_matchers("", "PATTERN")
        # Repeating patterns
        self.check_all_matchers("A" * 100, "AAA")
        self.check_all_matchers("AB" * 50, "ABAB")

    def test_trace_steps(self):
        bm = BoyerMoore("GCAGAGAG")
        trace = bm.search_with_trace("GCAATGCAGAGAG")
        self.assertIn("steps", trace)
        self.assertTrue(len(trace["steps"]) > 0)
        self.assertEqual(trace["matches"], [5])


if __name__ == "__main__":
    unittest.main()
