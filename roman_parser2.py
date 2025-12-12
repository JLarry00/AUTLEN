import ply.yacc as yacc
from src.roman_lexer import tokens


def p_roman(p):
    "roman : hundreds tens units"
    h, t, u = p[1], p[2], p[3]

    if h["valid"] and t["valid"] and u["valid"]:
        p[0] = {
            "val": h["val"] * 100 + t["val"] * 10 + u["val"],
            "valid": True
        }
    else:
        p[0] = {"val": -1, "valid": False}


def p_hundreds_low(p):
    "hundreds : low_hundreds"
    p[0] = p[1]

def p_hundreds_CD(p):
    "hundreds : C D"
    p[0] = {"val": 4, "valid": True}

def p_hundreds_CM(p):
    "hundreds : C M"
    p[0] = {"val": 9, "valid": True}

def p_hundreds_Dlow(p):
    "hundreds : D low_hundreds"
    low = p[2]
    p[0] = {
        "val": 5 + low["val"],
        "valid": low["valid"]
    }


def p_low_hundreds_rec(p):
    "low_hundreds : C low_hundreds"
    prev = p[2]
    count = prev["val"] + 1
    p[0] = {
        "val": count,
        "valid": prev["valid"] and count <= 3
    }

def p_low_hundreds_lambda(p):
    "low_hundreds : lambda"
    p[0] = {"val": 0, "valid": True}


def p_tens_low(p):
    "tens : low_tens"
    p[0] = p[1]

def p_tens_XL(p):
    "tens : X L"
    p[0] = {"val": 4, "valid": True}

def p_tens_XC(p):
    "tens : X C"
    p[0] = {"val": 9, "valid": True}

def p_tens_Llow(p):
    "tens : L low_tens"
    low = p[2]
    p[0] = {
        "val": 5 + low["val"],
        "valid": low["valid"]
    }


def p_low_tens_rec(p):
    "low_tens : X low_tens"
    prev = p[2]
    count = prev["val"] + 1
    p[0] = {
        "val": count,
        "valid": prev["valid"] and count <= 3
    }

def p_low_tens_lambda(p):
    "low_tens : lambda"
    p[0] = {"val": 0, "valid": True}


def p_units_low(p):
    "units : low_units"
    p[0] = p[1]

def p_units_IV(p):
    "units : I V"
    p[0] = {"val": 4, "valid": True}

def p_units_IX(p):
    "units : I X"
    p[0] = {"val": 9, "valid": True}

def p_units_Vlow(p):
    "units : V low_units"
    low = p[2]
    p[0] = {
        "val": 5 + low["val"],
        "valid": low["valid"]
    }


def p_low_units_rec(p):
    "low_units : I low_units"
    prev = p[2]
    count = prev["val"] + 1
    p[0] = {
        "val": count,
        "valid": prev["valid"] and count <= 3
    }

def p_low_units_lambda(p):
    "low_units : lambda"
    p[0] = {"val": 0, "valid": True}


def p_lambda(p):
    "lambda :"
    p[0] = {"val": 0, "valid": True}


def p_error(p):
    # Entrada inválida → número romano inválido
    raise SyntaxError("Invalid roman numeral")


parser = yacc.yacc(start="roman")


if __name__ == "__main__":
    while True:
        try:
            s = input("Ingrese un número romano: ")
        except EOFError:
            break
        if not s:
            continue
        try:
            result = parser.parse(s)
        except SyntaxError:
            result = {"val": -1, "valid": False}
        print(result)