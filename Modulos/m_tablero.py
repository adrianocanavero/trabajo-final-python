import PySimpleGUI as sg
from random import choice
import Modulos.m_fichas as m_fichas

posicion_jugador = 0 # Es la posición en la que hay que poner la próxima palabra y puntaje de una jugada en concreta
posicion_maquina = 0 # Es la posición en la que hay que poner la próxima palabra y puntaje de una jugada en concreta
cant_letras = 7 # Es más fácil cambiar la cantidad de letras a usar si existe esta variable, porque se modifica un solo número

def crear_boton(i,j,AN,AL,nivel):

    """Dependiendo del valor de (i,j) en la iteración que crea el tablero, 
        devuelve el boton específico de esas coordenadas"""

    if (m_fichas.triplicar_palabra(i,j,nivel)):
        return sg.Button("TPPP", size=(AN, AL), key=(i,j), pad=(0,0), button_color=('white', 'dark red'))
    if (m_fichas.descuento_tres(i,j,nivel)):
        return sg.Button("D3P", size=(AN, AL), key=(i,j), pad=(0,0), button_color=('white', 'indigo'))
    if (m_fichas.triplicar_letra(i,j,nivel)):
        return sg.Button("TPPL", size=(AN, AL), key=(i,j), pad=(0,0), button_color=('white', '#533407'))
    if (m_fichas.descuento_uno(i,j,nivel)):
        return sg.Button("D1P", size=(AN, AL), key=(i,j), pad=(0,0), button_color=('white', 'dark blue'))    
    if (m_fichas.duplicar_palabra(i,j,nivel)):
        return sg.Button("DPPP", size=(AN, AL), key=(i,j), pad=(0,0), button_color=('white', '#08927d'))
    if (m_fichas.descuento_dos(i,j,nivel)):
        return sg.Button("D2P", size=(AN, AL), key=(i,j), pad=(0,0), button_color=('white', 'dark orange'))
    if (m_fichas.duplicar_letra(i,j,nivel)):
        return sg.Button("DPPL", size=(AN, AL), key=(i,j), pad=(0,0), button_color=('white', 'dark green'))
    if (m_fichas.es_inicio(i,j)):
        return sg.Button("INICIO", size=(AN, AL), key=(i,j), pad=(0,0), button_color=('white', 'grey'))
    return sg.Button("?", size=(AN, AL), key=(i,j), pad=(0,0))

def actualizar_puntos(a_quien_actualizar,window,puntos):

    """Actualiza el recuadro de puntos segun el jugador que se le indique"""

    if a_quien_actualizar == 0: # Cero = Jugador / Uno = Máquina
        window[(888,0)].update("PUNTOS\n"+str(puntos))
    else:
        window[(888,1)].update("PUNTOS\n"+str(puntos))
        
def calcular_puntos(palabra,lugares_usados,valores_letras,nivel):

    """Calcula el valor final de la palabra segun los lugares en los que se encuentran
        sus letras y el puntaje de cada letra"""

    lugares_usados.reverse()
    puntos = 0
    posicion = 0
    triplicar_la_palabra = False # Solo se pueda caer en un triplicar puntos por palabra a la vez, por eso puede ser booleano en vez de integer
    duplicar_la_palabra = False # Solo se pueda caer en un duplicar puntos por palabra a la vez, por eso puede ser booleano en vez de integer
    for letra in palabra:
        if (m_fichas.triplicar_palabra(lugares_usados[posicion][0],lugares_usados[posicion][1],nivel)):
            triplicar_la_palabra = True
        elif (m_fichas.duplicar_palabra(lugares_usados[posicion][0],lugares_usados[posicion][1],nivel)):
            duplicar_la_palabra = True
        if (m_fichas.triplicar_letra(lugares_usados[posicion][0],lugares_usados[posicion][1],nivel)):
            puntos += valores_letras[letra]*3
        elif (m_fichas.duplicar_letra(lugares_usados[posicion][0],lugares_usados[posicion][1],nivel)):
            puntos += valores_letras[letra]*2
        elif (m_fichas.descuento_tres(lugares_usados[posicion][0],lugares_usados[posicion][1],nivel)):
            puntos += valores_letras[letra]-3
        elif (m_fichas.descuento_dos(lugares_usados[posicion][0],lugares_usados[posicion][1],nivel)):
            puntos += valores_letras[letra]-2
        elif (m_fichas.descuento_uno(lugares_usados[posicion][0],lugares_usados[posicion][1],nivel)):
            puntos += valores_letras[letra]-1
        else: puntos += valores_letras[letra]
        posicion += 1
    if triplicar_la_palabra:
        puntos = puntos*3
    if duplicar_la_palabra:
        puntos = puntos*2
    return puntos

def puedo_cambiar(cambiar,event,lugares_usados_temp,lugares_usados_total):

    """Verifica que el evento reciente sea un click en el tablero para ingresar una letra"""

    # Se chequea si no es integer para que no cambie las letras.
    return cambiar and isinstance(event, int) == False and event != '__TIMEOUT__' and event not in lugares_usados_total and event != 'Cambiar letras'

def es_vertical(letras_ingresadas,event,lugares_usados):

    """Confirma que el ingreso de la palabra se esta realizando verticalmente."""

    return letras_ingresadas <cant_letras and event == (lugares_usados[0][0]+1, lugares_usados[0][1])

def es_horizontal(letras_ingresadas,event,lugares_usados):

    """Confirma que el ingreso de la palabra se esta realizando horizontalmente"""

    return letras_ingresadas<cant_letras and event == (lugares_usados[0][0], lugares_usados[0][1]+1) 
    
def es_letra_atril(event):

    """Verifica que el evento reciente sea un click sobre el atril del usuario."""

    return isinstance(event, int) # Como ahora la key es un integer, si es integer, significa que agarro del atril.

