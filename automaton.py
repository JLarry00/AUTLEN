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
                    if s is None:
                        new_states.update(self.lambda_transitions(transitions[s]))
        current_states.update(new_states)
        return current_states

    def symbol_transitions(self, current_states, symbol):
        #print(f"symbol_transitions: {current_states} {symbol}")
        new_states = set()
        for state in current_states:
            #print(f"state: {state}")
            if state in self.transitions:
                #print(f"state in transitions: {state}")
                transitions = self.transitions[state]
                #print(f"transitions: {transitions}")
                for s in transitions:
                    #print(f"s: {s}")
                    if s is symbol:
                        #print(f"s is symbol: {s}")
                        new_states.update(self.lambda_transitions(transitions[s]))
        #print(f"new_states: {new_states}")
        return new_states

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
        current_states = self.lambda_transitions(current_states)
        
        return current_states.intersection(self.final_states) != set()

    def to_deterministic(self):
        from re_parser import REParser
        rp = REParser()

        debug = False
        #debug = True

        init_st_set = self.lambda_transitions({self.initial_state})
        all_st_set_list = [init_st_set]
        new_init_st = rp._new_state()
        new_st_list = [new_init_st]
        new_final_states = set()
        if init_st_set.intersection(self.final_states) != set():
            new_final_states.add(new_init_st)

        if debug: print(self)

        A = FiniteAutomaton(new_init_st, new_st_list, self.symbols, {}, set())

        i = 0
        while i < len(all_st_set_list):
            if debug: print(f"\n\
==========================================================\n\
                        Step: {i}\n\
==========================================================")
            current_st_set = all_st_set_list[i]
            if debug: print(f"current_st_set: {current_st_set}")

            for s in self.symbols:
                if debug: print(f"\n=========\nsymbol: {s}\n=========")
                goal_st_set = self.symbol_transitions(current_st_set, s)
                if debug: print(f"goal_st_set: {goal_st_set}")

                new_goal_st = "Empty"
                if goal_st_set not in all_st_set_list:
                    if debug: print(f"goal_st_set not in all_st_set_list")
                    if len(goal_st_set) > 0:
                        new_goal_st = rp._new_state()
                        if debug: print(f"new_goal_st: {new_goal_st}")
                    new_st_list.append(new_goal_st)
                    if debug: print(f"new_st_list: {new_st_list}")
                    all_st_set_list.append(goal_st_set)
                    if debug: print(f"all_st_set_list: {all_st_set_list}")
                
                elif len(goal_st_set) > 0:
                    if debug: print(f"goal_st_set in all_st_set_list")
                    j = all_st_set_list.index(goal_st_set)
                    new_goal_st = new_st_list[j]
                    if debug: print(f"new_goal_st: {new_goal_st}")
                if debug: print(f"A.add_transition: {new_st_list[i]} -{s}-> {new_goal_st}")
                A.add_transition(new_st_list[i], s, new_goal_st)

                if goal_st_set.intersection(self.final_states) != set():
                    if debug: print(f"goal_st_set.intersection(self.final_states) != set()")
                    new_final_states.add(new_goal_st)
                    if debug: print(f"new_final_states: {new_final_states}")
            i += 1

        A.__update_final_states__(new_final_states)

        if debug: print(f"\n\
==========================================================\n\
                    Final Automaton\n\
==========================================================")  

        if debug: print(A)
        
        return A

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
    


    def __update_final_states__(self, states):
        """
        Método privado para actualizar los estados finales.
        """
        self.final_states = states

    def __str__(self):
        s = "Automaton:\n"
        s += f"  Symbols: {', '.join(str(s) for s in self.symbols)}\n"
        s += f"  States: {', '.join(self.states)}\n"
        s += f"  Initial state: {self.initial_state}\n"
        s += f"  Final states: {', '.join(self.final_states)}\n"
        s += "  Transitions:\n"
        for state_ini in self.transitions:
            for symbol in self.transitions[state_ini]:
                for state_fin in self.transitions[state_ini][symbol]:
                    sym = symbol if symbol is not None else "λ"
                    s += f"    {state_ini} -{sym}-> {state_fin}\n"

        return s