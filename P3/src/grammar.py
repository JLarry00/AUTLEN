from __future__ import annotations

from collections import deque
from logging import raiseExceptions
from operator import length_hint
from typing import AbstractSet, Collection, MutableSet, Optional, Dict, List, Optional

class RepeatedCellError(Exception):
    """Exception for repeated cells in LL(1) tables."""

class SyntaxError(Exception):
    """Exception for parsing errors."""

class Grammar:
    """
    Class that represents a grammar.

    Args:
        terminals: Terminal symbols of the grammar.
        non_terminals: Non terminal symbols of the grammar.
        productions: Dictionary with the production rules for each non terminal
          symbol of the grammar.
        axiom: Axiom of the grammar.

    """

    def __init__(
        self,
        terminals: AbstractSet[str],
        non_terminals: AbstractSet[str],
        productions: Dict[str, List[str]],
        axiom: str,
    ) -> None:
        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        if axiom not in non_terminals:
            raise ValueError(
                "Axiom must be included in the set of non terminals.",
            )

        if non_terminals != set(productions.keys()):
            raise ValueError(
                f"Set of non-terminals and productions keys should be equal."
            )
        
        for nt, rhs in productions.items():
            if not rhs:
                raise ValueError(
                    f"No production rules for non terminal symbol {nt} "
                )
            for r in rhs:
                for s in r:
                    if (
                        s not in non_terminals
                        and s not in terminals
                    ):
                        raise ValueError(
                            f"Invalid symbol {s}.",
                        )

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions
        self.axiom = axiom

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"axiom={self.axiom!r}, "
            f"productions={self.productions!r})"
        )


    def compute_first(self, sentence: str) -> AbstractSet[str]:
        """
        Method to compute the first set of a string.

        Args:
            str: string whose first set is to be computed.

        Returns:
            First set of str.
        """
        if len(sentence) == 0: return set([''])

        first = set()
        for s in sentence:
            if s not in self.non_terminals and s not in self.terminals: raise ValueError(f"Invalid symbol: {s}")

            if s in self.terminals:
                first.add(s)
                first.discard('')
                break
            
            first_s = set()
            for rule in self.productions[s]:
                if len(rule) == 0:
                    first_s.add('')
                    continue
                elif rule[0] in self.terminals:
                    first_s.add(rule[0])
                    continue
                elif rule[0] in self.non_terminals:
                    if rule[0] == s: continue
                    first_s.update(self.compute_first(rule))

            first.update(first_s)

            if '' not in first: break

            if s == sentence[-1] and '' not in first_s: first.discard('')

        return first
	# TO-DO: Complete this method for exercise 3...


    def compute_follow(self, symbol: str) -> AbstractSet[str]:
        """
        Method to compute the follow set of a non-terminal symbol.

        Args:
            symbol: non-terminal whose follow set is to be computed.

        Returns:
            Follow set of symbol.
        """
        # Comprobación básica: tiene que ser NO terminal
        if symbol not in self.non_terminals:
            raise ValueError(f"Invalid non-terminal symbol: {symbol}")

        # FOLLOW(X) para todos los no terminales, inicialmente vacío
        follow: Dict[str, AbstractSet[str]] = {
            nt: set() for nt in self.non_terminals
        }

        # Regla (1): añadir '$' al axioma
        follow[self.axiom].add('$')

        # Algoritmo iterativo tipo "hasta alcanzar punto fijo"
        changed = True
        while changed:
            changed = False

            # Recorremos TODAS las producciones A -> rhs
            for A, rhss in self.productions.items():
                for rhs in rhss:
                    # rhs es un string (cadena de símbolos)
                    for i, X in enumerate(rhs):
                        # Solo nos interesan las ocurrencias de NO terminales
                        if X not in self.non_terminals:
                            continue

                        # β = "lo que viene después de X" en la producción A -> α X β
                        beta = rhs[i+1:]

                        if beta:
                            # Regla (2): añadir FIRST(β) - {λ} a FOLLOW(X)
                            first_beta = self.compute_first(beta)
                            to_add = set(first_beta)
                            if '' in to_add:
                                to_add.remove('')   # quitamos λ

                            if not to_add.issubset(follow[X]):
                                follow[X] |= to_add
                                changed = True

                            # Regla (3): si λ ∈ FIRST(β), añadir FOLLOW(A) a FOLLOW(X)
                            if '' in first_beta:
                                if not follow[A].issubset(follow[X]):
                                    follow[X] |= follow[A]
                                    changed = True
                        else:
                            # Caso A -> α X   (β vacío):
                            # Regla (3) directa: añadir FOLLOW(A) a FOLLOW(X)
                            if not follow[A].issubset(follow[X]):
                                follow[X] |= follow[A]
                                changed = True

        # Devolvemos FOLLOW(symbol); por definición no debe contener λ
        return follow[symbol]


    def get_ll1_table(self) -> Optional[LL1Table]:
        """
        Method to compute the LL(1) table.

        Returns:
            LL(1) table for the grammar, or None if the grammar is not LL(1).
        """
        Table = LL1Table(self.non_terminals, self.terminals | {'$'})
        for non_terminal, productions in self.productions.items():
            for production in productions:
                
                first_p = self.compute_first(production)

                for f_terminal in first_p:

                    if f_terminal == '':

                        next_p = self.compute_follow(non_terminal)
                        
                        for n_terminal in next_p:

                            if n_terminal == '':
                                raise Exception(f"Error en la función follow: SIGUIENTE({non_terminal}) contiene lambda")

                            if not(n_terminal in self.terminals or n_terminal == '$'):
                                if n_terminal not in self.non_terminals:
                                    raise ValueError(f"Invalid symbol: {n_terminal}")
                                continue
                            
                            if Table.cells[non_terminal][n_terminal] is not None: return None

                            Table.add_cell(non_terminal, n_terminal, production)
                    else:
                        if f_terminal not in self.terminals:
                            if f_terminal not in self.non_terminals:
                                raise ValueError(f"Invalid symbol: {f_terminal}")
                            continue
                        
                        if Table.cells[non_terminal][f_terminal] is not None:
                            return None

                        Table.add_cell(non_terminal, f_terminal, production)
        return Table
	# TO-DO: Complete this method for exercise 5...


    def is_ll1(self) -> bool:
        return self.get_ll1_table() is not None


