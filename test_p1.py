#!/usr/bin/env python

import re
import unittest

from regular_expressions import RE0, RE1, RE2, RE3, RE4, RE5, RE6


class TestP0(unittest.TestCase):
    """Tests of assignment 0."""

    def check_expression(self, expr: str, string: str, expected: bool) -> None:
        with self.subTest(string=string):
            match = re.fullmatch(expr, string)
            self.assertEqual(bool(match), expected)

    def test_exercise_0(self) -> None:
        self.check_expression(RE0, "a", True)
        self.check_expression(RE0, "bbbbaba", True)
        self.check_expression(RE0, "abbab", False)
        self.check_expression(RE0, "b", False)

    def test_exercise_1(self) -> None:
        pass
        self.check_expression(RE1, "", True)
        self.check_expression(RE1, "00", True)
        self.check_expression(RE1, "110101", True)
        self.check_expression(RE1, "11010100000", True)
        self.check_expression(RE1, "1", False)
        self.check_expression(RE1, "1ba", False)
        

    def test_exercise_2(self) -> None:
        pass
        self.check_expression(RE2, "", True)
        self.check_expression(RE2, "0", True)
        self.check_expression(RE2, "1010", True)
        self.check_expression(RE2, "010", True)
        self.check_expression(RE2, "0101", True)
        self.check_expression(RE2, "1ba", False)
        self.check_expression(RE2, "11", False)
        self.check_expression(RE2, "00", False)

    def test_exercise_3(self) -> None:
        self.check_expression(RE3, "0", True)
        self.check_expression(RE3, "24", True)
        self.check_expression(RE3, "0.0", True)
        self.check_expression(RE3, "-12", True)
        self.check_expression(RE3, "+3.14", True)
        self.check_expression(RE3, "42.0", True)
        self.check_expression(RE3, "00", False)
        self.check_expression(RE3, "012", False)
        self.check_expression(RE3, "3.", False)
        self.check_expression(RE3, "00", False)

    def test_exercise_4(self) -> None:
        self.check_expression(RE4, "juan.perez@estudiante.uam.es", True)
        self.check_expression(RE4, "maria.gonzalez@uam.es", True)
        self.check_expression(RE4, "ana.martin@estudiante.uam.es", True)
        self.check_expression(RE4, "pedro.sanchez@uam.es", True)
        self.check_expression(RE4, "Juan.Perez@estudiante.uam.es", False)
        self.check_expression(RE4, "juan.perez@UAM.es", False)
        self.check_expression(RE4, "juan_perez@estudiante.uam.es", False)
        self.check_expression(RE4, "juan@estudiante.uam.es", False)

    def test_exercise_5(self) -> None:
        self.check_expression(RE5, "01/12/2025", True)
        self.check_expression(RE5, "09/01/0000", True)
        self.check_expression(RE5, "31/05/9999", True)
        self.check_expression(RE5, "05/10/0045", True)
        self.check_expression(RE5, "20/02/2025", True)
        self.check_expression(RE5, "1/03/0125", False)
        self.check_expression(RE5, "01/3/0125", False)
        self.check_expression(RE5, "01/03/125", False)
        self.check_expression(RE5, "dd/mm/aaaa", False)
        self.check_expression(RE5, "30/02/2025", False)
        self.check_expression(RE5, "31/02/2025", False)
        self.check_expression(RE5, "32/01/2025", False)
        self.check_expression(RE5, "31/06/2025", False)


    def test_exercise_6(self) -> None:
        self.check_expression(RE6, "192.168.0.1", True)
        self.check_expression(RE6, "0.1.192.168", True)
        self.check_expression(RE6, "10.0.0.255", True)
        self.check_expression(RE6, "0.0.0.0", True)
        self.check_expression(RE6, "172.16.254.1", True)
        self.check_expression(RE6, "8.8.8.8", True)
        self.check_expression(RE6, "256.100.50.25", False)
        self.check_expression(RE6, "192.168.0", False)
        self.check_expression(RE6, "172.16.0.256", False)
        self.check_expression(RE6, "10.0.0.1.2", False)
        

if __name__ == '__main__':
    unittest.main()
