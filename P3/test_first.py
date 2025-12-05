from math import prod
import unittest
from typing import AbstractSet

from src.grammar import Grammar
from src.utils import GrammarFormat


class TestFirst(unittest.TestCase):
    def _check_first(
        self,
        grammar: Grammar,
        input_string: str,
        first_set: AbstractSet[str],
    ) -> None:
        with self.subTest(
            string=f"First({input_string}), expected {first_set}",
        ):
            computed_first = grammar.compute_first(input_string)
            print(f"     => First({input_string}) = {computed_first} - Expected {first_set}")
            self.assertEqual(computed_first, first_set)

    def test_case1(self) -> None:
        """Test Case 1."""
        grammar_str = """
        E -> TX
        X -> +E
        X ->
        T -> iY
        T -> (E)
        Y -> *T
        Y ->
        """
        
        grammar = GrammarFormat.read(grammar_str)

        self._check_first(grammar, "E", {'(', 'i'})
        self._check_first(grammar, "T", {'(', 'i'})
        self._check_first(grammar, "X", {'', '+'})
        self._check_first(grammar, "Y", {'', '*'})
        self._check_first(grammar, "", {''})
        self._check_first(grammar, "Y+i", {'+', '*'})
        self._check_first(grammar, "YX", {'+', '*', ''})
        self._check_first(grammar, "YXT", {'+', '*', 'i', '('})

        # 10 extra/edge/strange cases
        self._check_first(grammar, "TX", {'(', 'i'})
        self._check_first(grammar, "XTX", {'+', '', '(', 'i'})
        self._check_first(grammar, "()", {'('})  # only terminals
        self._check_first(grammar, "++", {'+'})  # repeated terminal
        self._check_first(grammar, "TTT", {'(', 'i'})
        with self.assertRaises(ValueError): self._check_first(grammar, "XYZ", {'', '+', '*'})  # Z no está en la gramática, debe dar error
        self._check_first(grammar, "YXTX", {'+', '*', '', '(', 'i'})
        self._check_first(grammar, "YX()", {'+', '*', '('})
        self._check_first(grammar, "T", {'(', 'i'})
        self._check_first(grammar, "X", {'', '+'})
        self._check_first(grammar, "YY", {'', '*'})
        self._check_first(grammar, "XT", {'+', '(', 'i'})


if __name__ == '__main__':
    unittest.main()
