from m_buscador import buscar_palabra
from itertools import permutations,combinations
from m_tablero import tomar_y_borrar
from m_fichas import valores_letras
from random import choice
from random import randrange

def devolver_palabra(letras_de_maquina):
    print('devuelve primer palabra que encuentra')
    encontre = False
    for i in reversed(range (2, len(letras_de_maquina)+1)): # arranca desde 2
        combinations_list= list(combinations(letras_de_maquina, i))
        for tupla in combinations_list:
            to_string = ''.join(tupla)
            if buscar_palabra(to_string):
                encontre = True
                return to_string
    if not encontre:
        return 'No encontre palabra'

def palabra_maxima(letras_de_maquina,valores_letras):
    print('devuelve maxima palabra')
    max = 0
    sum = 0
    palabra_max = ''
    encontre = False
    for i in range(2, len(letras_de_maquina)+1): 
        combinations_list= list(combinations(letras_de_maquina, i))
        for tupla in combinations_list:
            to_string = ''.join(tupla)
            if buscar_palabra(to_string):
                encontre = True
                for char in to_string:
                    sum += valores_letras[char]
                if sum>max:
                    palabra_max = to_string
                    max = sum
    if encontre: return palabra_max  
    else: return 'No encontre palabra'  
                     
def encontrar_lugar(lugares_usados_total,cantidad):
    
    # SI EL (7,7) ESTÁ LIBRE (O SEA EMPIEZA LA MÁQUINA) LOS LUGARES A USAR VAN A ESTAR VERTICAL U HORIZONTALMENTE DESDE (7,7)
    if (7,7) not in lugares_usados_total:
        lugares_a_usar = []
        direccion = choice(["Vertical", "Horizontal"])
        if direccion == "Vertical":
            for pos in range(7,7+cantidad):
                lugares_a_usar.insert(0,(pos,7))
        else:
            for pos in range(7,7+cantidad):
                lugares_a_usar.insert(0,(7,pos))
    
    # SI (7,7) NO ESTÁ LIBRE SE BUSCA UN LUGAR DISPONIBLE
    else:
        encontre = False
        while not encontre:
            lugares_a_usar = [] # SE RESETEA CON CADA INTENTO
            fila = randrange(15) # SE ELIGE UNA FILA AL AZAR
            columna = randrange(15) # SE ELIGE UNA COLUMNA AL AZAR
            posicion_invalida = False
            cant_usadas = 1
            lugares_a_usar.insert(0,(fila,columna))
            direccion = choice(["Vertical", "Horizontal"]) # SE ELIGE UNA DIRECCIÓN AL AZAR
            
            # MIENTRAS LOS LUGARES QUE SE QUIEREN USAR NO ESTÉN OCUPADOS, NO SE VAYAN DEL TABLERO Y NO SE HAYAN CONSEGUIDO LUGARES PARA TODAS LAS LETRAS
            while ("Lugar ocupado" not in map(lambda coordenadas:coordenadas if (coordenadas not in lugares_usados_total) else "Lugar ocupado",lugares_a_usar)) and (not posicion_invalida) and (cant_usadas < cantidad):
                cant_usadas += 1
                if direccion == "Vertical":
                    fila += 1
                    if fila == 15:
                        posicion_invalida = True
                    lugares_a_usar.insert(0,(fila,columna))
                else:
                    columna += 1
                    if columna == 15:
                        posicion_invalida = True
                    lugares_a_usar.insert(0,(fila,columna))
            
            # SI SE CONSIGUIERON LUGARES PARA TODAS LAS LETRAS TERMINA LA EJECUCIÓN, SINO SE INTENTA DE NUEVO CON OTRAS COORDENADAS
            if ("Lugar ocupado" not in map(lambda coordenadas:coordenadas if (coordenadas not in lugares_usados_total) else "Lugar ocupado",lugares_a_usar)) and (not posicion_invalida):
                encontre = True
    return lugares_a_usar

def cambiar_letras_usadas_por_nuevas(palabra_maquina):
    letras_a_reponer = 0
    for letra in palabra_maquina: # Saca las letras usadas
        letras_a_reponer += 1
        letras_de_maquina.remove(letra)
    for x in range(letras_a_reponer): # Repone las letras faltantes
        letras_de_maquina.append(tomar_y_borrar(Letras))

cant_letras = 7

creando_letras = [['A']*11,['B']*3,['C']*4,['D']*4,['E']*11,['F']*2,['G']*2,['H']*2,['I']*6,['J']*2,['K']*2,['L']*4,['M']*3,['N']*5,
            ['Ñ']*2,['O']*8,['P']*2,['Q']*2,['R']*4,['S']*7,['T']*4,['U']*6,['V']*2,['W']*2,'X',['Y']*2,'Z']

Letras = [elem for sublist in creando_letras for elem in sublist] #hace que creando_letras sea una sola lista.

letras_de_maquina = []

for j in range(cant_letras):
    letras_de_maquina.append(tomar_y_borrar(Letras))

#print(devolver_palabra(letras_de_maquina))

#print(palabra_maxima(letras_de_maquina,valores_letras))

