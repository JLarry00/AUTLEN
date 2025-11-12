"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automaton import FiniteAutomaton
from utils import AutomataFormat, deterministic_automata_isomorphism


class TestMinimize(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_minimize(self, automaton, simplified, tag):
        """Test that the minimized automaton is the simplified one."""
        minimized = automaton.to_minimized()
        equiv_map = deterministic_automata_isomorphism(minimized, simplified)

        automaton.draw(filename=f"{tag}_orig",    view=False)
        minimized.draw(filename=f"{tag}_minimized",     view=False)
        simplified.draw(filename=f"{tag}_expected", view=False)

        self.assertTrue(equiv_map is not None)

    def test_empty_language(self):
        """Test an automaton for the empty language."""
        automaton_str = """
        Automaton:
            Symbols: a

            Initial
            NotReached1
            NotReached2
            Empty

            ini Initial -a-> Empty
            NotReached1 -a-> NotReached2
            NotReached2 -a-> Empty
            Empty -a-> Empty
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: a

            Initial

            ini Initial -a-> Initial
        """

        simplified = AutomataFormat.read(simplified_str)

        self._check_minimize(automaton, simplified, "empty_str_language")

    def test_empty_str_language(self):
        """Test an automaton for the empty language."""
        automaton_str = """
        Automaton:
            Symbols: a

            Initial final
            NotReached1
            NotReached2
            Empty

            ini Initial -a-> Empty
            NotReached1 -a-> NotReached2
            NotReached2 -a-> Empty
            Empty -a-> Empty
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: a

            Initial final
            Empty 

            ini Initial -a-> Empty
            Empty -a-> Empty
        """

        simplified = AutomataFormat.read(simplified_str)

        self._check_minimize(automaton, simplified, "empty_language")

    def test_redundant_states(self):
        """Test an automaton for the empty language."""
        automaton_str = """
        Automaton:
            Symbols: ab

            Initial
            B1 final
            B2 final
            Empty

            ini Initial -a-> B1
            Initial -b-> Empty
            B1 -a-> B1
            B1 -b-> B2
            B2 -a-> B1
            B2 -b-> B1
            Empty -a-> Empty
            Empty -b-> Empty
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: ab

            Initial
            B final
            Empty

            ini Initial -a-> B
            Initial -b-> Empty
            B -a-> B
            B -b-> B
            Empty -a-> Empty
            Empty -b-> Empty
        """

        simplified = AutomataFormat.read(simplified_str).to_deterministic()

        self._check_minimize(automaton, simplified, "redundant_states")
    


    def test_minimize(self):
        """Test an automaton for the empty language."""
        automaton_str = """
        Automaton:
            Symbols: ab

            Initial
            B1 final
            B2 final
            Empty

            ini Initial -a-> B1
            Initial -b-> Empty
            B1 -a-> B1
            B1 -b-> B2
            B2 -a-> B1
            B2 -b-> B1
            Empty -a-> Empty
            Empty -b-> Empty
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: ab

            Initial
            B final
            Empty

            ini Initial -a-> B
            Initial -b-> Empty
            B -a-> B
            B -b-> B
            Empty -a-> Empty
            Empty -b-> Empty
        """

        simplified = AutomataFormat.read(simplified_str).to_deterministic()

        self._check_minimize(automaton, simplified, "minimize")

    def test_minimize_2(self):
        """Test minimization of a cyclic automaton with 6 states."""
        automaton_str = """
        Automaton:
            Symbols: 01

            q0 final
            q1
            q2 final
            q3
            q4 final
            q5

            ini q0 -0-> q1
            q0 -1-> q1
            q1 -0-> q2
            q1 -1-> q2
            q2 -0-> q3
            q2 -1-> q3
            q3 -0-> q4
            q3 -1-> q4
            q4 -0-> q5
            q4 -1-> q5
            q5 -0-> q0
            q5 -1-> q0
        """

        automaton = AutomataFormat.read(automaton_str)

        simplified_str = """
        Automaton:
            Symbols: 01

            q0q2q4 final
            q1q3q5

            ini q0q2q4 -0-> q1q3q5
            q0q2q4 -1-> q1q3q5
            q1q3q5 -0-> q0q2q4
            q1q3q5 -1-> q0q2q4
        """

        simplified = AutomataFormat.read(simplified_str).to_deterministic()

        self._check_minimize(automaton, simplified, "minimize_2")


if __name__ == '__main__':
    unittest.main()