class LL1Table:
    """
    LL1 table. Initially all cells are set to None (empty). Table cells
    must be filled by calling the method add_cell.

    Args:
        non_terminals: Set of non terminal symbols.
        terminals: Set of terminal symbols.

    """

    def __init__(
        self,
        non_terminals: AbstractSet[str],
        terminals: AbstractSet[str],
    ) -> None:

        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        self.terminals: AbstractSet[str] = terminals
        self.non_terminals: AbstractSet[str] = non_terminals
        self.cells: Dict[str, Dict[str, Optional[str]]] = {nt: {t: None for t in terminals} for nt in non_terminals}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"cells={self.cells!r})"
        )

    def add_cell(self, non_terminal: str, terminal: str, cell_body: str) -> None:
        """
        Adds a cell to an LL(1) table.

        Args:
            non_terminal: Non termial symbol (row)
            terminal: Terminal symbol (column)
            cell_body: content of the cell 

        Raises:
            RepeatedCellError: if trying to add a cell already filled.
        """
        if non_terminal not in self.non_terminals:
            raise ValueError(
                "Trying to add cell for non terminal symbol not included "
                "in table.",
            )
        if terminal not in self.terminals:
            raise ValueError(
                "Trying to add cell for terminal symbol not included "
                "in table.",
            )
        if not all(x in self.terminals | self.non_terminals for x in cell_body):
            raise ValueError(
                "Trying to add cell whose body contains elements that are "
                "not either terminals nor non terminals.",
            )            
        if self.cells[non_terminal][terminal] is not None:
            raise RepeatedCellError(
                f"Repeated cell ({non_terminal}, {terminal}).")
        else:
            self.cells[non_terminal][terminal] = cell_body

    def analyze2(self, input_string: str, start: str) -> ParseTree:
        """
        Method to analyze a string using the LL(1) table.

        Args:
            input_string: string to analyze.
            start: initial symbol.

        Returns:
            ParseTree object with either the parse tree (if the elective exercise is solved)
            or an empty tree (if the elective exercise is not considered).

        Raises:
            SyntaxError: if the input string is not syntactically correct.
        """
        if len(input_string) == 0: raise(SyntaxError(f"Input string not valid: empty string"))
        if input_string[-1] != "$": raise(SyntaxError(f"Input string not valid: missing $ at the end"))
        st = deque([start])
        input = deque(input_string)

        while len(st) > 0:
            elem = st.pop()
            c = input[0]
            if c not in self.terminals: raise(SyntaxError(f"Unknown symbol: {c}"))
            if elem in self.terminals:
                if elem == c: input.popleft()
                else: raise(SyntaxError(f"Terminal char in stack ({elem}) and input ({c}) differ"))

            elif elem in self.non_terminals:
                rule = self.cells[elem][c]

                if rule is None: raise(SyntaxError(f"No production rule for {elem} and {c}"))

                elif rule != "":
                    for char in reversed(rule): st.append(char)

            else:
                raise(SyntaxError(f"Unknown symbol: {elem}"))

        if c != "$": raise(SyntaxError(f"Input string not fully analyzed"))
        if len(input) > 1: raise(SyntaxError(f"Input string not fully analyzed"))
        
        return True
	# TO-DO: Complete this method for exercise 2...

    def  analyze(self, input_string: str, start: str) -> ParseTree:
        """
        Method to analyze a string using the LL(1) table.

        Args:
            input_string: string to analyze.
            start: initial symbol.

        Returns:
            ParseTree object with either the parse tree (if the elective exercise is solved)
            or an empty tree (if the elective exercise is not considered).

        Raises:
            SyntaxError: if the input string is not syntactically correct.
        """
        if len(input_string) == 0: raise(SyntaxError(f"Input string not valid: empty string"))
        if input_string[-1] != "$": raise(SyntaxError(f"Input string not valid: missing $ at the end"))
        st = deque([start])

        input = deque(input_string)
        tree = ParseTree(start)
        stack = deque([tree, ParseTree("$")])

        while len(stack) > 0:
            ptree = stack.popleft()
            elem = ptree.root
            c = input[0]
            if c not in self.terminals: raise(SyntaxError(f"Unknown symbol: {c}"))
            if elem in self.terminals:
                if elem == c: input.popleft()
                else: raise(SyntaxError(f"Terminal char in stack ({elem}) and input ({c}) differ"))

            elif elem in self.non_terminals:
                rule = self.cells[elem][c]

                if rule is None: raise(SyntaxError(f"No production rule for {elem} and {c}"))

                elif rule != "":
                    trees = deque()
                    for char in reversed(rule):
                        new_tree = ParseTree(char)
                        stack.appendleft(new_tree)
                        trees.appendleft(new_tree)
                    ptree.add_children(trees)
                else:
                    empty_tree = ParseTree("λ")
                    ptree.add_children([empty_tree])

            else:
                raise(SyntaxError(f"Unknown symbol: {elem}"))

        if c != "$": raise(SyntaxError(f"Input string not fully analyzed"))
        if len(input) > 1: raise(SyntaxError(f"Input string not fully analyzed"))
        
        return tree
    
    