def quitar_letras(lugares_usados,backup_text,window):

    """Quita las letras del tablero en el caso de que se ingrese una palabra erronea."""

    i = 0
    for tupla in lugares_usados:
        window[tupla].update(backup_text[i])
        i+=1

def agregar_letra(lugares_usados_total,backup_text,event,escribir,save,lugares_usados_temp,palabra,boton_de_la_letra,window,pos_atril_usadas):

    """Agrega una letra al tablero y hace efectivo el update de la ventana.
        Agrega las cordenadas ingresadas a save y actualiza los lugares usados"""

    se_puso_una_letra = True
    if event[0] >= 0 and event[0] <= 14 and event[1] >= 0 and event[1] <= 14: # Se asegura que lugar que se tocó para poner la letra es una posición del tablero
        backup_text.insert(0,window.Element(event).GetText()) # se guarda el texto que habia en el boton  
        window[event].update(escribir) # event = posición del botón tocado (dado por key=(i,j)), si se agarra del atril es una letra.
        save[event] = escribir
        lugares_usados_total.append(event)
        lugares_usados_temp.insert(0,event) # Agrega elementos a lista[0] corriendo los demas. ultimo elem = pos 0 siempre.
        palabra.append(escribir)
        pos_atril_usadas.append(boton_de_la_letra)
        se_puso_una_letra = False
    return se_puso_una_letra

def ingreso_palabra(letras_ingresadas,event):

    """Verifica que las letras ingresadas sean más de dos y 
        que se haya clickeado el boton de ingresar palabra"""

    if letras_ingresadas>= 2:
        if letras_ingresadas == cant_letras or event == (471,471):
            return True
        else: return False
    else:
        return False

def devolver_letras_atril(letras_usadas,pos_atril_usadas,window):

    """Devuelve las letras que se usaron en una palabra incorrecta al atril."""

    i = 0
    for letra in letras_usadas:
        window[pos_atril_usadas[i]].update(letra)
        i+=1

def dar_nuevas_letras(Letras,pos_atril_usadas,window):

    """Llena el atril con la cantidad de letras necesarias"""

    for i in pos_atril_usadas:
        window[i].update(tomar_y_borrar(Letras))

def tomar_y_borrar(Letras):

    """Toma una letra de la lista de letras y la borra de la misma"""

    letra_retornada = choice(Letras)
    Letras.remove(letra_retornada)
    return letra_retornada
    
def palabras_por_turno_pantalla(jug_o_maq,clave):

    """Retorna el boton que muestra las palabras con sus puntajes pero invisible,
        cuando se ingresa una palabra, se hace un update y se visibiliza"""

    return sg.Button(size=(8, 2), key=(jug_o_maq,clave), pad=(0,0), button_color=('white', '#314978'), visible=False)
    

def agregar_pal_y_pun_a_pantalla(palabra_en_string,jug_o_maq,puntos,window,save):

    """Agrega al tablero las palabras ingresadas con sus respectivos puntajes. Las de las izquierda son
        las de la maquina y las de la derecha son del usuario. Tambien se guarda en save este event"""

    if jug_o_maq == 0: 
        global posicion_jugador
        window[444,posicion_jugador].update(palabra_en_string+"\n"+str(puntos),visible=True) 
        save[444,posicion_jugador] = palabra_en_string+"\n"+str(puntos)
        posicion_jugador += 1 
    else:
        global posicion_maquina
        window[445,posicion_maquina].update(palabra_en_string+"\n"+str(puntos),visible=True)
        save[445,posicion_maquina] = palabra_en_string+"\n"+str(puntos)
        posicion_maquina += 1

def cambiar_letras(window,Letras,cant_letras):

    """ El usuario elige las letras que desea cambiar, estas se devuelven a la bolsa de fichas y se le otorgan nuevas
        fichas al atril. Retorna True si hubo un cambio efectivo, si salió de la ventana sin cambiar, retorna False"""

    letras_atril = [] # por si entra a cambiar todas
    for i in range(cant_letras):
       letra = window[i].GetText()
       letras_atril.append(letra)
    
    layout = [[sg.Text('Elegir letras a cambiar', justification= 'center', font = 'Any 12', pad= (207,11))],
        [sg.Button(letras_atril[j], key = j, size=(4, 2), pad=(21.5,0), button_color=('white', '#3d578b')) for j in range(cant_letras)],
        [sg.Button('Cambiar', size = (7,3), pad= (102.5,15), button_color=('white', '#52313a')), sg.Button('Cambiar\ntodas', size= (7,3), pad= (140,15), button_color=('white', '#52313a'))]]
    
    win = sg.Window('Cambiar letras', layout,keep_on_top=True)

    letras_a_cambiar = []
    pos_a_cambiar = []
    ok = False
    
    while True:
        event,values = win.Read()

        if isinstance(event,int) and not event == '---': # si es int, es una letra del atril
            letras_a_cambiar.append(win[event].GetText()) # se toma la lera en esa posicion
            win[event].update('---')  
            pos_a_cambiar.append(event)

        if event == 'Cambiar' and letras_a_cambiar:
            for x in pos_a_cambiar:
                Letras.append(letras_a_cambiar.pop()) # se agrega la letra a cambiar a la bolsa
                window[x].update(tomar_y_borrar(Letras)) # se toma una letra de letras y hace update de window principal.
            ok = True
            break

        if event == 'Cambiar\ntodas':
            for j in range(cant_letras):
                Letras.append(letras_atril.pop()) # se agrega la letra a cambiar a la bolsa
                window[j].update(tomar_y_borrar(Letras))
            ok = True
            break
            
        if event == None:
            break

    win.close()
    return ok
