from src.grammar import Grammar
import sys
from io import StringIO

# Definir las gramáticas para roman_parser1 (G1) y roman_parser2 (G2)
# 
# DIFERENCIA CLAVE:
# G1 (roman_parser1): left-recursive  (LowHundreds → LowHundreds C | λ)
# G2 (roman_parser2): right-recursive   (LowHundreds → C LowHundreds | λ)
# 
# Mapeo de símbolos (un carácter por símbolo):
# R = roman
# H = hundreds
# A = low_hundreds
# T = tens
# B = low_tens
# U = units
# O = low_units
# Terminales: C, D, I, L, M, V, X

# Terminales: C, D, I, L, M, V, X
terminals = {'C', 'D', 'I', 'L', 'M', 'V', 'X'}

# No terminales (un carácter cada uno)
non_terminals = {'R', 'H', 'A', 'T', 'B', 'U', 'O'}

# GRAMÁTICA G1 (roman_parser1) - LEFT-RECURSIVE
# R -> H T U
# H -> A | CD | DA | CM
# A -> AC | λ  (LEFT-RECURSIVE: LowHundreds → LowHundreds C | λ)
# T -> B | XL | LB | XC
# B -> BX | λ  (LEFT-RECURSIVE: LowTens → LowTens X | λ)
# U -> O | IV | VO | IX
# O -> OI | λ  (LEFT-RECURSIVE: LowUnits → LowUnits I | λ)
productions_g1 = {
    'R': ['HTU'],  # roman -> hundreds tens units
    'H': ['A', 'CD', 'DA', 'CM'],  # hundreds -> low_hundreds | C D | D low_hundreds | C M
    'A': ['AC', ''],  # low_hundreds -> low_hundreds C | lambda (LEFT-RECURSIVE)
    'T': ['B', 'XL', 'LB', 'XC'],  # tens -> low_tens | X L | L low_tens | X C
    'B': ['BX', ''],  # low_tens -> low_tens X | lambda (LEFT-RECURSIVE)
    'U': ['O', 'IV', 'VO', 'IX'],  # units -> low_units | I V | V low_units | I X
    'O': ['OI', '']  # low_units -> low_units I | lambda (LEFT-RECURSIVE)
}

# GRAMÁTICA G2 (roman_parser2) - RIGHT-RECURSIVE
# R -> H T U
# H -> A | CD | DA | CM
# A -> CA | λ  (RIGHT-RECURSIVE: LowHundreds → C LowHundreds | λ)
# T -> B | XL | LB | XC
# B -> XB | λ  (RIGHT-RECURSIVE: LowTens → X LowTens | λ)
# U -> O | IV | VO | IX
# O -> IO | λ  (RIGHT-RECURSIVE: LowUnits → I LowUnits | λ)
productions_g2 = {
    'R': ['HTU'],  # roman -> hundreds tens units
    'H': ['A', 'CD', 'DA', 'CM'],  # hundreds -> low_hundreds | C D | D low_hundreds | C M
    'A': ['CA', ''],  # low_hundreds -> C low_hundreds | lambda (RIGHT-RECURSIVE)
    'T': ['B', 'XL', 'LB', 'XC'],  # tens -> low_tens | X L | L low_tens | X C
    'B': ['XB', ''],  # low_tens -> X low_tens | lambda (RIGHT-RECURSIVE)
    'U': ['O', 'IV', 'VO', 'IX'],  # units -> low_units | I V | V low_units | I X
    'O': ['IO', '']  # low_units -> I low_units | lambda (RIGHT-RECURSIVE)
}

# Crear las gramáticas
grammar1 = Grammar(terminals, non_terminals, productions_g1, 'R')
grammar2 = Grammar(terminals, non_terminals, productions_g2, 'R')

# Mapeo para mostrar nombres originales
symbol_names = {
    'R': 'roman',
    'H': 'hundreds',
    'A': 'low_hundreds',
    'T': 'tens',
    'B': 'low_tens',
    'U': 'units',
    'O': 'low_units'
}

def get_first_follow_dict(grammar):
    """Calcula y retorna diccionarios con FIRST y FOLLOW para todos los símbolos."""
    symbols_order = ['R', 'H', 'A', 'T', 'B', 'U', 'O']
    first_dict = {}
    follow_dict = {}
    
    for symbol in symbols_order:
        first_set = grammar.compute_first(symbol)
        follow_set = grammar.compute_follow(symbol)
        first_dict[symbol] = first_set
        follow_dict[symbol] = follow_set
    
    return first_dict, follow_dict

