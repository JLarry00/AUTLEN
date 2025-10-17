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
        
    def add_transition(self, start_state, symbol, end_state):
        # Validación de parámetros None
        if start_state is None or end_state is None:
            return False

        # Agregar la transición a la estructura
        if start_state in self.transitions:
            if symbol in self.transitions[start_state]:
                if end_state in self.transitions[start_state][symbol]:
                    return True  # La transición ya existe
                else:
                    self.transitions[start_state][symbol].add(end_state)
            else:
                self.transitions[start_state][symbol] = {end_state}
        else:
            self.transitions[start_state] = {symbol: {end_state}}
        
        return True
    
    def lambda_transitions(self, current_states):
        new_states = set()
        for state in current_states:
            if state in self.transitions:
                transitions = self.transitions[state]
                for s in transitions:
                    if s == None:
                        new_states.update(self.lambda_transitions(transitions[s]))
        current_states.update(new_states)
        return current_states

    def accepts(self, cadena):
        current_states = {self.initial_state} # Set of states
        i = 0

        while True:
            current_states = self.lambda_transitions(current_states)

            if len(cadena) == 0: break
            symbol = cadena[i]
            i += 1
            if symbol not in self.symbols:
                return False
            
            next_states = set()
            for state in current_states:

                if state not in self.transitions: continue
                if symbol not in self.transitions[state]: continue

                next_states.update(self.transitions[state][symbol])
            current_states = next_states

            if i >= len(cadena): break
        
        return current_states.intersection(self.final_states) != set()

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
