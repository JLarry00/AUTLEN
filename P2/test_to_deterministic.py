"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automaton import FiniteAutomaton
from utils import AutomataFormat, deterministic_automata_isomorphism


class TestTransform(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_transform(self, automaton, expected):
        """Test that the transformed automaton is as the expected one."""

        automaton.draw(filename="automaton", view=False)

        transformed = automaton.to_deterministic()

        transformed.draw(filename="transformed", view=False)
        expected.draw(filename="expected", view=False)

        equiv_map = deterministic_automata_isomorphism(expected, transformed)

        self.assertTrue(equiv_map is not None)

    def test_case1(self):
        """Test Case 1."""
        automaton_str = """
        Automaton:
        Symbols: 01
        
        q0
        qf final
        
        ini q0 -0-> qf
        qf -1-> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: 01
        
        q0
        qf final
        empty
        
        ini q0 -0-> qf
        q0 -1-> empty
        qf -0-> empty
        qf -1-> qf
        empty -0-> empty
        empty -1-> empty
        
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case2(self):
        """Test Case 2 - Complex with non-deterministic transitions."""
        automaton_str = """
        Automaton:
        Symbols: 01
        
        q0
        q1
        q2 final
        
        ini q0 -0-> q1
        q0 -0-> q2
        q0 -1-> q1
        q1 -0-> q2
        q1 -1-> q1
        q2 -0-> q1
        q2 -1-> q2
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: 01
        
        q0
        q1 final
        q2
        q3 final
        
        ini q0 -0-> q1
        q0 -1-> q2
        q1 -0-> q1
        q1 -1-> q1
        q2 -0-> q3
        q2 -1-> q2
        q3 -0-> q2
        q3 -1-> q3
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case3(self):
        """Test Case 3 - More complex with non-deterministic transitions and lambda transitions."""
        automaton_str = """
        Automaton:
        Symbols: abc
        
        q0
        q1
        q2
        q3
        q4
        q5
        q6
        q7
        q8 final
        
        ini q0 --> q1
        q0 --> q8
        q1 --> q2
        q1 --> q5
        q2 -a-> q3
        q3 -b-> q4
        q4 --> q7
        q5 -c-> q6
        q6 --> q7
        q7 --> q1
        q7 --> q8
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: abc
        
        q0 final
        q1
        Empty
        q2 final
        q3 final
        
        ini q0 -a-> q1
        q0 -b-> Empty
        q0 -c-> q2
        q1 -a-> Empty
        q1 -b-> q3
        q1 -c-> Empty
        Empty -a-> Empty
        Empty -b-> Empty
        Empty -c-> Empty
        q2 -a-> q1
        q2 -b-> Empty
        q2 -c-> q2
        q3 -a-> q1
        q3 -b-> Empty
        q3 -c-> q2
        
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)


if __name__ == '__main__':
    unittest.main()
