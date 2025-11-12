"""Test evaluation of automatas."""
import unittest
from abc import ABC, abstractmethod
from typing import Optional, Type

from automaton import FiniteAutomaton
from utils import AutomataFormat


class TestEvaluatorBase(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    @abstractmethod
    def _create_automata(self):
        pass

    def setUp(self):
        """Set up the tests."""
        self.automaton = self._create_automata()

    def _check_accept_body(self, string, should_accept = True):
        accepted = self.automaton.accepts(string)
        if accepted != should_accept:
            #print(string, "should be", should_accept, "but is", accepted)
            pass
        self.assertEqual(accepted, should_accept)

    def _check_accept(self, string, should_accept = True, exception = None):

        with self.subTest(string=string):
            if exception is None:
                self._check_accept_body(string, should_accept)
            else:
                with self.assertRaises(exception):
                    self._check_accept_body(string, should_accept)


class TestEvaluatorFixed(TestEvaluatorBase):
    """Test for a fixed string."""

    def _create_automata(self):

        print("\n\nCreating automaton...\n\n")

        description = """
        Automaton:
            Symbols: Helo

            Empty
            H
            He
            Hel
            Hell
            Hello final

            ini Empty -H-> H
            H -e-> He
            He -l-> Hel
            Hel -l-> Hell
            Hell -o-> Hello
        """

        return AutomataFormat.read(description)

    def test_fixed(self):
        """Test for a fixed string."""
        self._check_accept("Hello", should_accept=True)
        self._check_accept("Helloo", should_accept=False)
        self._check_accept("Hell", should_accept=False)
        self._check_accept("llH", should_accept=False)
        self._check_accept("", should_accept=False)
        self._check_accept("Hella", should_accept=False)
        self._check_accept("aHello", should_accept=False)
        self._check_accept("Helloa", should_accept=False)


class TestEvaluatorLambdas(TestEvaluatorBase):
    """Test for a fixed string."""

    def _create_automata(self):

        description = """
        Automaton:
            Symbols: 

            1
            2
            3
            4 final

            ini 1 --> 2
            2 --> 3
            3 --> 4
        """

        return AutomataFormat.read(description)

    def test_lambda(self):
        """Test for a fixed string."""
        self._check_accept("", should_accept=True)
        self._check_accept("a", should_accept=False)


class TestEvaluatorNumber(TestEvaluatorBase):
    """Test for a fixed string."""

    def _create_automata(self):

        description = """
        Automaton:
            Symbols: 01.-

            initial
            sign
            int final
            dot
            decimal final

            ini initial ---> sign
            initial --> sign
            sign -0-> int
            sign -1-> int
            int -0-> int
            int -1-> int
            int -.-> dot
            dot -0-> decimal
            dot -1-> decimal
            decimal -0-> decimal
            decimal -1-> decimal
        """

        return AutomataFormat.read(description)

    def test_number(self) -> None:
        """Test for a fixed string."""
        self._check_accept("0", should_accept=True)
        self._check_accept("0.0", should_accept=True)
        self._check_accept("0.1", should_accept=True)
        self._check_accept("1.0", should_accept=True)
        self._check_accept("-0", should_accept=True)
        self._check_accept("-0.0", should_accept=True)
        self._check_accept("-0.1", should_accept=True)
        self._check_accept("-1.0", should_accept=True)
        self._check_accept("-101.010", should_accept=True)
        self._check_accept("0.", should_accept=False)
        self._check_accept(".0", should_accept=False)
        self._check_accept("0.0.0", should_accept=False)
        self._check_accept("0-0.0", should_accept=False)


class TestEvaluatorMultiplePaths(TestEvaluatorBase):
    """Test para un autómata complejo con múltiples caminos (no determinista)."""

    def _create_automata(self):

        description = """
        Automaton:
            Symbols: abc

            start
            state_a
            state_b
            state_c
            loop_a
            loop_b
            loop_c
            final_1 final
            final_2 final
            final_3 final
            final_4 final

            ini start --> final_4
            ini start -a-> state_a
            ini start -b-> state_b
            ini start -c-> state_c
            state_a -a-> loop_a
            state_a -a-> final_1
            state_a -b-> loop_b
            state_a -c-> loop_c
            state_b -a-> loop_a
            state_b -b-> loop_b
            state_b -b-> final_2
            state_b -c-> loop_c
            state_c -a-> loop_a
            state_c -b-> loop_b
            state_c -c-> loop_c
            state_c -c-> final_3
            loop_a -a-> loop_a
            loop_a -a-> final_1
            loop_a -b-> loop_b
            loop_a -c-> loop_c
            loop_b -a-> loop_a
            loop_b -b-> loop_b
            loop_b -b-> final_2
            loop_b -c-> loop_c
            loop_c -a-> loop_a
            loop_c -b-> loop_b
            loop_c -c-> loop_c
            loop_c -c-> final_3
            loop_a -b-> final_4
            loop_b -c-> final_4
            loop_c -a-> final_4
        """

        return AutomataFormat.read(description)

    def test_multiple_paths(self):
        """Test para strings complejos con múltiples caminos de aceptación."""
        # Casos inválidos - strings de 1 carácter (no llegan a estados finales)
        self._check_accept("a", should_accept=False)  # start -> state_a (no final)
        self._check_accept("b", should_accept=False)  # start -> state_b (no final)
        self._check_accept("c", should_accept=False)  # start -> state_c (no final)
        
        # Casos válidos - strings de 2 caracteres que llegan a finales
        self._check_accept("aa", should_accept=True)  # start -> state_a -> final_1
        self._check_accept("bb", should_accept=True)  # start -> state_b -> final_2
        self._check_accept("cc", should_accept=True)  # start -> state_c -> final_3
        
        # Casos inválidos - strings de 2 caracteres que no llegan a finales
        self._check_accept("ab", should_accept=False)  # start -> state_a -> loop_b (no final)
        self._check_accept("ac", should_accept=False)  # start -> state_a -> loop_c (no final)
        self._check_accept("ba", should_accept=False)  # start -> state_b -> loop_a (no final)
        self._check_accept("bc", should_accept=False)  # start -> state_b -> loop_c (no final)
        self._check_accept("ca", should_accept=False)  # start -> state_c -> loop_a (no final)
        self._check_accept("cb", should_accept=False)  # start -> state_c -> loop_b (no final)
        
        # Casos válidos - strings de 3 caracteres
        self._check_accept("aaa", should_accept=True)  # Puede llegar a final_1
        self._check_accept("aab", should_accept=True)  # state_a -> loop_a -> final_4
        self._check_accept("abb", should_accept=True)   # state_a -> loop_b -> loop_b -> final_4
        self._check_accept("abc", should_accept=True)  # state_a -> loop_b -> loop_c -> final_4
        self._check_accept("aca", should_accept=True)   # state_a -> loop_a -> loop_c -> final_4
        self._check_accept("acc", should_accept=True)   # state_a -> loop_a -> loop_c -> final_4
        self._check_accept("baa", should_accept=True)   # state_b -> loop_a -> loop_a -> final_4
        self._check_accept("bab", should_accept=True)   # state_b -> loop_b -> loop_b -> final_4
        self._check_accept("bbb", should_accept=True)   # state_b -> loop_b -> loop_b -> final_4
        self._check_accept("bbc", should_accept=True)  # state_b -> loop_b -> final_4
        self._check_accept("bca", should_accept=True)  # state_b -> loop_c -> final_4
        self._check_accept("bcc", should_accept=True)   # state_b -> loop_c -> final_4
        self._check_accept("caa", should_accept=True)   # state_c -> loop_a -> loop_a -> final_4
        self._check_accept("cab", should_accept=True)  # state_c -> loop_a -> final_4
        self._check_accept("cbb", should_accept=True)   # state_c -> loop_b -> loop_b -> final_4
        self._check_accept("cbc", should_accept=True)   # state_c -> loop_c -> loop_c -> final_4
        self._check_accept("cca", should_accept=True)  # state_c -> loop_c -> final_4
        self._check_accept("ccc", should_accept=True)   # state_c -> loop_c -> loop_c -> final_4
        
        # Casos inválidos - strings de 3 caracteres que no llegan a finales
        self._check_accept("aba", should_accept=False)  # state_a -> loop_b -> loop_a (no final)
        self._check_accept("aac", should_accept=False)  # state_a -> loop_a -> loop_c (no final)
        self._check_accept("acb", should_accept=False)  # state_a -> loop_a -> loop_b (no final)
        self._check_accept("bac", should_accept=False)  # state_b -> loop_c -> loop_a (no final)
        self._check_accept("bba", should_accept=False)  # state_b -> loop_a -> loop_b (no final)
        self._check_accept("bcb", should_accept=False)  # state_b -> loop_b -> loop_c (no final)
        self._check_accept("cac", should_accept=False)  # state_c -> loop_a -> loop_c (no final)
        self._check_accept("cba", should_accept=False)  # state_c -> loop_a -> loop_b (no final)
        self._check_accept("ccb", should_accept=False)  # state_c -> loop_c -> loop_b (no final)
        
        # Casos válidos - strings de 4 caracteres
        self._check_accept("aaaa", should_accept=True)  # Puede llegar a final_1
        self._check_accept("abab", should_accept=True)  # state_a -> loop_b -> loop_a -> final_4
        self._check_accept("bcab", should_accept=True)  # state_b -> loop_c -> loop_a -> final_4
        self._check_accept("cabc", should_accept=True)  # state_c -> loop_a -> loop_b -> final_4
        
        # Casos inválidos - strings de 4 caracteres que no llegan a finales
        self._check_accept("abcb", should_accept=False)  # state_a -> loop_b -> loop_c -> loop_b (no final)
        
        # Casos válidos - strings más largos
        self._check_accept("abcabc", should_accept=True)  # state_a -> loop_b -> loop_c -> loop_a -> loop_b -> final_4
        self._check_accept("ababab", should_accept=True)  # state_a -> loop_b -> loop_a -> loop_b -> loop_a -> final_4
        
        # Casos inválidos - strings vacíos o con símbolos no válidos
        self._check_accept("", should_accept=True)  # Cadena vacía
        self._check_accept("x", should_accept=False)  # Símbolo no válido
        self._check_accept("ax", should_accept=False)  # Símbolo no válido
        self._check_accept("d", should_accept=False)  # Símbolo no válido

if __name__ == '__main__':
    unittest.main()
