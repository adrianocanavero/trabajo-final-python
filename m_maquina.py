from m_buscador import buscar_palabra
from itertools import combinations
from m_tablero import tomar_y_borrar
from m_fichas import valores_letras

def devolver_palabra(letras_de_maquina):
    print('devuelve primer palabra que encuentra')
    for i in range (2, len(letras_de_maquina)+1): # arranca desde 2
        combinations_list= list(combinations(letras_de_maquina, i))
        for tupla in combinations_list:
            to_string = ''.join(tupla)
            if buscar_palabra(to_string):
                return to_string
                break

def palabra_maxima(letras_de_maquina,valores_letras):
    print('devuelve maxima palabra')
    max = 0
    sum = 0
    palabra_max = ''
    for i in range (2, len(letras_de_maquina)+1): 
        combinations_list= list(combinations(letras_de_maquina, i))
        for tupla in combinations_list:
            to_string = ''.join(tupla)
            if buscar_palabra(to_string):
                for char in to_string:
                    sum += valores_letras[char]
                if sum>max:
                    palabra_max = to_string
                    max = sum
    return palabra_max    

                     
cant_letras = 7

creando_letras = [['A']*11,['B']*3,['C']*4,['D']*4,['E']*11,['F']*2,['G']*2,['H']*2,['I']*6,['J']*2,['K']*2,['L']*4,['M']*3,['N']*5,
            ['Ñ']*2,['O']*8,['P']*2,['Q']*2,['R']*4,['S']*7,['T']*4,['U']*6,['V']*2,['W']*2,'X',['Y']*2,'Z']

Letras = [elem for sublist in creando_letras for elem in sublist] #hace que creando_letras sea una sola lista.

letras_de_maquina = []

for j in range(cant_letras):
    letras_de_maquina.append(tomar_y_borrar(Letras))

#print(devolver_palabra(letras_de_maquina))

print(palabra_maxima(letras_de_maquina,valores_letras))

