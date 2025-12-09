import unittest
import time
from typing import AbstractSet

from src.grammar import Grammar
from src.utils import GrammarFormat


class TestFollow(unittest.TestCase):
    def _check_follow(
        self,
        grammar: Grammar,
        symbol: str,
        follow_set: AbstractSet[str],
    ) -> None:
        with self.subTest(string=f"Follow({symbol}), expected {follow_set}"):
            computed_follow = grammar.compute_follow(symbol)
            self.assertEqual(computed_follow, follow_set)

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
        self._check_follow(grammar, "E", {'$', ')'})
        self._check_follow(grammar, "T", {'$', ')', '+'})
        self._check_follow(grammar, "X", {'$', ')'})
        self._check_follow(grammar, "Y", {'$', ')', '+'})

        def test_simple_nullable(self) -> None:
            """
            Gramática:
                S -> A B
                A -> a
                A ->
                B -> b

            FOLLOW(S) = {$}
            FOLLOW(A) = {b}
            FOLLOW(B) = {$}
            """
        grammar_str = """
        S -> AB
        A -> a
        A ->
        B -> b
        """
        grammar = GrammarFormat.read(grammar_str)

        self._check_follow(grammar, "S", {'$'})
        self._check_follow(grammar, "A", {'b'})
        self._check_follow(grammar, "B", {'$'})

    def test_chain_nullable_middle(self) -> None:
        """
        Gramática:
            S -> A B C
            A -> a
            A ->
            B -> b
            B ->
            C -> c

        FOLLOW(S) = {$}
        FOLLOW(A) = {b, c}
        FOLLOW(B) = {c}
        FOLLOW(C) = {$}
        """
        grammar_str = """
        S -> ABC
        A -> a
        A ->
        B -> b
        B ->
        C -> c
        """
        grammar = GrammarFormat.read(grammar_str)

        self._check_follow(grammar, "S", {'$'})
        self._check_follow(grammar, "A", {'b', 'c'})
        self._check_follow(grammar, "B", {'c'})
        self._check_follow(grammar, "C", {'$'})

    def test_simple_recursion(self) -> None:
        """
        Gramática:
            S -> aS
            S -> bA
            A -> cA
            A -> d

        FOLLOW(S) = {$}
        FOLLOW(A) = {$}
        """
        grammar_str = """
        S -> aS
        S -> bA
        A -> cA
        A -> d
        """
        grammar = GrammarFormat.read(grammar_str)

        self._check_follow(grammar, "S", {'$'})
        self._check_follow(grammar, "A", {'$'})

    def test_follow_invalid_symbol_raises(self) -> None:
        """compute_follow debe lanzar ValueError si el símbolo no es no terminal."""
        grammar_str = """
        S -> AB
        A -> a
        B -> b
        """
        grammar = GrammarFormat.read(grammar_str)

        with self.assertRaises(ValueError):
            grammar.compute_follow("a")   # 'a' es terminal, no no terminal
    
    """def test_follow_performance(self):
        """"""
        Test artificial para comprobar que compute_follow realmente
        ejecuta trabajo y medir un tiempo visible.
        No forma parte de la corrección oficial.
        """"""

        grammar_str = """"""
        E -> TX
        X -> +E
        X ->
        T -> iY
        T -> (E)
        Y -> *T
        Y ->
        """"""

        grammar = GrammarFormat.read(grammar_str)

        N = 100000

        start = time.perf_counter()
        for _ in range(N):
            grammar.compute_follow("E")
        end = time.perf_counter()

        total = end - start
        avg = total / N

        print("\n--- Performance Test ---")
        print(f"Total time for {N} executions: {total:.6f} s")
        print(f"Average per call: {avg:.10f} s")

        self.assertEqual(grammar.compute_follow("E"), {'$', ')'})"""


if __name__ == '__main__':
    unittest.main()
