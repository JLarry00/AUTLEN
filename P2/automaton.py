"""
Módulo para la implementación de autómatas finitos.

Este módulo proporciona una clase para representar y manipular autómatas finitos
deterministas (AFD) y no deterministas (AFN), incluyendo autómatas con transiciones
lambda (ε-transiciones).

Jose-Ignacio Fernández de la Puente Perez y Juan Larrondo Fernández de Córdoba
Última modificación: 7/nov/2025
"""

from graphviz import Digraph
from queue import Queue as q

"""
Podéis implementar cualquier función auxiliar que consideréis necesaria
"""


class FiniteAutomaton:
    """
    Clase que representa un autómata finito (determinista o no determinista).
    
    Attributes:
        initial_state (str): Estado inicial del autómata.
        states (list[str]): Lista de todos los estados del autómata.
        symbols (set): Conjunto de símbolos del alfabeto de entrada.
        transitions (dict): Diccionario de transiciones. Estructura:
            {estado_origen: {símbolo: {estado_destino1, estado_destino2, ...}}}
            Para transiciones lambda, el símbolo es None.
        final_states (set[str]): Conjunto de estados finales (de aceptación).
    """
    
    def __init__(self, initial_state, states, symbols, transitions, final_states):
        """
        Inicializa un nuevo autómata finito.
        
        Args:
            initial_state (str): Estado inicial del autómata.
            states (list[str]): Lista de todos los estados del autómata.
            symbols (set): Conjunto de símbolos del alfabeto de entrada.
            transitions (dict): Diccionario de transiciones. Estructura:
                {estado_origen: {símbolo: {estado_destino1, estado_destino2, ...}}}
                Para transiciones lambda (ε), el símbolo debe ser None.
            final_states (set[str]): Conjunto de estados finales (de aceptación).
        """
        self.initial_state = initial_state
        self.states = states
        self.symbols = symbols
        self.transitions = transitions  # Ya viene como dicc de diccs
        self.final_states = final_states
        
    def add_transition(self, start_state, symbol, end_state):
        """
        Agrega una transición al autómata.
        
        Si la transición ya existe, no se duplica. Permite agregar transiciones
        lambda usando None como símbolo.
        
        Args:
            start_state (str): Estado de origen de la transición.
            symbol: Símbolo que activa la transición. Use None para transiciones lambda (ε).
            end_state (str): Estado de destino de la transición.
        
        Returns:
            bool: True si la transición se agregó correctamente o ya existía,
                  False si alguno de los parámetros no es válido.
        """
        # Validación de parámetros
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

    def accepts(self, cadena):
        """
        Determina si el autómata acepta una cadena de entrada.
        
        Simula la ejecución del autómata sobre la cadena, considerando
        transiciones lambda y no determinismo. La cadena es aceptada si
        después de procesarla completamente, al menos uno de los estados
        actuales es un estado final.

        Asumimos que la cadena no contiene el simbolo lambda, por lo que 
        todo simbolo que no sea valido se devuelve False.
        
        Args:
            cadena (str): Cadena de entrada a evaluar.
        
        Returns:
            bool: True si la cadena es aceptada por el autómata, False en caso contrario.
                 También retorna False si la cadena contiene símbolos no pertenecientes
                 al alfabeto del autómata.
        """
        current_states = self.lambda_clausure({self.initial_state})
        i = 0

        while i < len(cadena):
            symbol = cadena[i]
            i += 1

            if symbol not in self.symbols:
                return False # Si el simbolo no es valido, se devuelve False
            
            next_states = set()
            for state in current_states:
                if state not in self.transitions: continue
                if symbol not in self.transitions[state]: continue
                next_states.update(self.transitions[state][symbol])

            current_states = self.lambda_clausure(next_states)
        
        return current_states.intersection(self.final_states) != set()

    def to_deterministic(self):
        """
        Convierte el autómata a su versión determinista equivalente (AFD).
        
        Implementa el algoritmo de construcción de subconjuntos para convertir
        un autómata finito no determinista (AFN) con transiciones lambda en un
        autómata finito determinista (AFD) equivalente. Cada estado del AFD
        representa un conjunto de estados del AFN original.
        
        Returns:
            FiniteAutomaton: Nuevo autómata finito determinista equivalente al original.
                            Los estados del nuevo autómata son representaciones en
                            cadena de los conjuntos de estados del autómata original.
        
        Note:
            Si el autómata original ya es determinista, el resultado será equivalente
            pero con una representación diferente de los estados.
        """
        init_st_set = self.lambda_clausure({self.initial_state})
        all_st_set_list = [init_st_set]
        new_init_st = str(init_st_set)
        new_st_list = [new_init_st]
        new_final_states = set()
        if init_st_set.intersection(self.final_states) != set():
            new_final_states.add(new_init_st)

        A = FiniteAutomaton(new_init_st, new_st_list, self.symbols, {}, set())

        i = 0
        while i < len(all_st_set_list):
            current_st_set = all_st_set_list[i]

            for s in self.symbols:
                goal_st_set = self.symbol_transitions(current_st_set, s)

                new_goal_st = "Empty"
                if goal_st_set not in all_st_set_list:
                    if len(goal_st_set) > 0:
                        new_goal_st = str(goal_st_set)
                    new_st_list.append(new_goal_st)
                    all_st_set_list.append(goal_st_set)
                
                elif len(goal_st_set) > 0:
                    j = all_st_set_list.index(goal_st_set)
                    new_goal_st = new_st_list[j]
                A.add_transition(new_st_list[i], s, new_goal_st)

                if goal_st_set.intersection(self.final_states) != set():
                    new_final_states.add(new_goal_st)
            i += 1

        A.final_states = new_final_states

        return A

    def to_minimized(self):
        """
        Minimiza el autómata eliminando estados equivalentes.
        
        Implementa el algoritmo de minimización de autómatas finitos deterministas
        mediante el método de partición-refinamiento. Primero elimina estados
        inalcanzables mediante BFS, luego agrupa estados equivalentes en clases
        de equivalencia iterativamente hasta que no se puedan refinar más.
        
        Returns:
            FiniteAutomaton: Nuevo autómata finito minimizado equivalente al original.
                            El autómata resultante tiene el menor número posible de
                            estados manteniendo el mismo lenguaje reconocido.
        
        Note:
            El autómata debe ser determinista para que la minimización sea correcta.
            Si el autómata no es determinista, primero debe aplicarse to_deterministic().
        """
        # BFS
        reachable_st, transitions = self.automaton_bfs()
        NF_states = set(reachable_st) - self.final_states

        # Iteraciones
        current_classes = {st: 0 if st in NF_states else 1 for st in reachable_st}
        old_classes = {}

        flag = True
        k = 1
        while flag:
            flag = False
            old_classes = current_classes
            current_classes = {}
            classes_map = {}

            i = 0
            class_number = 0
            for st1 in reachable_st:
                if st1 not in current_classes.keys():
                    if st1 == list(reachable_st)[0]:
                        current_classes[st1] = 0
                        classes_map[0] = {st1}
                    else:
                        class_number += 1
                        current_classes[st1] = class_number
                        classes_map[class_number] = {st1}
                
                for st2 in list(reachable_st)[i+1:]:
                    same_class = False
                    if (st2 not in current_classes.keys()) and (old_classes[st2] == old_classes[st1]):
                        same_class = True
                        for symbol in transitions[st2]:
                            stf1 = list(transitions[st1][symbol])[0]
                            stf2 = list(transitions[st2][symbol])[0]
                            if old_classes[stf1] != old_classes[stf2]:
                                same_class = False
                                break
                    if same_class:
                        current_classes[st2] = current_classes[st1]
                        classes_map[class_number].add(st2)
                i += 1
                if i > len(reachable_st):
                    break
            if current_classes != old_classes:
                flag = True
            k += 1

        # Autómata Minimizado
        new_states = []
        for st in classes_map.values():
            new_states.append(str(st))

        if len(self.final_states) > 0:
            final_class = current_classes[list(self.final_states)[0]]
            new_final_states = {str(classes_map[final_class])}
        else:
            new_final_states = set()

        initial_class = current_classes[self.initial_state]
        new_initial_state = str(classes_map[initial_class])

        A = FiniteAutomaton(new_initial_state, new_states, self.symbols, {}, new_final_states)
        for state in reachable_st:
            j = current_classes[state]
            current_st = str(classes_map[j])
            for symbol in transitions[state]:
                for state_fin in transitions[state][symbol]:
                    i = current_classes[state_fin]
                    A.add_transition(current_st, symbol, str(classes_map[i]))

        return A
        
    def draw(self, path="./images/", filename="automata.png", view=False):
        """
        Genera una representación visual del autómata usando Graphviz.
        
        Crea un diagrama en formato PNG que muestra los estados, transiciones
        y estados finales del autómata. Los estados finales se representan
        con doble círculo y las transiciones lambda se etiquetan con "λ".
        
        Args:
            path (str, optional): Directorio donde se guardará la imagen.
                                 Por defecto es "./images/".
            filename (str, optional): Nombre del archivo de salida.
                                     Por defecto es "automata.png".
            view (bool, optional): Si es True, abre la imagen automáticamente
                                  después de generarla. Por defecto es False.
        
        Note:
            Requiere que Graphviz esté instalado en el sistema. El directorio
            especificado en path se creará si no existe.
        """
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


    
    def lambda_clausure(self, current_states):
        """
        Calcula el cierre lambda (ε-clausura) de un conjunto de estados.
        
        El cierre lambda incluye todos los estados alcanzables desde los estados
        actuales mediante cero o más transiciones lambda (ε-transiciones).
        
        Args:
            current_states (set[str]): Conjunto de estados desde los que calcular
                                       el cierre lambda.
        
        Returns:
            set[str]: Conjunto de estados actualizado con el cierre lambda.
                     El conjunto incluye los estados originales más todos los
                     estados alcanzables mediante transiciones lambda.
        """
        new_states = set()
        for state in current_states:
            if state in self.transitions:
                transitions = self.transitions[state]
                for s in transitions:
                    if s is None:
                        new_states.update(self.lambda_clausure(transitions[s]))
        current_states.update(new_states)
        return current_states

    def symbol_transitions(self, current_states, symbol):
        """
        Calcula los estados alcanzables desde un conjunto de estados mediante un símbolo.
        
        Primero aplica el cierre lambda a los estados actuales, luego aplica
        las transiciones con el símbolo dado, y finalmente aplica nuevamente
        el cierre lambda a los estados resultantes.
        
        Args:
            current_states (set[str]): Conjunto de estados desde los que partir.
            symbol: Símbolo del alfabeto que activa las transiciones.
        
        Returns:
            set[str]: Conjunto de estados alcanzables después de aplicar el símbolo
                     y el cierre lambda correspondiente.
        """
        new_states = set()
        for state in current_states:
            if state in self.transitions:
                transitions = self.transitions[state]
                for s in transitions:
                    if s is symbol:
                        new_states.update(self.lambda_clausure(transitions[s]))
        
        return new_states

    def automaton_bfs(self) -> tuple[list[str], dict[str, dict[str, set[str]]]]:
        """
        Encuentra todos los estados alcanzables desde el estado inicial mediante BFS.
        
        Realiza un recorrido en anchura (BFS) desde el estado inicial para
        identificar todos los estados que son alcanzables. También construye
        un diccionario con las transiciones de los estados alcanzables.
        
        Returns:
            tuple[list[str], dict[str, dict[str, set[str]]]]: Tupla que contiene:
                - Lista de estados alcanzables desde el estado inicial.
                - Diccionario de transiciones de los estados alcanzables.
                  Estructura: {estado: {símbolo: {estado_destino1, ...}}}
        
        Note:
            Este método es útil para eliminar estados inalcanzables antes de
            aplicar algoritmos de minimización u otras operaciones.
        """
        queue = q()
        queue.put(self.initial_state)
        reachable_states = []
        transition_dict = {}

        while not queue.empty():
            current_state = queue.get()

            if current_state not in reachable_states:
                reachable_states.append(current_state)
                
                transitions = self.transitions[current_state]
                transition_dict[current_state] = transitions

                for symbol in transitions:
                    for state in transitions[symbol]:
                        if state not in reachable_states:
                            queue.put(state)

        return reachable_states, transition_dict



    def __str__(self):
        """
        Retorna una representación en cadena legible del autómata.
        
        Genera una descripción textual completa del autómata incluyendo
        símbolos, estados, estado inicial, estados finales y todas las
        transiciones. Las transiciones lambda se representan con "λ".
        
        Returns:
            str: Cadena de texto que describe el autómata de forma legible.
        
        Example:
            >>> automaton = FiniteAutomaton("q0", ["q0", "q1"], {"a", "b"}, {}, {"q1"})
            >>> print(automaton)
            Automaton:
              Symbols: a, b
              States: q0, q1
              Initial state: q0
              Final states: q1
              Transitions:
        """
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
