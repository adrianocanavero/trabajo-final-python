import PySimpleGUI as sg
from random import choice
import m_buscador
import m_tablero
from m_fichas import valores_letras
from m_fichas import bolsa_de_letras
import m_maquina
import pickle
import time
from m_menu import menu
from m_topten import top_puntajes
from m_configuracion import configurar
import winsound
from m_veredicto import mostrar_puntaje
from m_guardado import guardar,inicializar_variables,abrir_guardado

def main(hay_save=False,tiempo=60,nivel="medio",valores_de_letras=valores_letras,bolsa_letras=bolsa_de_letras):


    """ Funcion main: ejecuta el juego debidamente. Recibe True si el jugador eligio Nueva Partida o False si
        el jugador eligió Cargar Partida"""
    
    
    # Intento abrir archivo. 
    if (hay_save): 
        try:
            save_window,datos_usuario,nivel,bolsa_letras = abrir_guardado()
        except EOFError: ## si no hay save, no tendria porque haber problema
            hay_save = False
        except FileNotFoundError:
            hay_save = False
    m_maquina.nivel = nivel
    #LAYOUT
        
    puntos_jugador = 0
    puntos_maquina = 0
    AN = 4 # Este es el ancho de los botones
    AL = 2 # Este es el alto de los botones
    INICIO = (7,7)
    filas = 15
    cant_letras = 7
    creando_letras = bolsa_letras

    Letras = [elem for sublist in creando_letras for elem in sublist] #hace que creando_letras sea una sola lista

    # El primer elemento de key es 999 para identificar que es una ficha de la maquina y que no pase nada si el jugador aprieta ahí
    tablero = [[sg.Button(size=(AN, AL), key=(999,j), pad=(21.5,18)) for j in range(cant_letras)]]
    tablero.extend([[m_tablero.crear_boton(i,j,AN,AL,nivel) for j in range(filas)] for i in range(filas)])
    tablero.extend([[sg.Text("Seleccione una letra de abajo",pad=(200,5))],
        [sg.Button(m_tablero.tomar_y_borrar(Letras), key = j, size=(AN, AL), pad=(21.5,0)) for j in range(cant_letras)],
        [sg.Button('Ingresar Palabra!', size= (7,3), pad=(40.5,20)),sg.Button('Cambiar letras', size= (7,3), pad=(40.5,20)),
        sg.Button('Posponer', size=(7, 3), pad=(40.5,20)),sg.Button('Terminar', size=(7, 3), pad=(40.5,20))]])
    tablero.extend([[sg.Text('Tiempo',key='timer',pad=(270,0))]])

    # \n pone lo que sigue un renglón más abajo  
    zona_puntos_jugador = [[sg.Button("PUNTOS\n"+str(puntos_jugador), size=(8, 4), key=(888,0), pad=(0,340))]]
    zona_puntos_maquina = [[sg.Button("PUNTOS\n"+str(puntos_maquina), size=(8, 4), key=(888,1), pad=(0,340))]]

    pal_y_pun_jug_en_pantalla = [[m_tablero.palabras_por_turno_pantalla(444,j) for j in range(20)]] # Puede mostrar hasta 20 palabras
    pal_y_pun_maq_en_pantalla = [[m_tablero.palabras_por_turno_pantalla(445,j) for j in range(20)]] # Puede mostrar hasta 20 palabras

    layout = [[sg.Column(pal_y_pun_maq_en_pantalla),sg.Column(zona_puntos_maquina),sg.Column(tablero),sg.Column(zona_puntos_jugador),sg.Column(pal_y_pun_jug_en_pantalla)]]

    window = sg.Window('ScrabbleAR',layout)

    #Variables del juego
    if hay_save: # aca cargo todos los datos
        save,lugares_usados_temp,lugares_usados_total,vertical,horizontal, \
        letras_ingresadas,backup_text,palabra,pos_atril_usadas,Letras, \
        puntos_jugador,puntos_maquina,turno_jugador,tiempo_actual,tiempo, \
        valores_de_letras,veces_cambiadas = inicializar_variables(save_window,datos_usuario)
    else:
        tiempo_actual = 0
        save = {}
        lugares_usados_temp = []
        lugares_usados_total = []
        m_maquina.letras_de_maquina = []
        m_maquina.inicializar_letras_maquina(Letras) # Le da 7 letras a la máquina
        vertical = False
        horizontal = False
        letras_ingresadas = 0
        backup_text = [] #lista con texto de botones p/ restablecer en caso de palabra erronea.
        palabra = [] # borre letras usadas y solo queda palabra. mande a las funciones que usaban letras_usadas palabras y funcionan igual.
        pos_atril_usadas = [] # lista con las posiciones usadas del atril. Sirve en caso de reponer y para que no se vuelvan a usar.
        # reponer, además,  cuando se usa una letra se guarda acá y si está acá ya no se puede usar otra vez
        turno_jugador = choice([True, False])
        veces_cambiadas = 0
    cambiar = False

    TIEMPO = tiempo # tiempo de juego en secs
    # WINDOW LOOP

    while True:
        event, values = window.read(timeout=100)
        if hay_save:
            for key in save:
                window[key].update(save[key],visible = True) # parece que hace un update con todas las keys de un diccionario.
            m_tablero.actualizar_puntos(0,window,puntos_jugador)
            m_tablero.actualizar_puntos(1,window,puntos_maquina)
            window.Refresh()
            #print(save)
            hay_save = False

        tiempo_actual += 0.1
        window['timer'].update('{}:{:02d}'.format((TIEMPO -round(tiempo_actual))//60,(TIEMPO -round(tiempo_actual))%60)) # lo hice asi para que la cuenta sea regresiva

        if (tiempo_actual >= TIEMPO):
            razon_fin = '¡Terminó el tiempo!'
            if palabra:
                m_tablero.quitar_letras(lugares_usados_temp,backup_text,window)
                m_tablero.devolver_letras_atril(palabra,pos_atril_usadas,window) # te devuelve letras si justo estabas metiendo en el tablero y se termino el tiempo
            mostrar_puntaje(razon_fin,puntos_jugador,puntos_maquina,window,m_maquina.letras_de_maquina,valores_de_letras,cant_letras)
            break

        if event == 'Posponer':
            guardar(save,lugares_usados_total,lugares_usados_temp,window,pos_atril_usadas,nivel,bolsa_letras,
                letras_ingresadas,palabra,backup_text,horizontal,vertical,puntos_jugador, 
                puntos_maquina,Letras,tiempo_actual,TIEMPO,valores_de_letras,veces_cambiadas)
            break
        
        if event in (None,'Terminar'):
            break
        
        if event == 'Cambiar letras' and veces_cambiadas<3:
            m_tablero.quitar_letras(lugares_usados_temp,backup_text,window)
            m_tablero.devolver_letras_atril(palabra,pos_atril_usadas,window)
            m_tablero.cambiar_letras(window,Letras,cant_letras)
            veces_cambiadas+=1
            turno_jugador = False

        #SI ES EL TURNO DEL JUGADOR
        if turno_jugador:

            #AGARRO DEL ATRIL
            if m_tablero.es_letra_atril(event):
                #escribir = event[0] # ahora no puedo agarrar directamente de event el texto del boton. 
                if event not in pos_atril_usadas: # para que no se puedan agarrar los "---"
                    escribir = window.Element(event).GetText()
                    cambiar = True
                    boton_de_la_letra = event # Con esto puedo acceder al botón de la letra usada // ahora es un integer.
        
            if m_tablero.puedo_cambiar(cambiar,event,lugares_usados_temp,lugares_usados_total):  
                
            #INGRESAR PRIMERA LETRA
                if not lugares_usados_total: # Si lugares usados es vacio, solo permito ingresar en inicio.
                    if event == INICIO:
                        m_tablero.agregar_letra(lugares_usados_total,backup_text,event,escribir,save,
                                                lugares_usados_temp,palabra,boton_de_la_letra,window,pos_atril_usadas)  
                        cambiar = False
                        letras_ingresadas += 1
                else:
                    #DETERMINAR SI SE INGRESA HORIZONTAL O VERTICAL
                    #print(horizontal)
                    if not lugares_usados_temp:
                        m_tablero.agregar_letra(lugares_usados_total,backup_text,event,escribir,save,
                                                lugares_usados_temp,palabra,boton_de_la_letra,window,pos_atril_usadas)
                        cambiar = False
                        letras_ingresadas += 1
                    else:
                        if not horizontal:
                            if m_tablero.es_vertical(letras_ingresadas,event,lugares_usados_temp):
                                vertical = True # Si suma o resta 1 a las columnas, vertical = true
                                m_tablero.agregar_letra(lugares_usados_total,backup_text,event,escribir,save,
                                                        lugares_usados_temp,palabra,boton_de_la_letra,window,pos_atril_usadas)                
                                cambiar = False
                                letras_ingresadas += 1
                        if not vertical:
                            if m_tablero.es_horizontal(letras_ingresadas,event,lugares_usados_temp):
                                horizontal = True
                                m_tablero.agregar_letra(lugares_usados_total,backup_text,event,escribir,save,
                                                        lugares_usados_temp,palabra,boton_de_la_letra,window,pos_atril_usadas)
                                cambiar = False
                                letras_ingresadas += 1
                
                    # SE BORRA LA LETRA USADA
                if not cambiar: # si cambiar pasa a false, es porque ya puso una letra en el atril.
                    #print(boton_de_la_letra)
                    window[boton_de_la_letra].update("---")
            
        
            #CHEQUEO DE PALABRA
            if m_tablero.ingreso_palabra(letras_ingresadas,event):
                to_string = ''.join(palabra) # paso lista palabra a string
                if not m_buscador.buscar_palabra(to_string,nivel):
                    m_tablero.quitar_letras(lugares_usados_temp,backup_text,window)
                    m_tablero.devolver_letras_atril(palabra,pos_atril_usadas,window)
                    
                    # reset de variables:
                    pos_atril_usadas = []
                    horizontal = False
                    vertical = False
                    backup_text = []
                    letras_ingresadas = 0
                    for tupla in lugares_usados_temp:
                        lugares_usados_total.remove(tupla) # quito valores de temp que estan en total.
                        save.pop(tupla) # tambien la quito de save.
                    lugares_usados_temp = []
                    palabra = []
                    cambiar = False
                else:
                    turno_jugador = False
                    puntos_actuales = m_tablero.calcular_puntos(palabra,lugares_usados_temp,valores_de_letras,nivel)
                    puntos_jugador += puntos_actuales
                    m_tablero.agregar_pal_y_pun_a_pantalla(to_string,0,puntos_actuales,window,save)
                    m_tablero.actualizar_puntos(0,window,puntos_jugador)
                    try:
                        m_tablero.dar_nuevas_letras(Letras,pos_atril_usadas,window) # si index error = lista vacia
                    except IndexError:
                        razon_fin = ('Se terminaron las fichas!')
                        mostrar_puntaje(razon_fin,puntos_jugador,puntos_maquina,window,m_maquina.letras_de_maquina,valores_de_letras)
                        break
                    pos_atril_usadas = []
                    horizontal = False
                    vertical = False
                    backup_text = []
                    letras_ingresadas = 0
                    lugares_usados_temp = []
                    palabra = []
                    cambiar = False
            #print(palabra)
        
        #SI ES EL TURNO DE LA MÁQUINA
        else:
            turno_jugador = True
            if nivel == "dificil":
                palabra_maquina = str(m_maquina.palabra_maxima(valores_de_letras)) # Sin str lo considera NoneType
            else:
                palabra_maquina = str(m_maquina.devolver_palabra()) # Sin str lo considera NoneType
            if palabra_maquina != 'No encontre palabra':
                posiciones_para_la_maquina = m_maquina.encontrar_lugar(lugares_usados_total,len(palabra_maquina))
                puntos_actuales = m_tablero.calcular_puntos(palabra_maquina,posiciones_para_la_maquina,valores_de_letras,nivel)
                puntos_maquina += puntos_actuales
                pos = 0                              
                for letra in palabra_maquina:
                    window[posiciones_para_la_maquina[pos]].update(letra)
                    save[posiciones_para_la_maquina[pos]] = letra
                    pos += 1
                m_tablero.agregar_pal_y_pun_a_pantalla(palabra_maquina,1,puntos_actuales,window,save)
                m_tablero.actualizar_puntos(1,window,puntos_maquina)
                lugares_usados_total.extend(posiciones_para_la_maquina)
                try:
                    m_maquina.cambiar_letras_usadas_por_nuevas(palabra_maquina,Letras)
                except IndexError:
                    razon_fin = 'Se acabaron las fichas!'
                    mostrar_puntaje(razon_fin,puntos_jugador,puntos_maquina,window,m_maquina.letras_de_maquina,cant_letras)
                    break
            
    window.close()

while True:
    opcion_elegida = menu()
    if opcion_elegida == 'Nueva partida':
        main()
    elif opcion_elegida == 'Cargar partida':
        main(True)
    elif opcion_elegida == 'Configurar':
        configuracion_elegida = configurar()
        if configuracion_elegida != None:
            main(False,configuracion_elegida["tiempo"],configuracion_elegida["nivel"],configuracion_elegida["puntaje fichas"],configuracion_elegida["cantidad fichas"])
    elif opcion_elegida == 'Top ten\npuntajes':
        top_puntajes()
    else:
        break
