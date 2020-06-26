import PySimpleGUI as sg

# i = fila y j = columna

valores_letras = {
                    "A": 1, "E": 1, "O": 1, "S": 1, "I": 1, "U": 1, "N": 1, "L": 1, "R":1, "T":1,
                    "C":2, "D":2, "G":2,
                    "M":3, "B":3, "P": 3,
                    "F":4, "V":4, "Y":4, 
                    "J":6, "H":5,
                    "K":8, "Ñ":8, "Q":8, "W": 8, "X": 8,
                    "Z":10
                }

def triplicar_palabra(i,j):

    """Verifica si el casillero es de triplicar"""

    if (i == 0 and j == 0) or (i == 0 and j == 14) or (i == 14 and j == 0) or (i == 14 and j == 14): 
        return True
    else: return False

def descuento_tres(i,j):

    """Verifica si el casillero es de descontar"""

    if (i == 0 and j == 7) or (i == 14 and j == 7) or (i == 7 and j == 0) or (i == 7 and j == 14):
        return True
    else: return False

def triplicar_letra(i,j):

    """Verifica si el casillero es de triplicar el puntaje de la letra"""

    if (i == 7 and j == 4) or (i == 7 and j == 10) or (i == 4 and j == 7) or (i == 10 and j == 7):
        return True
    else: return False

def descuento_uno(i,j):

    """Verifica si el casillero es de descontar uno del puntaje de la letra"""

    if (i == 3 and j == 4) or (i == 4 and j == 3) or (i == 10 and j == 3) or (i == 11 and j == 4) or (i == 3 and j == 10) or (i == 4 and j == 11) or (i == 10 and j == 11) or (i == 11 and j == 10):
        return True
    else: return False

def duplicar_palabra(i,j):

    """Verifica si el casillero es de duplicar el puntaje total de la palabra"""

    if (i == 1 and j == 1) or (i == 1 and j == 13) or (i == 13 and j == 1) or (i == 13 and j == 13):
        return True
    else: return False

def descuento_dos(i,j):

    """Verifica si el casillero es de descontar dos puntos a la letra"""

    if (i == 1 and j == 7) or (i == 7 and j == 1) or (i == 7 and j == 13) or (i == 13 and j == 7):
        return True
    else: return False

def duplicar_letra(i,j):

    """Verifica si el casillero es de duplicar el puntaje de la letra"""

    if (i == 2 and j == 2) or (i == 2 and j == 12) or (i == 12 and j == 2) or (i == 12 and j == 12):
        return True
    else: return False

def es_inicio(i,j):

    """Verifica si el casillero es el de inicio"""
    
    if (i == 7 and j == 7):
        return True
    else: return False
