# Práctica 2: Autómatas Finitos y Expresiones Regulares

## Descripción General

Este proyecto implementa un sistema completo para trabajar con autómatas finitos (deterministas y no deterministas) y su relación con expresiones regulares. La práctica incluye la construcción de autómatas a partir de expresiones regulares, la conversión de autómatas no deterministas a deterministas, y la minimización de autómatas deterministas.

## Archivos Principales

### `automaton.py`

Implementa la clase `FiniteAutomaton` que representa un autómata finito con las siguientes funcionalidades:

#### Funcionalidades Principales

1. **Representación de Autómatas**
   - Soporte para autómatas finitos deterministas (AFD) y no deterministas (AFN)
   - Soporte para transiciones lambda (ε-transiciones)
   - Estructura de datos: estados, símbolos, transiciones y estados finales

2. **Operaciones Básicas**
   - `add_transition()`: Agrega transiciones al autómata
   - `accepts()`: Determina si el autómata acepta una cadena de entrada

3. **Transformaciones de Autómatas**
   - `to_deterministic()`: Convierte un AFN con transiciones lambda a un AFD equivalente usando el algoritmo de construcción de subconjuntos
   - `to_minimized()`: Minimiza un autómata determinista eliminando estados equivalentes mediante el algoritmo de partición-refinamiento

4. **Utilidades**
   - `draw()`: Genera una representación visual del autómata usando Graphviz
   - `automaton_bfs()`: Encuentra todos los estados alcanzables desde el estado inicial mediante BFS
   - `lambda_clausure()`: Calcula el cierre lambda (ε-clausura) de un conjunto de estados
   - `symbol_transitions()`: Calcula los estados alcanzables mediante un símbolo
   - `__str__()`: Representación textual legible del autómata

### `re_parser.py`

Implementa el parser de expresiones regulares que construye autómatas finitos a partir de expresiones regulares.

#### Funcionalidades Principales

1. **Conversión de Notación**
   - `_re_to_rpn()`: Convierte expresiones regulares en notación infija a notación polaca inversa (RPN)
   - Maneja operadores: concatenación (`.`), unión (`+`), estrella de Kleene (`*`), y paréntesis

2. **Construcción de Autómatas**
   - `_create_automaton_symbol()`: Crea un autómata que acepta un único símbolo
   - `_create_automaton_lambda()`: Crea un autómata que acepta la cadena vacía (λ)
   - `_create_automaton_empty()`: Crea un autómata que acepta el lenguaje vacío
   - `_create_automaton_concat()`: Construye el autómata para la concatenación de dos autómatas
   - `_create_automaton_union()`: Construye el autómata para la unión de dos autómatas
   - `_create_automaton_star()`: Construye el autómata para la estrella de Kleene

3. **Método Principal**
   - `create_automaton()`: Construye un autómata finito a partir de una expresión regular

#### Sintaxis de Expresiones Regulares

- **Símbolos**: Cualquier carácter (excepto operadores especiales)
- **Concatenación**: `.` (punto)
- **Unión**: `+` (más)
- **Estrella de Kleene**: `*` (asterisco)
- **Cadena vacía**: `λ`
- **Paréntesis**: `()` para agrupar expresiones

**Ejemplos:**
- `"a.b"`: Concatenación (acepta "ab")
- `"a+b"`: Unión (acepta "a" o "b")
- `"a*"`: Estrella de Kleene (acepta "", "a", "aa", "aaa", ...)
- `"(a+b)*"`: Cualquier secuencia de 'a' y 'b' (incluyendo la cadena vacía)
- `"H.e.l.l.o"`: Concatenación de varios símbolos (acepta "Hello")

## Estructura del Proyecto

```
AUTLEN/
├── automaton.py          # Implementación de autómatas finitos
├── re_parser.py          # Parser de expresiones regulares
├── utils.py              # Utilidades para lectura/escritura de autómatas
├── test_to_deterministic.py  # Tests para conversión a determinista
├── test_minimization.py      # Tests para minimización
├── test_re_parser.py         # Tests para el parser de expresiones regulares
├── test_evaluator.py         # Tests para evaluación de cadenas
└── images/                   # Imágenes generadas por Graphviz
```

## Tests

El proyecto incluye varios archivos de test que verifican la correcta implementación.
Se han modificado los tests para ampliar las pruebas que se realizan:

- **test_evaluator.py**: Prueba la aceptación de cadenas
- **test_re_parser.py**: Prueba la construcción de autómatas desde expresiones regulares
- **test_to_deterministic.py**: Prueba la conversión de AFN a AFD
- **test_minimization.py**: Prueba la minimización de autómatas

Para ejecutar los tests:

```bash
python3 test_evaluator.py
python3 test_re_parser.py
python3 test_to_deterministic.py
python3 test_minimization.py
```

## Dependencias

- **Python 3.7+**
- **graphviz**: Para la visualización de autómatas
  ```bash
  pip install graphviz
  ```
  Nota: Instalación según el sistema:
  - Ubuntu/Debian: `sudo apt-get install graphviz`
  - macOS: `brew install graphviz`
  - Windows: Descargar desde [graphviz.org](https://graphviz.org/)

## Autores

Jose-Ignacio Fernández de la Puente Perez y Juan Larrondo Fernández de Córdoba
Última modificación: 7/nov/2025

