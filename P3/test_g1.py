import unittest

from src.g1_parser import *

class TestGrammar(unittest.TestCase):
    def _check_analyze(self, input_string, valid):
        try:
            result = parser.parse(input_string)
            assert(result == valid)
        except:
            assert(not valid)

    def test_case_1(self):
        # n = 2, k = 3, k >= n+1 => True
        self._check_analyze("aabbccc", True)

    def test_case_2(self):
        # n = 2, k = 2, k < n+1 => False
        self._check_analyze("aabbcc", False)

    def test_case_3(self):
        # n = 0, k = 1, k >= n+1 => True
        self._check_analyze("c", True)
    
    def test_case_4(self):
        # n = 0, k = 2, k >= n+1 => True
        self._check_analyze("cc", True)

    def test_case_5(self):
        # n = 0, k = 0, k < n+1 => False
        self._check_analyze("", False)
    
    def test_case_6(self):
        # n = 1, k = 2, k >= n+1 => True
        self._check_analyze("abcc", True)
    
    def test_case_7(self):
        # n = 1, k = 1, k < n+1 => False
        self._check_analyze("abc", False)

    def test_case_8(self):
        # n = 2, k = 4, k >= n+1 => True
        self._check_analyze("aabbcccc", True)
    
    def test_case_9(self):
        # n = 3, k = 4, k >= n+1 => True
        self._check_analyze("aaabbbcccc", True)
    
    def test_case_10(self):
        # n = 3, k = 3, k < n+1 => False
        self._check_analyze("aaabbbccc", False)

    def test_case_11(self):
        # n = 3, k = 6, k >= n+1 => True
        self._check_analyze("aaabbbcccccc", True)
    
    def test_case_12(self):
        # n = 0, k = 3, k >= n+1 => True
        self._check_analyze("ccc", True)
    
    def test_case_13(self):
        # Extra: n = 0, k = 0, False (k < n+1)
        self._check_analyze("", False)
    
    def test_case_14(self):
        # Extra: n = 2, k = 5, True
        self._check_analyze("aabbccccc", True)

    def test_case_15(self):
        # Mal formed strings: wrong letter order or counts
        self._check_analyze("ab", False)        # not enough c's
    
    def test_case_16(self):
        self._check_analyze("aabbbcc", False)   # too many b's
    
    def test_case_17(self):
        self._check_analyze("abbc", False)      # not enough a's

    def test_case_18(self):
        self._check_analyze("bacc", False)      # letters out of order
    
    def test_case_19(self):
        self._check_analyze("aaabbbbc", False)  # too many b's
    
    def test_case_20(self):
        self._check_analyze("aacbbbc", False)   # c in the middle
    
    def test_case_21(self):
        self._check_analyze("aabbcdd", False)   # contains an invalid letter d


if __name__ == '__main__':
    unittest.main()