import unittest

from src.grammar import Grammar, LL1Table, ParseTree, SyntaxError
from src.utils import GrammarFormat
from typing import Optional, Type

class TestAnalyze(unittest.TestCase):
    def _check_analyze(
            self,
            table: LL1Table,
            input_string: str,
            start: str,
            exception: Optional[Type[Exception]] = None
    ) -> None:
        with self.subTest(string=input_string):
            if exception is None:
                if table.analyze(input_string, start) is not None: print("✅", end="")
                else: print("❌", end="")
                self.assertTrue(table.analyze(input_string, start) is not None)
            else:
                with self.assertRaises(exception):
                    try:
                        table.analyze(input_string, start)
                    except exception:
                        print("✅", end="")
                        raise

    def _check_analyze_from_grammar(
            self,
            grammar: Grammar,
            input_string: str,
            start: str,
            exception: Optional[Type[Exception]] = None
    ) -> None:
        with self.subTest(string=input_string):
            table = grammar.get_ll1_table()
            self.assertTrue(table is not None)
            if table is not None:
                if exception is None:
                    if table.analyze(input_string, start) is not None: print("✅", end="")
                    else: print("❌", end="")
                    self.assertTrue(table.analyze(input_string, start) is not None)
                else:
                    with self.assertRaises(exception):
                        try:
                            table.analyze(input_string, start)
                        except exception:
                            print("✅", end="")
                            raise

    def _check_parse_tree(
            self,
            table: LL1Table,
            input_string: str,
            start: str,
            tree: ParseTree,
            exception: Optional[Type[Exception]] = None
    ) -> None:
        with self.subTest(string=input_string):
            if exception is None:
                res_tree = table.analyze(input_string, start)
                if res_tree == tree:
                    print("✅", end="")
                else:
                    print("❌", end="")
                self.assertEqual(res_tree, tree)
            else:
                with self.assertRaises(exception):
                    try:
                        table.analyze(input_string, start)
                    except exception:
                        print("✅", end="")
                        raise

    def test_case1(self) -> None:
        """Test for syntax analysis from table."""
        terminals = {"(", ")", "i", "+", "*", "$"}
        non_terminals = {"E", "T", "X", "Y"}
        cells = [('E', '(', 'TX'),
                 ('E', 'i', 'TX'),
                 ('T', '(', '(E)'),
                 ('T', 'i', 'iY'),
                 ('X', '+', '+E'),
                 ('X', ')', ''),
                 ('X', '$', ''),
                 ('Y', '*', '*T'),
                 ('Y', '+', ''),
                 ('Y', ')', ''),
                 ('Y', '$', '')]
        table = LL1Table(non_terminals, terminals)
        for (nt, t, body) in cells:
            table.add_cell(nt, t, body)

        print()
        # Casos típicos válidos
        self._check_analyze(table, "i*i$", "E")
        self._check_analyze(table, "i*i+i$", "E")
        self._check_analyze(table, "i*i+i+(i*i)$", "E")

        # Casos extraños o límite
        # Símbolo inválido de la entrada
        self._check_analyze(table, "a", "E", exception=SyntaxError)
        # Paréntesis sin cerrar
        self._check_analyze(table, "(i$", "E", exception=SyntaxError)
        # Caracteres de la cadena "pegados" después del $
        self._check_analyze(table, "i*i$i", "E", exception=SyntaxError)
        # Falta el símbolo $
        self._check_analyze(table, "i*i", "E", exception=SyntaxError)
        # Cadena empezando con operador
        self._check_analyze(table, "+i*i", "E", exception=SyntaxError)
        # Cadena finalizando con operador
        self._check_analyze(table, "i*i+", "E", exception=SyntaxError)
        # Símbolo después del $ al final
        self._check_analyze(table, "i*i+i+(i*i)$i", "E", exception=SyntaxError)
        # Varios símbolos $ en la cadena
        self._check_analyze(table, "i*i$i$", "E", exception=SyntaxError)
        # Entrada vacía
        self._check_analyze(table, "", "E", exception=SyntaxError)
        # Solo el símbolo $
        self._check_analyze(table, "$", "E", exception=SyntaxError)
        # Solo un paréntesis de cierre
        self._check_analyze(table, ")$", "E", exception=SyntaxError)
        # Expresión vacía entre paréntesis
        self._check_analyze(table, "()", "E", exception=SyntaxError)
        # Entrada con espacios (los espacios no forman parte de los terminales)
        self._check_analyze(table, "i * i $", "E", exception=SyntaxError)
        # Expresión imposible con dos operadores seguidos
        self._check_analyze(table, "i**i$", "E", exception=SyntaxError)
        print()


    def test_case2(self) -> None:
        """Test for syntax analysis from grammar."""
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

        # first_e = grammar.compute_first("TX")
        # print(f"     => First(E -> TX): {first_e}")
        # first_x = grammar.compute_first("+E")
        # print(f"     => First(X -> +E): {first_x}")
        # first_ = grammar.compute_first("")
        # print(f"     => First(X -> ): {first_}")
        # first_t = grammar.compute_first("iY")
        # print(f"     => First(T -> iY): {first_t}")
        # first_y = grammar.compute_first("(E)")
        # print(f"     => First(T -> (E)): {first_y}")
        # follow_e = grammar.compute_first("*T")
        # print(f"     => First(Y -> *T): {follow_e}")
        # first_ = grammar.compute_first("")
        # print(f"     => First(Y -> ): {first_}")

        # follow_e = grammar.compute_follow("E")
        # print(f"     => Follow(E): {follow_e}")
        # follow_x = grammar.compute_follow("X")
        # print(f"     => Follow(X): {follow_x}")
        # follow_t = grammar.compute_follow("T")
        # print(f"     => Follow(T): {follow_t}")
        # follow_y = grammar.compute_follow("Y")
        # print(f"     => Follow(Y): {follow_y}")

        print()
        self._check_analyze_from_grammar(grammar, "i*i$", "E")
        self._check_analyze_from_grammar(grammar, "i*i+i$", "E")
        self._check_analyze_from_grammar(grammar, "i*i+i+(i*i)$", "E")
        self._check_analyze_from_grammar(grammar, "a", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "(i$", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "i*i$i", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "i*i", "E", exception=SyntaxError)
        self._check_analyze_from_grammar(grammar, "+i*i", "E", exception=SyntaxError)

        # Valid regular cases
        self._check_analyze_from_grammar(grammar, "i*i$", "E")  # simple multiplication
        self._check_analyze_from_grammar(grammar, "i+i$", "E")  # simple addition
        self._check_analyze_from_grammar(grammar, "(i)$", "E")  # simple parenthesized

        # More complex valid cases
        self._check_analyze_from_grammar(grammar, "i*i+i$", "E")  # multiplication then addition
        self._check_analyze_from_grammar(grammar, "i*i+i+(i*i)$", "E")  # nested parentheses
        self._check_analyze_from_grammar(grammar, "(((i)))$", "E")  # deeply nested

        # Edge and unusual cases - valid
        self._check_analyze_from_grammar(grammar, "i$", "E")        # Single i, minimal
        self._check_analyze_from_grammar(grammar, "i+i+i$", "E")    # chain addition
        self._check_analyze_from_grammar(grammar, "i*i*i$", "E")    # chain multiplication

        # Edge - invalid syntax or input
        self._check_analyze_from_grammar(grammar, "a", "E", exception=SyntaxError)    # invalid character
        self._check_analyze_from_grammar(grammar, "", "E", exception=SyntaxError)     # completely empty
        self._check_analyze_from_grammar(grammar, "$", "E", exception=SyntaxError)    # just end marker
        self._check_analyze_from_grammar(grammar, "()", "E", exception=SyntaxError)   # empty parentheses
        self._check_analyze_from_grammar(grammar, "($", "E", exception=SyntaxError)   # opening parenthesis with no expression
        self._check_analyze_from_grammar(grammar, "(i$", "E", exception=SyntaxError)  # missing closing parenthesis

        self._check_analyze_from_grammar(grammar, "i*i$i", "E", exception=SyntaxError)  # suffix after correct expr
        self._check_analyze_from_grammar(grammar, "i*i", "E", exception=SyntaxError)    # missing end marker
        self._check_analyze_from_grammar(grammar, "+i*i", "E", exception=SyntaxError)   # starts with operator
        self._check_analyze_from_grammar(grammar, "*i$", "E", exception=SyntaxError)    # starts with operator
        self._check_analyze_from_grammar(grammar, "i++i$", "E", exception=SyntaxError)  # repeated operator

        # Terminal errors
        self._check_analyze_from_grammar(grammar, "i*i)$((", "E", exception=SyntaxError)  # excess unmatched parens
        self._check_analyze_from_grammar(grammar, "i(i)$", "E", exception=SyntaxError)    # invalid parenthesis use

        # Token separation error (spaces are not terminals)
        self._check_analyze_from_grammar(grammar, "i * i $", "E", exception=SyntaxError)  # spaces

        # Test with only parentheses
        self._check_analyze_from_grammar(grammar, "())$", "E", exception=SyntaxError)     # only parentheses
        print()

    def test_case3(self) -> None:
        """Test for parse tree construction."""
        terminals = {"(", ")", "i", "+", "*", "$"}
        non_terminals = {"E", "T", "X", "Y"}
        cells = [('E', '(', 'TX'),
                 ('E', 'i', 'TX'),
                 ('T', '(', '(E)'),
                 ('T', 'i', 'iY'),
                 ('X', '+', '+E'),
                 ('X', ')', ''),
                 ('X', '$', ''),
                 ('Y', '*', '*T'),
                 ('Y', '+', ''),
                 ('Y', ')', ''),
                 ('Y', '$', '')]
        table = LL1Table(non_terminals, terminals)
        for (nt, t, body) in cells:
            table.add_cell(nt, t, body)

        print()

        t01 = ParseTree("λ")
        t02 = ParseTree("X", [t01])
        t03 = ParseTree("λ")
        t04 = ParseTree("Y", [t03])
        t05 = ParseTree("i")
        t06 = ParseTree("T", [t05, t04])
        t07 = ParseTree("*")
        t08 = ParseTree("Y", [t07, t06])
        t09 = ParseTree("i")
        t10 = ParseTree("T", [t09, t08])
        tree = ParseTree("E", [t10, t02])
        self._check_parse_tree(table, "i*i$", "E", tree)

        t01 = ParseTree("λ")
        t02 = ParseTree("X", [t01])
        t03 = ParseTree("λ")
        t04 = ParseTree("Y", [t03])
        t05 = ParseTree("i")
        t06 = ParseTree("T", [t05, t04])
        t07 = ParseTree("+")
        t13 = ParseTree("λ")
        t12 = ParseTree("X", [t13])
        t11 = ParseTree("λ")
        t10 = ParseTree("Y", [t11])
        t09 = ParseTree("i")
        t08 = ParseTree("T", [t09, t10])
        t07b = ParseTree("E", [t08, t12])
        t06b = ParseTree("X", [t07, t07b])
        tree = ParseTree("E", [t06, t06b])
        self._check_parse_tree(table, "i+i$", "E", tree)

        t01 = ParseTree("λ")
        t02 = ParseTree("Y", [t01])
        t03 = ParseTree("i")
        t04 = ParseTree("T", [t03, t02])
        t05 = ParseTree("*")
        t06 = ParseTree("T", [t04, t05])
        t07 = ParseTree("λ")
        t08 = ParseTree("Y", [t07])
        t09 = ParseTree("i")
        t10 = ParseTree("T", [t09, t08])
        t11 = ParseTree("*")
        t12 = ParseTree("T", [t10, t11])
        t13 = ParseTree("Y", [t11, t10])

        t01 = ParseTree("λ")
        t02 = ParseTree("Y", [t01])
        t03 = ParseTree("i")
        t04 = ParseTree("T", [t03, t02])
        t05 = ParseTree("*")
        t06 = ParseTree("Y", [t05, t04])
        t07 = ParseTree("i")
        t08 = ParseTree("T", [t07, t06])
        t09 = ParseTree("+")
        t10 = ParseTree("λ")
        t11 = ParseTree("Y", [t10])
        t12 = ParseTree("i")
        t13 = ParseTree("T", [t12, t11])
        t14 = ParseTree("X", [t10])
        t15 = ParseTree("E", [t13, t14])
        t16 = ParseTree("X", [t09, t15])

        tree = ParseTree("E", [t08, t16])
        self._check_parse_tree(table, "i*i+i$", "E", tree)

        print()

if __name__ == '__main__':
    unittest.main()