class ParseTree():
    """
    Parse Tree.

    Args:
        root: root node of the tree.
        children: list of children, which are also ParseTree objects.
    """
    def __init__(self, root: str, children: Collection[ParseTree] = []) -> None:
        self.root = root
        self.children = children

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.root!r}: {self.children})"
        )
    
    def __str__(self) -> str:
        # Tree representation using unicode box-drawing characters,
        # fix: don't add initial 3-space padding for children of the root node.
        def _str_tree(node, prefix="", is_last=True, is_root=False):
            lines = []
            if is_root:
                # No connector or prefix for root
                lines.append(str(node.root))
            else:
                connector = "└── " if is_last else "├── "
                lines.append(prefix + connector + str(node.root))
            if node.children:
                child_count = len(node.children)
                for i, child in enumerate(node.children):
                    is_last_child = (i == child_count - 1)
                    # For children of the root node, do not add prefix (to avoid extra spaces)
                    if is_root:
                        new_prefix = " "
                    else:
                        new_prefix = prefix + ("    " if is_last else "│   ")
                    lines.append(_str_tree(child, new_prefix, is_last_child, False))
            return "\n".join(lines)
        # Render with is_root=True for the root node
        return _str_tree(self, "", True, True)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.root == other.root
            and len(self.children) == len(other.children)
            and all([x.__eq__(y) for x, y in zip(self.children, other.children)])
        )

    def add_children(self, children: Collection[ParseTree]) -> None:
        self.children = children
