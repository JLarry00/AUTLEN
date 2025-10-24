"""
    Equipo docente de Autómatas y Lenguajes Curso 2025-26
    Última modificación: 18 de septiembre de 2025
"""

from automaton import FiniteAutomaton

def _re_to_rpn(re_string):
    """
    Convert re to reverse polish notation (RPN).

    Does not check that the input re is syntactically correct.

    Args:
        re_string: Regular expression in infix notation. Type: str

    Returns:
        Regular expression in reverse polish notation. Type: str

    """
    stack = [] # List of strings
    rpn_string = ""
    for x in re_string:
        if x == "+":
            while len(stack) > 0 and stack[-1] != "(":
                rpn_string += stack.pop()
            stack.append(x)
        elif x == ".":
            while len(stack) > 0 and stack[-1] == ".":
                rpn_string += stack.pop()
            stack.append(x)
        elif x == "(":
            stack.append(x)
        elif x == ")":
            while stack[-1] != "(":
                rpn_string += stack.pop()
            stack.pop()
        else:
            rpn_string += x

    while len(stack) > 0:
        rpn_string += stack.pop()

    return rpn_string



class REParser():
    """Class for processing regular expressions in Kleene's syntax."""
    
    def __init__(self) -> None:
        self.state_counter = 0

    def _new_state(self):
        s = f"q{self.state_counter}"
        self.state_counter += 1
        return s


    def _epsilon_closure(self, aut, states):
        """Cierre-λ (None) sobre el autómata de Thompson ya construido."""
        stack = list(states)
        seen = set(states)
        while stack:
            s = stack.pop()
            for t in aut.transitions.get(s, {}).get(None, set()):
                if t not in seen:
                    seen.add(t)
                    stack.append(t)
        return seen

    def _remove_epsilons(self, aut):
        """
        Elimina transiciones λ del AFND:
        Para cada estado s y símbolo a:
            δ'(s,a) = ε-closure( move( ε-closure(s), a ) )
        Estados finales' = { s | ε-closure(s) ∩ F ≠ ∅ }
        """
        symbols = tuple(aut.symbols)  # mantenemos el alfabeto igual (sin None)
        states = list(aut.states)

        # 1) precalcular cierres ε de cada estado
        eclose = {s: self._epsilon_closure(aut, {s}) for s in states}

        # 2) construir nuevas transiciones sin None
        new_trans = {}
        for s in states:
            new_trans.setdefault(s, {})
            for a in symbols:
                # move desde todo el cierre ε de s
                T = set()
                for t in eclose[s]:
                    T |= aut.transitions.get(t, {}).get(a, set())
                # cierre ε después de consumir a
                T2 = set()
                for u in T:
                    T2 |= eclose[u]
                if T2:
                    new_trans[s][a] = T2

        # 3) estados finales nuevos: los que alcanzan un final vía ε
        new_finals = set()
        for s in states:
            if eclose[s] & aut.final_states:
                new_finals.add(s)

        # 4) devolver autómata sin λ
        return FiniteAutomaton(
            initial_state=aut.initial_state,
            states=states,
            symbols=symbols,
            transitions=new_trans,
            final_states=new_finals,
        )
   
    def _copy(self, A):
        return FiniteAutomaton(
            initial_state=A.initial_state,
            states=list(A.states),
            symbols=set(A.symbols),
            transitions={p:{a:set(T) for a,T in d.items()} for p,d in (A.transitions or {}).items()},
            final_states=set(A.final_states),
        )

    def _create_automaton_empty(self):
        """
        Create an automaton that accepts the empty language.

        Returns:
            Automaton that accepts the empty language. Type: FiniteAutomaton

        """
        q0 = self._new_state()
        return FiniteAutomaton(
            initial_state=q0,
            states=[q0],
            symbols=set(),
            transitions={},
            final_states=set(),
        )
        

    def _create_automaton_lambda(self):
        """
        Create an automaton that accepts the empty string.

        Returns:
            Automaton that accepts the empty string. Type: FiniteAutomaton

        """
        q0 = self._new_state()
        return FiniteAutomaton(
            initial_state=q0,
            states=[q0],
            symbols=set(),
            transitions={},
            final_states={q0},
        )


    def _create_automaton_symbol(self, symbol):
        """
        Create an automaton that accepts one symbol.

        Args:
            symbol: Symbol that the automaton should accept. Type: str

        Returns:
            Automaton that accepts a symbol. Type: FiniteAutomaton

        """
        q0, q1 = self._new_state(), self._new_state()
        return FiniteAutomaton(
            initial_state=q0,
            states=[q0, q1],
            symbols={symbol},
            transitions={q0: {symbol: {q1}}},
            final_states={q1},
        )

    def _create_automaton_star(self, A):
        """
        Create an automaton that accepts the Kleene star of another.

        Args:
            automaton: Automaton whose Kleene star must be computed. Type: FiniteAutomaton

        Returns:
            Automaton that accepts the Kleene star. Type: FiniteAutomaton

        """
        A = self._copy(A)
        qi, qf = self._new_state(), self._new_state()
        states = [qi, qf] + A.states
        symbols = set(A.symbols)
        trans = {p:{a:set(T) for a,T in d.items()} for p,d in (A.transitions or {}).items()}

        trans.setdefault(qi, {}).setdefault(None, set()).update({A.initial_state, qf})
        for f in A.final_states:
            trans.setdefault(f, {}).setdefault(None, set()).update({A.initial_state, qf})

        return FiniteAutomaton(qi, states, symbols, trans, {qf})


    def _create_automaton_union(self, A, B):
        """
        Create an automaton that accepts the union of two automata.

        Args:
            automaton1: First automaton of the union. Type: FiniteAutomaton.
            automaton2: Second automaton of the union. Type: FiniteAutomaton.

        Returns:
            Automaton that accepts the union. Type: FiniteAutomaton.

        """
        A, B = self._copy(A), self._copy(B)
        qi, qf = self._new_state(), self._new_state()
        states = [qi, qf] + A.states + B.states
        symbols = set(A.symbols) | set(B.symbols)
        trans = {p:{a:set(T) for a,T in d.items()} for p,d in (A.transitions or {}).items()}
        for p,d in (B.transitions or {}).items():
            trans.setdefault(p, {})
            for a,T in d.items():
                trans[p].setdefault(a, set()).update(T)

        trans.setdefault(qi, {}).setdefault(None, set()).update({A.initial_state, B.initial_state})
        for f in A.final_states | B.final_states:
            trans.setdefault(f, {}).setdefault(None, set()).add(qf)

        return FiniteAutomaton(qi, states, symbols, trans, {qf})


    def _create_automaton_concat(self, A, B):
        """
        Create an automaton that accepts the concatenation of two automata.

        Args:
            automaton1: First automaton of the concatenation. Type: FiniteAutomaton.
            automaton2: Second automaton of the concatenation. Type: FiniteAutomaton.

        Returns:
            Automaton that accepts the concatenation. Type: FiniteAutomaton.

        """
        A, B = self._copy(A), self._copy(B)
        states = A.states + B.states
        symbols = set(A.symbols) | set(B.symbols)
        trans = {p:{a:set(T) for a,T in d.items()} for p,d in (A.transitions or {}).items()}
        for p,d in (B.transitions or {}).items():
            trans.setdefault(p, {})
            for a,T in d.items():
                trans[p].setdefault(a, set()).update(T)

        for f in A.final_states:
            trans.setdefault(f, {}).setdefault(None, set()).add(B.initial_state)

        return FiniteAutomaton(A.initial_state, states, symbols, trans, set(B.final_states))


    def create_automaton(
        self,
        re_string,
    ):
        """
        Create an automaton from a regex.

        Args:
            re_string: String with the regular expression in Kleene notation. Type: str

        Returns:
            Automaton equivalent to the regex. Type: FiniteAutomaton

        """
        if not re_string:
            return self._create_automaton_empty()

        rpn_string = _re_to_rpn(re_string)
        stack = []
        self.state_counter = 0

        for x in rpn_string:
            if x == "*":
                aut = stack.pop()
                stack.append(self._create_automaton_star(aut))
            elif x == "+":
                aut2 = stack.pop()
                aut1 = stack.pop()
                stack.append(self._create_automaton_union(aut1, aut2))
            elif x == ".":
                aut2 = stack.pop()
                aut1 = stack.pop()
                stack.append(self._create_automaton_concat(aut1, aut2))
            elif x == "λ":
                stack.append(self._create_automaton_lambda())
            else:
                stack.append(self._create_automaton_symbol(x))

        nfa = stack.pop()
        #clave: eliminamos ε para que accepts() (sin cierre final) funcione
        return self._remove_epsilons(nfa)
