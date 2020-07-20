import PySimpleGUI as sg
from random import choice
import Modulos.m_buscador as m_buscador
import Modulos.m_tablero as m_tablero
from Modulos.m_fichas import valores_letras
from Modulos.m_fichas import bolsa_de_letras
import Modulos.m_maquina as m_maquina
import time
from Modulos.m_menu import menu
from Modulos.m_topten import top_puntajes
from Modulos.m_configuracion import configurar
from Modulos.m_veredicto import mostrar_puntaje
from Modulos.m_guardado import guardar,inicializar_variables,abrir_guardado
import Modulos.m_sonidos as sound

def main(hay_save=False,tiempo=60,nivel="facil",valores_de_letras=valores_letras,bolsa_letras=bolsa_de_letras):

    """Funcion main: ejecuta el juego debidamente. El primer parámetro determina si hay una partida 
        guardada y los otros la configuración del juego. Todos tienen valores por defecto"""
    
    # Si se eligió "Cargar partida" se cargan los datos de la partida guardada en variables
    if (hay_save): 
        save_window,datos_usuario,nivel,bolsa_letras = abrir_guardado()
    m_maquina.nivel = nivel # Se guarda en la máquina el nivel de la partida porque va a ser usado
    
    #LAYOUT
        
    puntos_jugador = 0
    puntos_maquina = 0
    AN = 4 # Este es el ancho de los botones
    AL = 2 # Este es el alto de los botones
    INICIO = (7,7)
    filas = 15
    cant_letras = 7 # Es más fácil cambiar la cantidad de letras a usar si existe esta variable, porque se modifica un solo número
    creando_letras = bolsa_letras

    Letras = [elem for sublist in creando_letras for elem in sublist] # hace que creando_letras sea una sola lista

    # El primer elemento de key es 999 para identificar que es una ficha de la maquina y que no pase nada si el jugador aprieta ahí
    tablero = [[sg.Button(size=(AN, AL), key=(999,j), pad=(21.5,18), button_color=('white', '#3d578b')) for j in range(cant_letras)]]
    tablero.extend([[m_tablero.crear_boton(i,j,AN,AL,nivel) for j in range(filas)] for i in range(filas)])
    tablero.extend([[sg.Text("Seleccione una letra de abajo",pad=(200,5))],
        [sg.Button(m_tablero.tomar_y_borrar(Letras), key = j, size=(AN, AL), pad=(21.5,0), button_color=('white', '#3d578b')) for j in range(cant_letras)],
        [sg.Button('Ingresar palabra', size= (7,3), key=(471,471), pad=(40.5,20), button_color=('white', '#52313a')),sg.Button('Cambiar letras', size= (7,3), pad=(40.5,20), button_color=('white', '#52313a')),
        sg.Button('Posponer', size=(7, 3), pad=(40.5,20), button_color=('white', '#52313a')),sg.Button('Terminar', size=(7, 3), pad=(40.5,20), button_color=('white', '#52313a'))]])
    tablero.extend([[sg.Text('Tiempo',key='timer',pad=(270,0))]])

    # \n pone lo que sigue un renglón más abajo  
    zona_puntos_jugador = [[sg.Text("",pad=(0,130))],[sg.Button("JUGADOR",size=(8,2), key=(456,0), pad=(0,10), button_color=('white', '#272727'))],
        [sg.Button("PUNTOS\n"+str(puntos_jugador), size=(8, 4), key=(888,0), pad=(0,0), button_color=('white', '#4b4b4b'))]]
    zona_puntos_maquina = [[sg.Text("",pad=(0,130))],[sg.Button("MÁQUINA",size=(8,2), key=(456,1), pad=(5,10), button_color=('white', '#272727'))],
        [sg.Button("PUNTOS\n"+str(puntos_maquina), size=(8, 4), key=(888,1), pad=(5,0), button_color=('white', '#4b4b4b'))]]

    pal_y_pun_jug_en_pantalla = [[m_tablero.palabras_por_turno_pantalla(444,j) for j in range(25)]] # Puede mostrar hasta 25 palabras
    pal_y_pun_maq_en_pantalla = [[m_tablero.palabras_por_turno_pantalla(445,j) for j in range(25)]] # Puede mostrar hasta 25 palabras

    layout = [[sg.Column(pal_y_pun_maq_en_pantalla),sg.Column(zona_puntos_maquina),sg.Column(tablero),sg.Column(zona_puntos_jugador),sg.Column(pal_y_pun_jug_en_pantalla)]]

    window = sg.Window('ScrabbleAR',layout)

    # Variables del juego
    if hay_save: # aca se cargan todos los datos
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
        backup_text = [] # lista con texto de botones para restablecer en caso de palabra erronea.
        palabra = []
        pos_atril_usadas = [] # lista con las posiciones usadas del atril. Sirve en caso de reponer y para que no se
        # vuelvan a usar. Además, cuando se usa una letra se guarda acá y si está acá ya no se puede usar otra vez
        turno_jugador = choice([True, False])
        veces_cambiadas = 0
    cambiar = False

    TIEMPO = tiempo # tiempo de juego en segundos
    
    fondo = sound.s_fondo() # empieza musica de fondo

    # WINDOW LOOP

    while True:
        
        event, values = window.read(timeout=100)
        if hay_save:
            for key in save:
                window[key].update(save[key],visible = True) # hace un update con todas las keys de un diccionario.
            m_tablero.actualizar_puntos(0,window,puntos_jugador)
            m_tablero.actualizar_puntos(1,window,puntos_maquina)
            window.Refresh()
            #print(save)
            hay_save = False

        tiempo_actual += 0.1
        window['timer'].update('{}:{:02d}'.format((TIEMPO -round(tiempo_actual))//60,(TIEMPO -round(tiempo_actual))%60)) # la cuenta es regresiva

        if (tiempo_actual >= TIEMPO):
            if fondo != None: fondo.fadeout(500)
            razon_fin = '¡Terminó el tiempo!'
            if palabra:
                m_tablero.quitar_letras(lugares_usados_temp,backup_text,window)
                m_tablero.devolver_letras_atril(palabra,pos_atril_usadas,window) # devuelve letras si se termina el tiempo y se estaban poniendo letras
            mostrar_puntaje(razon_fin,puntos_jugador,puntos_maquina,window,m_maquina.letras_de_maquina,valores_de_letras,cant_letras)
            break

        if event == 'Posponer':
            if fondo != None: fondo.fadeout(500)
            guardar(save,lugares_usados_total,lugares_usados_temp,window,pos_atril_usadas,nivel,bolsa_letras,
                letras_ingresadas,palabra,backup_text,horizontal,vertical,puntos_jugador, 
                puntos_maquina,Letras,tiempo_actual,TIEMPO,valores_de_letras,veces_cambiadas)
            break
        
        if event == None:
            if fondo != None: fondo.fadeout(500)
            break

        if event == 'Terminar':
            if fondo != None: fondo.fadeout(500)
            m_tablero.quitar_letras(lugares_usados_temp,backup_text,window)
            m_tablero.devolver_letras_atril(palabra,pos_atril_usadas,window)
            razon_fin = 'Terminar'
            mostrar_puntaje(razon_fin,puntos_jugador,puntos_maquina,window,m_maquina.letras_de_maquina,valores_de_letras,cant_letras)
            break
        
        if event == 'Cambiar letras' and veces_cambiadas<3:
            if pos_atril_usadas: # si el usuario ingreso letras en el tablero y eligió cambiar.
                m_tablero.quitar_letras(lugares_usados_temp,backup_text,window) # se devuelve fichas y se resetea variables de ingreso de palabras.
                m_tablero.devolver_letras_atril(palabra,pos_atril_usadas,window)
                # reset variables
                pos_atril_usadas = []
                horizontal = False
                vertical = False
                backup_text = []
                letras_ingresadas = 0
                for tupla in lugares_usados_temp:
                    lugares_usados_total.remove(tupla) # se sacan valores de temp que estan en total.
                    save.pop(tupla) # tambien se saca de save.
                lugares_usados_temp = []
                palabra = []
                cambiar = False
            if m_tablero.cambiar_letras(window,Letras,cant_letras): # se realiza la funcion de cambiar letras y si devuelve true, se hace efectivo el if.
                veces_cambiadas+=1
                turno_jugador = False

        #SI ES EL TURNO DEL JUGADOR
        if turno_jugador:

            #AGARRO DEL ATRIL
            if m_tablero.es_letra_atril(event):
                if event not in pos_atril_usadas: # para que no se puedan agarrar los "---"
                    escribir = window.Element(event).GetText()
                    cambiar = True
                    boton_de_la_letra = event # Con esto se puede acceder al botón de la letra usada. Ahora es un integer.
        
            if m_tablero.puedo_cambiar(cambiar,event,lugares_usados_temp,lugares_usados_total):  
                
            #INGRESAR PRIMERA LETRA
                if not lugares_usados_total: # Si lugares usados es vacio, solo se permite ingresar en inicio.
                    if event == INICIO:
                        cambiar = m_tablero.agregar_letra(lugares_usados_total,backup_text,event,escribir,save,
                                                lugares_usados_temp,palabra,boton_de_la_letra,window,pos_atril_usadas)
                        if not cambiar: # Si se puso una letra se aumenta en 1 letras_ingresadas
                            letras_ingresadas += 1
                else:
                    #DETERMINAR SI SE INGRESA HORIZONTAL O VERTICAL
                    # print(horizontal)
                    if not lugares_usados_temp:
                        cambiar = m_tablero.agregar_letra(lugares_usados_total,backup_text,event,escribir,save,
                                                lugares_usados_temp,palabra,boton_de_la_letra,window,pos_atril_usadas)
                        if not cambiar: # Si se puso una letra se aumenta en 1 letras_ingresadas
                            letras_ingresadas += 1
                    else:
                        if not horizontal:
                            if m_tablero.es_vertical(letras_ingresadas,event,lugares_usados_temp):
                                vertical = True # Si suma o resta 1 a las columnas, vertical = true
                                cambiar = m_tablero.agregar_letra(lugares_usados_total,backup_text,event,escribir,save,
                                                        lugares_usados_temp,palabra,boton_de_la_letra,window,pos_atril_usadas)                
                                if not cambiar: # Si se puso una letra se aumenta en 1 letras_ingresadas
                                    letras_ingresadas += 1
                        if not vertical:
                            if m_tablero.es_horizontal(letras_ingresadas,event,lugares_usados_temp):
                                horizontal = True
                                cambiar = m_tablero.agregar_letra(lugares_usados_total,backup_text,event,escribir,save,
                                                        lugares_usados_temp,palabra,boton_de_la_letra,window,pos_atril_usadas)
                                if not cambiar: # Si se puso una letra se aumenta en 1 letras_ingresadas
                                    letras_ingresadas += 1
                
                # SE BORRA LA LETRA USADA
                if not cambiar: # si cambiar pasa a false, es porque ya se puso una letra en el atril.
                    # print(boton_de_la_letra)
                    window[boton_de_la_letra].update("---")
            
            #CHEQUEO DE PALABRA
            if m_tablero.ingreso_palabra(letras_ingresadas,event):
                to_string = ''.join(palabra) # se pasa lista palabra a string
                if not m_buscador.buscar_palabra(to_string,nivel):
                    sound.s_invalida()
                    m_tablero.quitar_letras(lugares_usados_temp,backup_text,window)
                    m_tablero.devolver_letras_atril(palabra,pos_atril_usadas,window)
                    
                    # reset de variables:
                    pos_atril_usadas = []
                    horizontal = False
                    vertical = False
                    backup_text = []
                    letras_ingresadas = 0
                    for tupla in lugares_usados_temp:
                        lugares_usados_total.remove(tupla) # se sacan valores de temp que estan en total.
                        save.pop(tupla) # tambien se saca de save.
                    lugares_usados_temp = []
                    palabra = []
                    cambiar = False
                else:
                    sound.s_valida()
                    turno_jugador = False
                    puntos_actuales = m_tablero.calcular_puntos(palabra,lugares_usados_temp,valores_de_letras,nivel)
                    puntos_jugador += puntos_actuales
                    m_tablero.agregar_pal_y_pun_a_pantalla(to_string,0,puntos_actuales,window,save)
                    m_tablero.actualizar_puntos(0,window,puntos_jugador)
                    try:
                        m_tablero.dar_nuevas_letras(Letras,pos_atril_usadas,window) 
                    except IndexError: # si index error = lista vacia
                        if fondo != None: fondo.fadeout(500)
                        razon_fin = '¡Se acabaron las fichas!'
                        mostrar_puntaje(razon_fin,puntos_jugador,puntos_maquina,window,m_maquina.letras_de_maquina,valores_de_letras,cant_letras)
                        break
                    pos_atril_usadas = []
                    horizontal = False
                    vertical = False
                    backup_text = []
                    letras_ingresadas = 0
                    lugares_usados_temp = []
                    palabra = []
                    cambiar = False
            # print(palabra)
        
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
                except IndexError: # si index error = lista vacia
                    if fondo != None: fondo.fadeout(500)
                    razon_fin = '¡Se acabaron las fichas!'
                    mostrar_puntaje(razon_fin,puntos_jugador,puntos_maquina,window,m_maquina.letras_de_maquina,valores_de_letras,cant_letras)
                    break
            
    window.close()

# PROGRAMA PRINCIPAL
play = True
while True:
    if play:
        sonido_menu = sound.s_menu()
        play = False
    opcion_elegida = menu()
    if opcion_elegida == 'Nueva partida':
        sound.s_boton()
        if sonido_menu != None: sonido_menu.fadeout(500)
        main()
    elif opcion_elegida == 'Cargar partida':
        sound.s_boton()
        sonido_menu.fadeout(500)
        main(True)
    elif opcion_elegida == 'Configurar':
        sound.s_boton()
        configuracion_elegida = configurar()
        if configuracion_elegida != None:
            main(False,configuracion_elegida["tiempo"],configuracion_elegida["nivel"],configuracion_elegida["puntaje fichas"],configuracion_elegida["cantidad fichas"])
    elif opcion_elegida == 'Top ten\npuntajes':
        sound.s_boton()
        top_puntajes()
    else:
        break
