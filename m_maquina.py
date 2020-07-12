from m_buscador import buscar_palabra
from itertools import combinations,permutations
from m_tablero import tomar_y_borrar
from random import choice
from random import randrange

nivel = 'medio'

def devolver_palabra():

    """Retorna una palabra dada la lista de letras que posee el atril de la maquina, en caso de no encontrar,
        retorna 'No encontre palabra'."""

    #print('devuelve primer palabra que encuentra')
    encontre = False
    for i in reversed(range (2, 7)): # arranca desde 2
        combinations_list= list(combinations(letras_de_maquina, i))
        for tupla in combinations_list:
            to_string = ''.join(tupla)
            if buscar_palabra(to_string,nivel):
                encontre = True
                return to_string
    if not encontre:
        return 'No encontre palabra'

def palabra_maxima(valores_letras):
    """Metodo pensado para implementar en un nivel con mayor dificultad"""

    #print('devuelve maxima palabra')
    max = 0
    sum = 0
    palabra_max = ''
    encontre = False
    for i in range(2, len(letras_de_maquina)+1): 
        combinations_list= list(combinations(letras_de_maquina, i))
        for tupla in combinations_list:
            to_string = ''.join(tupla)
            if buscar_palabra(to_string,nivel):
                encontre = True
                for char in to_string:
                    sum += valores_letras[char]
                if sum>max:
                    palabra_max = to_string
                    max = sum
    if encontre: return palabra_max  
    else: return 'No encontre palabra'  
                     
def encontrar_lugar(lugares_usados_total,cantidad):
    
    """Busca un espacio acorde a la cantidad de letras que tiene la palabra que va a ingresar la AI"""

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

def cambiar_letras_usadas_por_nuevas(palabra_maquina,Letras):

    """Remueve del atril de la maquina las letras que utilizó para formar una palabra y
        le da letras nuevas"""

    letras_a_reponer = 0
    for letra in palabra_maquina: # Saca las letras usadas
        letras_a_reponer += 1
        letras_de_maquina.remove(letra)
    for x in range(letras_a_reponer): # Repone las letras faltantes
        letras_de_maquina.append(tomar_y_borrar(Letras))

def inicializar_letras_maquina(Letras):

    """Da las letras iniciales de la maquina cuando se comienza una nueva partida""" 
    
    for j in range(cant_letras):
        letras_de_maquina.append(tomar_y_borrar(Letras))

cant_letras = 7

letras_de_maquina = []

#print(devolver_palabra(letras_de_maquina))

#print(palabra_maxima(letras_de_maquina,valores_letras))

