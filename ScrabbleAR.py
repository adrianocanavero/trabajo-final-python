import PySimpleGUI as sg
from random import choice
import m_buscador
import m_tablero
from m_fichas import valores_letras
import m_maquina
import pickle
import time
from m_menu import menu
from m_topten import top_puntajes
from m_configuracion import configurar
import winsound

def main(hay_save,nivel="facil"):


    """ Funcion main: ejecuta el juego debidamente. Recibe True si el jugador eligio Nueva Partida o False si
        el jugador eligió Cargar Partida"""
        
    def ganar(total_jugador,total_maquina):
        """Crea y muestra la ventana del ganador, y permite ingresar el puntaje para guardarlo en los top ten"""

        win_layout = [[sg.Text('¡Ganaste!',font= 'Any 16',size =(25,1), justification='center')],
                        [sg.Text('Puntaje PC: ' + str(total_maquina)), sg.Text('Puntaje jugador: ' + str(total_jugador))],
                        [sg.Text('Ingresa tu nombre:')],
                        [sg.InputText()],
                        [sg.Button('Guardar Puntaje')]]
        win_window = sg.Window('Scrabble AR',win_layout,keep_on_top=True)
        try:
            winsound.PlaySound('ganar.wav', winsound.SND_ASYNC)
        except:
            pass
        while True:
            e,v = win_window.read()
            if e == 'Guardar Puntaje' and v[0]!='Ingresa tu nombre:':
                archivo_topten = open('top_ten.txt', 'a') #si no existe arch, crea. si existe, agrega al final.
                archivo_topten.write(v[0] + ': ' + str(total_jugador) + '\n')
                archivo_topten.close()
                break
            if e == None:
                break
        win_window.close()

    def mostrar_puntaje(razon_fin,puntos_jugador,puntaje_maquina,window,letras_maquina,valores_letras):

        """Se ejecuta luego de que termina el tiempo o se terminan las fichas. Muestra las fichas que le quedaron al jugador
            y a la maquina y lo que van a restar del puntaje obtenido por la formación de palabras."""

        def calcularResta(lista_letras, valores_letras):
            puntaje_restar = 0
            for letra in lista_letras:
                puntaje_restar+= valores_letras[letra]
            return puntaje_restar
        letras_atril = []

        for i in range(cant_letras):
            if window[i].GetText() != '---':
                letras_atril.append(window[i].GetText())

        resta_jugador = calcularResta(letras_atril,valores_letras)
        resta_maquina = calcularResta(letras_maquina,valores_letras)

        layout_atril_jugador = [[sg.Text('Tus letras')], [sg.Button(m_tablero.tomar_y_borrar(letras_atril), key = j, size=(AN, AL), pad=(21.5,0)) for j in range(len(letras_atril))],
                                [sg.Text('Puntaje a restar : ' + str(resta_jugador))]]
        layout_atril_maquina = [[sg.Text('Letras de PC')],[sg.Button(m_tablero.tomar_y_borrar(letras_maquina), key = j, size=(AN, AL), pad=(21.5,0)) for j in range(len(letras_maquina))],
                                [sg.Text('Puntaje a restar : ' + str(resta_maquina))]]
        
        layout_final = [[sg.Column(layout_atril_jugador)], [sg.Column(layout_atril_maquina)], [sg.Button('Siguiente')]]

        window_final = sg.Window(razon_fin,layout_final,keep_on_top=True) #se mantiene siempre arriba del tablero
        while True:
            evento,values = window_final.read()
            if evento == None:
                window_final.close() # lo hago para que no se vea esta pantalla atras del cartel de ganar
                break
            if evento == 'Siguiente':
                total_maquina = puntos_maquina - resta_maquina
                total_jugador = puntos_jugador - resta_jugador
                if total_jugador> total_maquina:
                    window_final.close()
                    ganar(total_jugador,total_maquina)
                    break
                elif total_jugador<total_maquina:
                    window_final.close()
                    #perder(total_jugador,total_maquina)
                    break
                else:
                    window_final.close()
                    #empate(total_jugador)
                    break
    
    def guardar(save,lugares_usados_total,lugares_usados_temp,window,pos_atril_usadas,nivel,
                letras_ingresadas,palabra,backup_text,horizontal,vertical,puntos_jugador,puntos_maquina,Letras,tiempo_actual):
        """Guarda la información de la partida si el jugador elige Posponer. En save se encuentra la informacion del tablero,
            mientras que en datos_usuario estan los datos indispensables que necesita el juego para realizar sus funciones"""

        for i in range (7):
            save[i] = window[i].GetText()
        save['timer'] = tiempo_actual
        archivo_save = open('savewindow.pickle', 'wb')
        pickle.dump(save,archivo_save)
        archivo_save.close()
        archivo_save = open('datos_usuario.pickle', 'wb')
        datos_usuario ={'lug_tot': lugares_usados_total,
                        'lug_temp':lugares_usados_temp,
                        'pos_at': pos_atril_usadas,
                        'let_ing': letras_ingresadas,
                        'pal': palabra,
                        'back_txt': backup_text,
                        'hor': horizontal,
                        'ver': vertical,
                        'letras': Letras, 
                        'pj': puntos_jugador,
                        'pm': puntos_maquina,
                        'pos_jug': m_tablero.posicion_jugador,
                        'pos_maq': m_tablero.posicion_maquina,
                        'atril_maq': m_maquina.letras_de_maquina,
                        'nivel': nivel
                        }
        pickle.dump(datos_usuario,archivo_save)
        archivo_save.close()
    
    # Intento abrir archivo. 
    if (hay_save): 
        try:
            archivo_save = open('savewindow.pickle', 'rb')
            save_window = pickle.load(archivo_save) #aca guardo para actualizar el tablero
            archivo_save.close()
            print(save_window)
            archivo_save = open('datos_usuario.pickle', 'rb')
            datos_usuario = pickle.load(archivo_save) #aca guardo los datos del usuario
            archivo_save.close()
            print(datos_usuario)
            nivel = datos_usuario['nivel']
        except EOFError: ## si no hay save, no tendria porque haber problema
            hay_save = False
        except FileNotFoundError:
            hay_save = False

    #LAYOUT
        
    puntos_jugador = 0
    puntos_maquina = 0
    AN = 4 # Este es el ancho de los botones
    AL = 2 # Este es el alto de los botones
    INICIO = (7,7)
    filas = 15
    cant_letras = 7
    creando_letras = [['A']*11,['B']*3,['C']*4,['D']*4,['E']*11,['F']*2,['G']*2,['H']*2,['I']*6,['J']*2,['K']*2,['L']*4,['M']*3,['N']*5,
                ['Ñ']*2,['O']*8,['P']*2,['Q']*2,['R']*4,['S']*7,['T']*4,['U']*6,['V']*2,['W']*2,'X',['Y']*2,'Z']

    Letras = [elem for sublist in creando_letras for elem in sublist] #hace que creando_letras sea una sola lista.
    


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
        save = save_window # si hay save pongo en save lo que hay en verificar_guardado.
        lugares_usados_temp = datos_usuario['lug_temp']
        lugares_usados_total = datos_usuario['lug_tot']
        vertical = datos_usuario['ver']
        horizontal = datos_usuario['hor']
        letras_ingresadas = datos_usuario['let_ing']
        backup_text = datos_usuario['back_txt']
        palabra = datos_usuario['pal']
        pos_atril_usadas = datos_usuario['pos_at'] 
        Letras = datos_usuario['letras']
        puntos_jugador = datos_usuario['pj']
        puntos_maquina = datos_usuario['pm']
        m_tablero.posicion_maquina = datos_usuario['pos_maq']
        m_tablero.posicion_jugador = datos_usuario['pos_jug']
        m_maquina.letras_de_maquina = datos_usuario['atril_maq']
        turno_jugador = True # si se carga la partida siempre es el turno del jugador.
        tiempo_actual = save['timer']
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
    cambiar = False

    TIEMPO = 120 # tiempo de juego en secs
    # WINDOW LOOP

    while True:
        event, values = window.read(timeout=100)
  
        if hay_save:
            for key in save:
                window[key].update(save[key],visible = True) # parece que hace un update con todas las keys de un diccionario.
            m_tablero.actualizar_puntos(0,window,puntos_jugador)
            m_tablero.actualizar_puntos(1,window,puntos_maquina)
            window.Refresh()
            print(save)
            hay_save = False

        tiempo_actual += 0.1
        window['timer'].update('{}:{:02d}'.format((TIEMPO -round(tiempo_actual))//60,(TIEMPO -round(tiempo_actual))%60)) # lo hice asi para que la cuenta sea regresiva

        if (tiempo_actual >= TIEMPO):
            razon_fin = '¡Terminó el tiempo!'
            if palabra:
                m_tablero.quitar_letras(lugares_usados_temp,backup_text,window)
                m_tablero.devolver_letras_atril(palabra,pos_atril_usadas,window) # te devuelve letras si justo estabas metiendo en el tablero y se termino el tiempo
            mostrar_puntaje(razon_fin,puntos_jugador,puntos_maquina,window,m_maquina.letras_de_maquina,valores_letras)
            break

        if event == 'Posponer':
            guardar(save,lugares_usados_total,lugares_usados_temp,window,pos_atril_usadas,nivel,
                letras_ingresadas,palabra,backup_text,horizontal,vertical,puntos_jugador, 
                puntos_maquina,Letras,tiempo_actual)
            break
        
        if event in (None,'Terminar'):
            break
        
        if event == 'Cambiar letras':
            m_tablero.cambiar_letras(window,Letras,cant_letras)

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
                if not m_buscador.buscar_palabra(to_string):
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
                    puntos_actuales = m_tablero.calcular_puntos(palabra,lugares_usados_temp,valores_letras,nivel)
                    puntos_jugador += puntos_actuales
                    m_tablero.agregar_pal_y_pun_a_pantalla(to_string,0,puntos_actuales,window,save)
                    m_tablero.actualizar_puntos(0,window,puntos_jugador)
                    try:
                        m_tablero.dar_nuevas_letras(Letras,pos_atril_usadas,window) # si index error = lista vacia
                    except IndexError:
                        razon_fin = ('Se terminaron las fichas!')
                        mostrar_puntaje(razon_fin,puntos_jugador,puntos_maquina,window,m_maquina.letras_de_maquina,valores_letras)
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
            palabra_maquina = str(m_maquina.devolver_palabra()) # Sin str lo considera NoneType
            if palabra_maquina != 'No encontre palabra':
                posiciones_para_la_maquina = m_maquina.encontrar_lugar(lugares_usados_total,len(palabra_maquina))
                puntos_actuales = m_tablero.calcular_puntos(palabra_maquina,posiciones_para_la_maquina,valores_letras,nivel)
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
                    mostrar_puntaje(razon_fin,puntos_jugador,puntos_maquina,window,m_maquina.letras_de_maquina)
                    break
            
    window.close()

while True:
    opcion_elegida = menu()
    if opcion_elegida == 'Nueva partida':
        main(False)
    elif opcion_elegida == 'Cargar partida':
        main(True)
    elif opcion_elegida == 'Configurar':
        configurar()
        print("NO ESTÁ IMPLEMENTADO TODAVÍA")
    elif opcion_elegida == 'Top ten\npuntajes':
        top_puntajes()
    else:
        break
