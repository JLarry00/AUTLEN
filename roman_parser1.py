import ply.yacc as yacc
from src.roman_lexer import tokens

def p_roman(p):
    'roman : hundreds tens units'
    h, t, u = p[1], p[2], p[3]
    ok = h['valid'] and t['valid'] and u['valid']
    if ok:
        p[0] = {"val": h["val"] * 100 + t["val"] * 10 + u["val"], "valid": True}
    else:
        p[0] = {"val": -1, "valid": False}

def p_hundreds(p):
    """hundreds : low_hundreds
                | C D
                | D low_hundreds
                | C M"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[1] == 'C' and p[2] == 'D':
            p[0] = {"val": 4, "valid": True}
        elif p[1] == 'C' and p[2] == 'M':
            p[0] = {"val": 9, "valid": True}
    elif len(p) == 3 and p[1] == 'D':
        low = p[2]
        p[0] = {"val": 5 + low["val"], "valid": low["valid"]}

def p_hundreds_D(p):
    "hundreds : D low_hundreds"
    low = p[2]
    p[0] = {"val": 5 + low["val"], "valid": low["valid"]}

def p_low_hundreds(p):
    """low_hundreds : low_hundreds C
                    | lambda"""
    if len(p) == 3:
        prev = p[1]
        count = prev["val"] + 1
        p[0] = {"val": count, "valid": prev["valid"] and count <= 3}
    else:
        p[0] = {"val": 0, "valid": True}

def p_tens(p):
    """tens : low_tens
            | X L
            | L low_tens
            | X C"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[1] == 'X' and p[2] == 'L':
            p[0] = {"val": 4, "valid": True}
        elif p[1] == 'X' and p[2] == 'C':
            p[0] = {"val": 9, "valid": True}

def p_tens_L(p):
    "tens : L low_tens"
    low = p[2]
    p[0] = {"val": 5 + low["val"], "valid": low["valid"]}

def p_low_tens(p):
    """low_tens : low_tens X
                | lambda"""
    if len(p) == 3:
        prev = p[1]
        count = prev["val"] + 1
        p[0] = {"val": count, "valid": prev["valid"] and count <= 3}
    else:
        p[0] = {"val": 0, "valid": True}

def p_units(p):
    """units : low_units
             | I V
             | V low_units
             | I X"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[1] == 'I' and p[2] == 'V':
            p[0] = {"val": 4, "valid": True}
        elif p[1] == 'I' and p[2] == 'X':
            p[0] = {"val": 9, "valid": True}

def p_units_V(p):
    "units : V low_units"
    low = p[2]
    p[0] = {"val": 5 + low["val"], "valid": low["valid"]}

def p_low_units(p):
    """low_units : low_units I
                 | lambda"""
    if len(p) == 3:
        prev = p[1]
        count = prev["val"] + 1
        p[0] = {"val": count, "valid": prev["valid"] and count <= 3}
    else:
        p[0] = {"val": 0, "valid": True}

def p_lambda(p):
    'lambda :'
    p[0] = {"val": 0, "valid": True}

def p_error(p):
    return None

parser = yacc.yacc(start='roman')