import unittest

from src.roman_parser2 import *

class TestRommanGrammar(unittest.TestCase):
    def _check_analyze(self, input_string, int_value, valid):
        try:
            result = parser.parse(input_string)
            if not valid:
                assert(result["valid"] == valid)
            else:
                assert(result["valid"] == valid and result["val"] == int_value)
        except:
            assert(not valid)

    def test_cases_1(self):
        self._check_analyze("XX", 20, True)

    def test_cases_2(self):
        self._check_analyze("IX", 9, True)

    def test_cases_3(self):
        self._check_analyze("XII", 12, True)

    def test_cases_4(self):
        self._check_analyze("XIIII", 13, False)

    def test_cases_5_empty_string(self):
        self._check_analyze("", 0, True)  # An empty string is treated as lambda -> 0

    def test_cases_6_single_digit(self):
        self._check_analyze("I", 1, True)
        self._check_analyze("V", 5, True)
        self._check_analyze("X", 10, True)
        self._check_analyze("L", 50, True)
        self._check_analyze("C", 100, True)
        self._check_analyze("D", 500, True)
        self._check_analyze("M", 0, False)  # Out of grammar: 'M' at this level not handled

    def test_cases_7_valid_basic_numbers(self):
        self._check_analyze("II", 2, True)
        self._check_analyze("III", 3, True)
        self._check_analyze("IV", 4, True)
        self._check_analyze("VI", 6, True)
        self._check_analyze("VII", 7, True)
        self._check_analyze("VIII", 8, True)
        self._check_analyze("XIX", 19, True)
        self._check_analyze("XXI", 21, True)

    def test_cases_8_tens_and_units(self):
        self._check_analyze("XL", 40, True)
        self._check_analyze("XC", 90, True)
        self._check_analyze("LXXX", 80, True)
        self._check_analyze("LXXXIII", 83, True)
        self._check_analyze("XCIX", 99, True)
        self._check_analyze("XLIV", 44, True)

    def test_cases_9_hundreds(self):
        self._check_analyze("C", 100, True)
        self._check_analyze("CC", 200, True)
        self._check_analyze("CCC", 300, True)
        self._check_analyze("CD", 400, True)
        self._check_analyze("D", 500, True)
        self._check_analyze("DC", 600, True)
        self._check_analyze("DCCC", 800, True)
        self._check_analyze("CM", 900, True)

    def test_cases_10_full_numbers(self):
        self._check_analyze("CXLIV", 144, True)
        self._check_analyze("CDXLIV", 444, True)
        self._check_analyze("XCIV", 94, True)
        self._check_analyze("CCLXXXIV", 284, True)
        self._check_analyze("LXXXVIII", 88, True)
        self._check_analyze("CCCXCIX", 399, True)
        self._check_analyze("CMXCIX", 999, True)  # Not supported, max is 999, but check validity

    def test_cases_11_overflows_and_invalid(self):
        self._check_analyze("IIII", -1, False)
        self._check_analyze("XXXX", -1, False)
        self._check_analyze("CCCC", -1, False)
        self._check_analyze("VV", -1, False)
        self._check_analyze("LL", -1, False)
        self._check_analyze("DD", -1, False)
        self._check_analyze("VX", -1, False)
        self._check_analyze("IC", -1, False)
        self._check_analyze("IL", -1, False)
        self._check_analyze("XD", -1, False)
        self._check_analyze("IM", -1, False)
        self._check_analyze("XIIII", -1, False)
        self._check_analyze("MCM", -1, False)  # Out of range (M not handled at hundreds)

    def test_cases_12_mixed_cases(self):
        self._check_analyze("IXIX", -1, False)
        self._check_analyze("IXX", -1, False)
        self._check_analyze("XIC", -1, False)
        self._check_analyze("VIIII", -1, False)
        self._check_analyze("CIL", -1, False)
        self._check_analyze("VL", -1, False)
        self._check_analyze("CXI", 111, True)
        self._check_analyze("VIII", 8, True)
        self._check_analyze("XCVIII", 98, True)
        self._check_analyze("CDLXXXIII", 483, True)

    def test_cases_13_leading_trailing_invalid(self):
        self._check_analyze("IC", -1, False)
        self._check_analyze("VX", -1, False)
        self._check_analyze("LC", -1, False)
        self._check_analyze("DM", -1, False)
        self._check_analyze("CDXCXLIV", -1, False)

    def test_cases_14_non_roman_characters(self):
        self._check_analyze("ABC", -1, False)
        self._check_analyze("X2C", -1, False)
        self._check_analyze("xvi", -1, False)  # lowercase not valid in lexer rules

    def test_cases_15_spaces(self):
        self._check_analyze("X X", -1, False)
        self._check_analyze(" I I ", -1, False)
        self._check_analyze("  ", 0, True)  # Whitespaces only: reduces to lambda

    def test_cases_16_higher_values(self):
        # 999 is not directly representable unless the grammar handles M, which it doesn't
        self._check_analyze("CMXCIX", 999, True)
        # Out of grammar (since only hundreds supported, M not counted)
        self._check_analyze("M", -1, False)
        self._check_analyze("MM", -1, False)


if __name__ == '__main__':
    unittest.main()
