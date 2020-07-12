import PySimpleGUI as sg
import pickle
import winsound
from m_tablero import tomar_y_borrar



def ganar(total_jugador,total_maquina):

    """Crea y muestra la ventana del ganador, y permite ingresar el puntaje para guardarlo en los top ten"""
    try: # esto lo hago para determinar si se tiene que mostrar el guardar puntaje o no: se muestra solo si hay lugares o si el puntaje es mayor a alguno del top.
        archivo_topten = open('top_ten.pickle', 'rb')
        dic_top = pickle.load(archivo_topten)
        if len(dic_top) == 10: # si el dic tiene 10
            min = 9999
            for key in dic_top: # busco en el diccionario el minimo a sacar.
                if min > dic_top[key]:
                    minkey = key
                    min = dic_top[key]
            if total_jugador > min:
                mostrar = True # queda sacar clave minima
            else:
                mostrar = False
        else:
            mostrar = True
        archivo_topten.close()
    except FileNotFoundError:
        dic_top = {}
        mostrar = True
    win_layout = [[sg.Text('¡Ganaste!',font= 'Any 16',size =(25,1), justification='center')],
                    [sg.Text('Puntaje PC: ' + str(total_maquina), font= 'Any 14'), sg.Text('Puntaje jugador: ' + str(total_jugador), font= 'Any 14')],
                    [sg.Text('Ingresa tu nombre:', visible=mostrar)],
                    [sg.InputText(visible=mostrar)],
                    [sg.Button('Guardar Puntaje', visible=mostrar)],
                    [sg.Button('Salir')]]
    win_window = sg.Window('Resultado',win_layout,keep_on_top=True)
    try:
        winsound.PlaySound('ganar.wav', winsound.SND_ASYNC)
    except:
        pass
    while True:
        e,v = win_window.read()
        if e == 'Guardar Puntaje' and v[0]!='Ingresa tu nombre:':
            if len(dic_top)== 10:
                dic_top.pop(minkey)
                dic_top[v[0]] = total_jugador
                archivo_topten = open('top_ten.pickle', 'wb')
                print(dic_top)
                pickle.dump(dic_top,archivo_topten)
                archivo_topten.close()
            else:
                dic_top[v[0]] = total_jugador
                archivo_topten = open('top_ten.pickle', 'wb')
                pickle.dump(dic_top,archivo_topten)
                archivo_topten.close()
                print(dic_top)
            break
        if e in ('Salir', None):
            break
    win_window.close()

def perder_empatar(total_jugador,total_maquina,resultado):

    """Crea  y muestra la ventana en caso de perder o empate."""

    layout = [[sg.Text(resultado,font= 'Any 16',size =(25,1), justification='center')],
                    [sg.Text('Puntaje PC: ' + str(total_maquina), font= 'Any 14'), sg.Text('Puntaje jugador: ' + str(total_jugador), font= 'Any 14')],
                    [sg.Button('Salir')]]
    
    window = sg.Window('Resultado', layout)
    
    while True:
        e,v = window.read()
        if e in('Salir', None):
            break

    window.close()

def mostrar_puntaje(razon_fin,puntos_jugador,puntos_maquina,window,letras_maquina,valores_de_letras,cant_letras):

    """Se ejecuta luego de que termina el tiempo o se terminan las fichas. Muestra las fichas que le quedaron al jugador
        y a la maquina y lo que van a restar del puntaje obtenido por la formación de palabras."""

    def calcularResta(lista_letras, valores_de_letras):

        """Calcula puntos a restar para obtener el puntaje final"""

        puntaje_restar = 0
        for letra in lista_letras:
            puntaje_restar+= valores_de_letras[letra]
        return puntaje_restar
    letras_atril = []

    for i in range(cant_letras):
        if window[i].GetText() != '---':
            letras_atril.append(window[i].GetText())

    resta_jugador = calcularResta(letras_atril,valores_de_letras)
    resta_maquina = calcularResta(letras_maquina,valores_de_letras)

    layout_atril_jugador = [[sg.Text('Tus letras')], [sg.Button(tomar_y_borrar(letras_atril), key = j, size=(4, 2), pad=(21.5,0)) for j in range(len(letras_atril))],
                            [sg.Text('Puntaje a restar : ' + str(resta_jugador))]]
    layout_atril_maquina = [[sg.Text('Letras de PC')],[sg.Button(tomar_y_borrar(letras_maquina), key = j, size=(4, 2), pad=(21.5,0)) for j in range(len(letras_maquina))],
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
                perder_empatar(total_jugador,total_maquina,'¡Perdiste!')
                break
            else:
                window_final.close()
                perder_empatar(total_jugador,total_maquina,'¡Empate!')
                break