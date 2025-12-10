import ply.yacc as yacc
from src.roman_lexer import tokens

# Gramática

def p_roman(p):
    'roman : hundreds tens units'
    # Combine attributes from Hundreds, Tens, Units
    hundreds_attrs = p[1]
    tens_attrs = p[2]
    units_attrs = p[3]
    
    # Calculate total value
    total_val = hundreds_attrs['val'] * 100 + tens_attrs['val'] * 10 + units_attrs['val']
    
    # Validate: all sub-components valid
    is_valid = (hundreds_attrs['valid'] and 
                tens_attrs['valid'] and 
                units_attrs['valid'])
    
    if is_valid:
        p[0] = {"val": total_val, "valid": True}
    else:
        p[0] = {"val": -1, "valid": False}


def p_hundreds(p):
    """hundreds : low_hundreds
                | C D
                | D low_hundreds
                | C M"""
    if len(p) == 2:
        # LowHundreds
        p[0] = p[1]
    elif len(p) == 3:
        if p[1] == 'C' and p[2] == 'D':
            # CD = 400
            p[0] = {"val": 4, "valid": True}
        elif p[1] == 'C' and p[2] == 'M':
            # CM = 900
            p[0] = {"val": 9, "valid": True}
        elif p[1] == 'D':
            # D LowHundreds = 500 + (0-300) = 500-800
            low_hundreds_attrs = p[2]
            # Validate: low_hundreds val must be 0-3 (0-3 C's)
            is_valid = low_hundreds_attrs['valid'] and low_hundreds_attrs['val'] <= 3
            p[0] = {
                "val": 5 + low_hundreds_attrs['val'],
                "valid": is_valid
            }


def p_low_hundreds(p):
    """low_hundreds : C low_hundreds
                    | lambda"""
    if len(p) == 3:
        # Recursive case: LowHundreds C
        prev_attrs = p[1]
        count_c = prev_attrs['val'] + 1
        # Validate: count must be <= 3
        is_valid = prev_attrs['valid'] and count_c <= 3
        p[0] = {
            "val": count_c,
            "valid": is_valid
        }
    else:
        # Lambda case
        p[0] = {"val": 0, "valid": True}


def p_tens(p):
    """tens : low_tens
            | X L
            | L low_tens
            | X C"""
    if len(p) == 2:
        # LowTens
        p[0] = p[1]
    elif len(p) == 3:
        if p[1] == 'X' and p[2] == 'L':
            # XL = 40
            p[0] = {"val": 4, "valid": True}
        elif p[1] == 'X' and p[2] == 'C':
            # XC = 90
            p[0] = {"val": 9, "valid": True}
        elif p[1] == 'L':
            # L LowTens = 50 + (0-30) = 50-80
            low_tens_attrs = p[2]
            # Validate: low_tens val must be 0-3 (0-3 X's)
            is_valid = low_tens_attrs['valid'] and low_tens_attrs['val'] <= 3
            p[0] = {
                "val": 5 + low_tens_attrs['val'],
                "valid": is_valid
            }


def p_low_tens(p):
    """low_tens : X low_tens
                | lambda"""
    if len(p) == 3:
        # Recursive case: LowTens X
        prev_attrs = p[1]
        count_x = prev_attrs['val'] + 1
        # Validate: count must be <= 3
        is_valid = prev_attrs['valid'] and count_x <= 3
        p[0] = {
            "val": count_x,
            "valid": is_valid
        }
    else:
        # Lambda case
        p[0] = {"val": 0, "valid": True}


def p_units(p):
    """units : low_units
             | I V
             | V low_units
             | I X"""
    if len(p) == 2:
        # LowUnits
        p[0] = p[1]
    elif len(p) == 3:
        if p[1] == 'I' and p[2] == 'V':
            # IV = 4
            p[0] = {"val": 4, "valid": True}
        elif p[1] == 'I' and p[2] == 'X':
            # IX = 9
            p[0] = {"val": 9, "valid": True}
        elif p[1] == 'V':
            # V LowUnits = 5 + (0-3) = 5-8
            low_units_attrs = p[2]
            # Validate: low_units val must be 0-3 (0-3 I's)
            is_valid = low_units_attrs['valid'] and low_units_attrs['val'] <= 3
            p[0] = {
                "val": 5 + low_units_attrs['val'],
                "valid": is_valid
            }


def p_low_units(p):
    """low_units : I low_units
                 | lambda"""
    if len(p) == 3:
        # Recursive case: LowUnits I
        prev_attrs = p[1]
        count_i = prev_attrs['val'] + 1
        # Validate: count must be <= 3
        is_valid = prev_attrs['valid'] and count_i <= 3
        p[0] = {
            "val": count_i,
            "valid": is_valid
        }
    else:
        # Lambda case
        p[0] = {"val": 0, "valid": True}


# Definir lambda
def p_lambda(p):
    'lambda :'
    p[0] = {"val": 0, "valid": True}

# Manejo de errores sintácticos
def p_error(p):
    # For shift/reduce conflicts, PLY prefers shift
    # When we get an error, it might be because we shifted when we should have reduced
    # We'll let PLY handle recovery automatically
    if p:
        # Return None to signal error, but don't print to avoid noise
        # The parser will try to recover
        return None
    return None

# Construir el parser
parser = yacc.yacc(start='roman')

if __name__ == "__main__":
    while True:
        try:
            s = input("Ingrese un número romano: ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(f"El valor numérico es: {result}")