def print_first_follow(grammar, grammar_name):
    """Imprime los conjuntos FIRST y FOLLOW para todos los símbolos no terminales."""
    print(f"\n{'='*60}")
    print(f"GRAMÁTICA: {grammar_name}")
    print(f"{'='*60}\n")
    
    # Orden de impresión (usando los símbolos de un carácter)
    symbols_order = ['R', 'H', 'A', 'T', 'B', 'U', 'O']
    
    # Calcular el ancho máximo del nombre del símbolo
    max_name_width = max(len(symbol_names[s]) for s in symbols_order)
    
    print("CONJUNTOS FIRST:")
    print("-" * 60)
    for symbol in symbols_order:
        first_set = grammar.compute_first(symbol)
        # Convertir '' a 'λ' para mejor visualización
        first_display = {s if s != '' else 'λ' for s in first_set}
        symbol_name = symbol_names[symbol]
        # Calcular el ancho necesario para alinear (FIRST( + nombre + ): = 8 + max_name_width)
        prefix_width = 10 + max_name_width
        print(f"FIRST({symbol_name}):{' ' * (prefix_width - len(f'FIRST({symbol_name}):'))}{sorted(first_display)}")
    
    print("\nCONJUNTOS FOLLOW:")
    print("-" * 60)
    for symbol in symbols_order:
        follow_set = grammar.compute_follow(symbol)
        # Convertir '' a 'λ' para mejor visualización (aunque FOLLOW no debería tener λ)
        follow_display = {s if s != '' else 'λ' for s in follow_set}
        symbol_name = symbol_names[symbol]
        # Calcular el ancho necesario para alinear (FOLLOW( + nombre + ): = 9 + max_name_width)
        prefix_width = 10 + max_name_width
        print(f"FOLLOW({symbol_name}):{' ' * (prefix_width - len(f'FOLLOW({symbol_name}):'))}{sorted(follow_display)}")
    
    print()

def print_differences(first1, follow1, first2, follow2):
    """Imprime las diferencias entre los conjuntos FIRST y FOLLOW de ambas gramáticas."""
    symbols_order = ['R', 'H', 'A', 'T', 'B', 'U', 'O']
    
    print("\n" + "="*60)
    print("DIFERENCIAS ENTRE LAS GRAMÁTICAS:")
    print("="*60)
    print("\n1. DIFERENCIAS EN PRODUCCIONES:")
    print("-" * 60)
    print("G1 (roman_parser1): LEFT-RECURSIVE")
    print("  - LowHundreds → LowHundreds C | λ")
    print("  - LowTens → LowTens X | λ")
    print("  - LowUnits → LowUnits I | λ")
    print("G2 (roman_parser2): RIGHT-RECURSIVE")
    print("  - LowHundreds → C LowHundreds | λ")
    print("  - LowTens → X LowTens | λ")
    print("  - LowUnits → I LowUnits | λ")
    
    print("\n2. DIFERENCIAS EN CONJUNTOS FIRST:")
    print("-" * 60)
    first_differences = False
    for symbol in symbols_order:
        first_g1 = first1[symbol]
        first_g2 = first2[symbol]
        if first_g1 != first_g2:
            first_differences = True
            symbol_name = symbol_names[symbol]
            first_g1_display = {s if s != '' else 'λ' for s in first_g1}
            first_g2_display = {s if s != '' else 'λ' for s in first_g2}
            only_g1 = sorted(first_g1_display - first_g2_display)
            only_g2 = sorted(first_g2_display - first_g1_display)
            
            print(f"FIRST({symbol_name:15}):")
            print(f"  G1: {sorted(first_g1_display)}")
            print(f"  G2: {sorted(first_g2_display)}")
            if only_g1:
                print(f"  Solo en G1: {only_g1}")
            if only_g2:
                print(f"  Solo en G2: {only_g2}")
            print()
    
    if not first_differences:
        print("No hay diferencias en los conjuntos FIRST.")
    
    print("\n3. DIFERENCIAS EN CONJUNTOS FOLLOW:")
    print("-" * 60)
    follow_differences = False
    for symbol in symbols_order:
        follow_g1 = follow1[symbol]
        follow_g2 = follow2[symbol]
        if follow_g1 != follow_g2:
            follow_differences = True
            symbol_name = symbol_names[symbol]
            follow_g1_display = {s if s != '' else 'λ' for s in follow_g1}
            follow_g2_display = {s if s != '' else 'λ' for s in follow_g2}
            only_g1 = sorted(follow_g1_display - follow_g2_display)
            only_g2 = sorted(follow_g2_display - follow_g1_display)
            
            print(f"FOLLOW({symbol_name:14}):")
            print(f"  G1: {sorted(follow_g1_display)}")
            print(f"  G2: {sorted(follow_g2_display)}")
            if only_g1:
                print(f"  Solo en G1: {only_g1}")
            if only_g2:
                print(f"  Solo en G2: {only_g2}")
            print()
    
    if not follow_differences:
        print("No hay diferencias en los conjuntos FOLLOW.")

# Capturar la salida en un buffer
output_buffer = StringIO()
original_stdout = sys.stdout

try:
    # Redirigir stdout al buffer
    sys.stdout = output_buffer
    
    # Calcular FIRST y FOLLOW para ambas gramáticas
    first1, follow1 = get_first_follow_dict(grammar1)
    first2, follow2 = get_first_follow_dict(grammar2)
    
    # Imprimir para ambas gramáticas
    print_first_follow(grammar1, "roman_parser1")
    print_first_follow(grammar2, "roman_parser2")
    
    # Imprimir diferencias
    print_differences(first1, follow1, first2, follow2)
    
    # Obtener el contenido del buffer
    output_content = output_buffer.getvalue()
    
finally:
    # Restaurar stdout
    sys.stdout = original_stdout

# Escribir en archivo
output_file = "ej6_p2_output.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(output_content)

# También imprimir en consola
print(output_content)
print(f"\nSalida guardada en: {output_file}")

