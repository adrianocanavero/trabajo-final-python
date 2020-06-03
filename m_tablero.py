import PySimpleGUI as sg
from random import choice
import m_fichas

posicion_jugador = 0 # Es la posición en la que hay que poner la próxima palabra y puntaje de una jugada en concreta
posicion_maquina = 0 # Es la posición en la que hay que poner la próxima palabra y puntaje de una jugada en concreta

def crear_boton(i,j,AN,AL):
    if (m_fichas.triplicar_palabra(i,j)):
        return sg.Button("TPPP", size=(AN, AL), key=(i,j), pad=(0,0))
    if (m_fichas.descuento_tres(i,j)):
        return sg.Button("D3P", size=(AN, AL), key=(i,j), pad=(0,0))
    if (m_fichas.triplicar_letra(i,j)):
        return sg.Button("TPPL", size=(AN, AL), key=(i,j), pad=(0,0))
    if (m_fichas.descuento_uno(i,j)):
        return sg.Button("D1P", size=(AN, AL), key=(i,j), pad=(0,0))    
    if (m_fichas.duplicar_palabra(i,j)):
        return sg.Button("DPPP", size=(AN, AL), key=(i,j), pad=(0,0))
    if (m_fichas.descuento_dos(i,j)):
        return sg.Button("D2P", size=(AN, AL), key=(i,j), pad=(0,0))
    if (m_fichas.duplicar_letra(i,j)):
        return sg.Button("DPPL", size=(AN, AL), key=(i,j), pad=(0,0))
    if (m_fichas.es_inicio(i,j)):
        return sg.Button("INICIO", size=(AN, AL), key=(i,j), pad=(0,0))
    return sg.Button("?", size=(AN, AL), key=(i,j), pad=(0,0))

def actualizar_puntos(a_quien_actualizar,window,puntos_jugador):
    if a_quien_actualizar == 0: # Cero = Jugador / Uno = Máquina
        window[(888,0)].update("PUNTOS\n"+str(puntos_jugador))
    else:
        window[(888,1)].update("PUNTOS\n"+str(puntos_maquina))
        
def calcular_puntos(palabra,lugares_usados,valores_letras):
    lugares_usados.reverse()
    puntos = 0
    posicion = 0
    triplicar_la_palabra = False # Hay que asegurarse que solo se pueda caer en un triplicar puntos por palabra a la vez
    duplicar_la_palabra = False # Hay que asegurarse que solo se pueda caer en un duplicar puntos por palabra a la vez
    for letra in palabra:
        if (m_fichas.triplicar_palabra(lugares_usados[posicion][0],lugares_usados[posicion][1])):
            triplicar_la_palabra = True
        elif (m_fichas.duplicar_palabra(lugares_usados[posicion][0],lugares_usados[posicion][1])):
            duplicar_la_palabra = True
        if (m_fichas.triplicar_letra(lugares_usados[posicion][0],lugares_usados[posicion][1])):
            puntos += valores_letras[letra]*3
        elif (m_fichas.duplicar_letra(lugares_usados[posicion][0],lugares_usados[posicion][1])):
            puntos += valores_letras[letra]*2
        elif (m_fichas.descuento_tres(lugares_usados[posicion][0],lugares_usados[posicion][1])):
            puntos += valores_letras[letra]-3
        elif (m_fichas.descuento_dos(lugares_usados[posicion][0],lugares_usados[posicion][1])):
            puntos += valores_letras[letra]-2
        elif (m_fichas.descuento_uno(lugares_usados[posicion][0],lugares_usados[posicion][1])):
            puntos += valores_letras[letra]-1
        else: puntos += valores_letras[letra]
        posicion += 1
    if triplicar_la_palabra:
        puntos = puntos*3
    if duplicar_la_palabra:
        puntos = puntos*2
    return puntos

def puedo_cambiar(cambiar,event,lugares_usados_temp,lugares_usados_total):
    # Se chequea si no es integer para que no cambie las letras.
    return cambiar and isinstance(event, int) == False and event not in lugares_usados_total

def es_vertical(letras_ingresadas,event,lugares_usados):
    return letras_ingresadas <7 and event == (lugares_usados[0][0]+1, lugares_usados[0][1])

def es_horizontal(letras_ingresadas,event,lugares_usados):
    return letras_ingresadas<7 and event == (lugares_usados[0][0], lugares_usados[0][1]+1) 
    
def es_letra_atril(event):
    return isinstance(event, int) #Como ahora la key es un integer, si es integer, significa que agarro del atril.

def quitar_letras(lugares_usados,backup_text,window):
    i = 0
    for tupla in lugares_usados:
        window[tupla].update(backup_text[i])
        i+=1

def agregar_letra(lugares_usados_total,backup_text,event,escribir,lugares_usados_temp,palabra,boton_de_la_letra,window,pos_atril_usadas):
    backup_text.insert(0,window.Element(event).GetText()) # guardo texto que habia en el boton  
    window[event].update(escribir) #event = posición del botón tocado (dado por key=(i,j)), si agarro del atril es una letra.

    lugares_usados_total.append(event)
    lugares_usados_temp.insert(0,event) # Agrega elementos a lista[0] corriendo los demas. ultimo elem = pos 0 siempre.
    palabra.append(escribir)
    pos_atril_usadas.append(boton_de_la_letra)

def ingreso_palabra(letras_ingresadas,event):
    if letras_ingresadas>= 2:
        if letras_ingresadas == 7 or event == 'Ingresar Palabra!':
            return True
        else: return False
    else:
        return False

def devolver_letras_atril(letras_usadas,pos_atril_usadas,window):
    i = 0
    for letra in letras_usadas:
        window[pos_atril_usadas[i]].update(letra)
        i+=1

def dar_nuevas_letras(Letras,pos_atril_usadas,window):
    for i in pos_atril_usadas:
        window[i].update(tomar_y_borrar(Letras))

def tomar_y_borrar(Letras):
    letra_retornada = choice(Letras)
    Letras.remove(letra_retornada)
    return letra_retornada
    
def palabras_por_turno_pantalla(jug_o_maq,clave):
    return sg.Button(size=(8, 2), key=(jug_o_maq,clave), pad=(0,0),visible=False)
    

def agregar_pal_y_pun_a_pantalla(palabra_en_string,jug_o_maq,puntos,window):
    if jug_o_maq == 0: 
        global posicion_jugador
        window[444,posicion_jugador].update(palabra_en_string+"\n"+str(puntos),visible=True) 
        posicion_jugador += 1 
    else:
        global posicion_maquina
        window[445,posicion_maquina].update(palabra_en_string+"\n"+str(puntos),visible=True)
        posicion_maquina += 1
