"""
    Equipo docente de Autómatas y Lenguajes Curso 2025-26
    Última modificación: 18 de septiembre de 2025
"""

from collections import deque
from graphviz import Digraph
from utils import is_deterministic

"""
    Podéis implementar cualquier función auxiliar que consideréis necesaria
"""

class FiniteAutomaton:

    def __init__(self, initial_state, states, symbols, transitions, final_states):
        self.initial_state = initial_state
        self.states = states
        self.symbols = symbols
        self.transitions = transitions  # Ya viene como dicc de diccs
        self.final_states = final_states
        
    # Mejorar control de errores
    def add_transition(self, start_state, symbol, end_state):
        if  (start_state is None) or (symbol is None) or (end_state is None) or \
            (start_state not in self.states) or (symbol not in self.symbols) or (end_state not in self.states):
            return False

        if start_state in self.transitions:
            if symbol in self.transitions[start_state]:
                if end_state in self.transitions[start_state][symbol]:
                    return True
                else:
                    self.transitions[start_state][symbol].add(end_state)
            else:
                self.transitions[start_state][symbol] = set(end_state)
        else:
            self.transitions[start_state] = {symbol: set(end_state)}
        
        return True

    def accepts(self, cadena):
        
        return True

    def to_deterministic(self):
        pass

    def to_minimized(self):
        pass
        
    def draw(self, path="./images/", filename="automata.png", view=False):
        dot = Digraph(comment="Automata", format="png")
        dot.attr(rankdir="LR")

        # Nodo invisible para punto inicial
        dot.node("", shape="none")

        # Almacenar estados
        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape="doublecircle")
            else:
                dot.node(state, shape="circle")
        
        # Flecha al estado inicial
        dot.edge("", self.initial_state)

        # Almacenar transiciones
        for state_ini in self.transitions:
            for symbol in self.transitions[state_ini]:
                for state_fin in self.transitions[state_ini][symbol]:
                    dot.edge(state_ini, state_fin, symbol if symbol is not None else "λ")

        dot.render(path+filename, view=view)
