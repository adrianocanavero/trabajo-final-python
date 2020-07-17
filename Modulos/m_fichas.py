# i = fila y j = columna

bolsa_de_letras = [['A']*11,['B']*3,['C']*4,['D']*4,['E']*11,['F']*2,['G']*2,['H']*2,['I']*6,['J']*2,['K']*2,['L']*4,['M']*3,['N']*5,
                ['Ñ']*2,['O']*8,['P']*2,['Q']*2,['R']*4,['S']*7,['T']*4,['U']*6,['V']*2,['W']*2,'X',['Y']*2,'Z']

valores_letras = {
                    "A": 1, "E": 1, "O": 1, "S": 1, "I": 1, "U": 1, "N": 1, "L": 1, "R":1, "T":1,
                    "C":2, "D":2, "G":2,
                    "M":3, "B":3, "P": 3,
                    "F":4, "V":4, "Y":4, 
                    "J":6, "H":5,
                    "K":8, "Ñ":8, "Q":8, "W": 8, "X": 8,
                    "Z":10
                }

def triplicar_palabra(i,j,nivel):

    """Verifica si el casillero es de triplicar el puntaje de la palabra"""

    if nivel == "facil":
        if ((i == 0 and j == 0) or (i == 0 and j == 14) or (i == 14 and j == 0) or (i == 14 and j == 14)
        or (i == 1 and j == 1) or (i == 1 and j == 13) or (i == 13 and j == 1) or (i == 13 and j == 13)
        or (i == 2 and j == 2) or (i == 2 and j == 12) or (i == 12 and j == 2) or (i == 12 and j == 12)):
            return True
    elif nivel == "medio":
        if (i == 0 and j == 0) or (i == 0 and j == 14) or (i == 14 and j == 0) or (i == 14 and j == 14):
            return True
    elif nivel == "dificil":
        if (i == 1 and j == 1) or (i == 1 and j == 13) or (i == 13 and j == 1) or (i == 13 and j == 13):
            return True
    else: return False

def descuento_tres(i,j,nivel):

    """Verifica si el casillero es de descontar tres puntos"""

    if nivel == "facil":
        if (i == 6 and j == 6) or (i == 6 and j == 8) or (i == 8 and j == 6) or (i == 8 and j == 8):
            return True
    elif nivel == "medio":
        if (i == 0 and j == 7) or (i == 14 and j == 7) or (i == 7 and j == 0) or (i == 7 and j == 14):
            return True
    elif nivel == "dificil":
        if (i == 10 and j == 1) or (i == 4 and j == 1) or (i == 1 and j == 4) or (i == 13 and j == 4) or (i == 1 and j == 10) or (i == 4 and j == 13) or (i == 13 and j == 10) or (i == 10 and j == 13):
            return True
    else: return False

def triplicar_letra(i,j,nivel):

    """Verifica si el casillero es de triplicar el puntaje de la letra"""

    if nivel == "facil":
        if (i == 5 and j == 2) or (i == 2 and j == 5) or (i == 2 and j == 9) or (i == 5 and j == 12) or (i == 9 and j == 2) or (i == 12 and j == 5) or (i == 9 and j == 12) or (i == 12 and j == 9):
            return True
    elif nivel == "medio":
        if (i == 7 and j == 4) or (i == 7 and j == 10) or (i == 4 and j == 7) or (i == 10 and j == 7):
            return True
    elif nivel == "dificil":
        if (i == 7 and j == 2) or (i == 7 and j == 12) or (i == 2 and j == 7) or (i == 12 and j == 7):
            return True
    else: return False

def descuento_uno(i,j,nivel):

    """Verifica si el casillero es de descontar un punto"""

    if nivel == "facil":
        if (i == 1 and j == 7) or (i == 7 and j == 1) or (i == 7 and j == 13) or (i == 13 and j == 7):
            return True
    elif nivel == "medio":
        if (i == 3 and j == 4) or (i == 4 and j == 3) or (i == 10 and j == 3) or (i == 11 and j == 4) or (i == 3 and j == 10) or (i == 4 and j == 11) or (i == 10 and j == 11) or (i == 11 and j == 10):
            return True
    elif nivel == "dificil":
        if ((i == 3 and j == 5) or (i == 3 and j == 6) or (i == 3 and j == 8) or (i == 3 and j == 9)
        or (i == 5 and j == 3) or (i == 6 and j == 3) or (i == 8 and j == 3) or (i == 9 and j == 3)
        or (i == 11 and j == 5) or (i == 11 and j == 6) or (i == 11 and j == 8) or (i == 11 and j == 9)
        or (i == 5 and j == 11) or (i == 6 and j == 11) or (i == 8 and j == 11) or (i == 9 and j == 11)):
            return True
    else: return False

def duplicar_palabra(i,j,nivel):

    """Verifica si el casillero es de duplicar el puntaje de la palabra"""

    if nivel == "facil":
        if ((i == 3 and j == 3) or (i == 3 and j == 11) or (i == 9 and j == 5) or (i == 9 and j == 9)
        or (i == 4 and j == 4) or (i == 4 and j == 10) or (i == 10 and j == 4) or (i == 10 and j == 10)
        or (i == 5 and j == 5) or (i == 5 and j == 9) or (i == 11 and j == 3) or (i == 11 and j == 11)):
            return True
    elif nivel == "medio":
        if (i == 1 and j == 1) or (i == 1 and j == 13) or (i == 13 and j == 1) or (i == 13 and j == 13):
            return True
    elif nivel == "dificil":
        if (i == 3 and j == 3) or (i == 11 and j == 11) or (i == 3 and j == 11) or (i == 11 and j == 3):
            return True
    else: return False

def descuento_dos(i,j,nivel):

    """Verifica si el casillero es de descontar dos puntos"""

    if nivel == "facil":
        if (i == 0 and j == 7) or (i == 14 and j == 7) or (i == 7 and j == 0) or (i == 7 and j == 14):
            return True
    elif nivel == "medio":
        if (i == 1 and j == 7) or (i == 7 and j == 1) or (i == 7 and j == 13) or (i == 13 and j == 7):
            return True
    elif nivel == "dificil":
        if ((i == 4 and j == 7) or (i == 5 and j == 8) or (i == 6 and j == 9) or (i == 7 and j == 10)
        or (i == 8 and j == 9) or (i == 9 and j == 8) or (i == 10 and j == 7) or (i == 9 and j == 6)
        or (i == 8 and j == 5) or (i == 7 and j == 4) or (i == 6 and j == 5) or (i == 5 and j == 6)):
            return True
    else: return False

def duplicar_letra(i,j,nivel):

    """Verifica si el casillero es de duplicar el puntaje de la letra"""

    if nivel == "facil":
        if (i == 1 and j == 4) or (i == 4 and j == 1) or (i == 1 and j == 10) or (i == 4 and j == 13) or (i == 10 and j == 1) or (i == 13 and j == 4) or (i == 13 and j == 10) or (i == 10 and j == 13):
            return True
    elif nivel == "medio":
        if (i == 2 and j == 2) or (i == 2 and j == 12) or (i == 12 and j == 2) or (i == 12 and j == 12):
            return True
    elif nivel == "dificil":
        if (i == 0 and j == 7) or (i == 14 and j == 7) or (i == 7 and j == 0) or (i == 7 and j == 14):
            return True
    else: return False

def es_inicio(i,j):

    """Verifica si el casillero es el de inicio"""
    
    if (i == 7 and j == 7):
        return True
    else: return False
