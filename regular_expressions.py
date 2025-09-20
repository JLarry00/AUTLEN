"""
Esta es la expresion regular para el ejercicio 0, que se facilita
a modo de ejemplo:
"""
RE0 = "[ab]*a"
minus = "[a-z]*"
mayus = "[A-Z]*"
num = "[0-9]*"
num1 = "[1-9][0-9]*"

mes_grande = "((0[1-9])|(1[0-9])|(2[0-9])|(3[0-1]))[/](01|03|05|07|08|10|12)"
mes_peq = "((0[1-9])|(1[0-9])|(2[0-9])|30)[/](04|06|09|11)"
feb = "((0[1-9])|(1[0-9])|(2[0-8]))[/]02"
dia_mes = "(" + mes_grande + "|" + mes_peq + "|" + feb + ")"

oct = "(([0-9])|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5]))"

"""
Completa a continuacion las expresiones regulares para los
ejercicios 1-6:
"""
RE1 = "0*|(0*10*10*)*"
RE2 = "0?(10)*1?"
RE3 = "[+-]?(([1-9][0-9]*)|0)([.][0-9]+)?"
RE4 = minus + "[.]" + minus + "@" + "(estudiante[.])?" + "uam[.]es"
RE5 = dia_mes + "[/]([0-9][0-9][0-9][0-9])"
RE6 = oct + "[.]" + oct + "[.]" + oct + "[.]" + oct

"""
Recuerda que puedes usar el fichero test_p0.py para probar tus
expresiones regulares.
"""
