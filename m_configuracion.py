import PySimpleGUI as sg
from m_fichas import valores_letras

def configurar():
    
    """Genera la ventana del menu de configuración"""
    
    abecedario_sin_espacio = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    
    # Está hecho así para que se vea alineado con los sliders
    abecedario_con_espacio = ['     A','     B','     C','     D','     E','     F','     G','     H','      I','      J','     K','     L','     M',
        '     N','     Ñ','     O','     P','     Q','     R','     S','     T','     U','     V','    W','     X','      Y','     Z']
    
    layout = [[sg.Text('Configurar el tiempo',pad=(507,0))],
        [sg.Text(pad=(140,0)),sg.Slider(range=(1,240), orientation='h', size=(64,20), default_value=60)],
        [sg.Text()], # Genera espacio. En este caso queda mejor generar el espacio de esta forma que con el segundo valor de pad en el elemento de arriba o abajo
        [sg.Text('Configurar el nivel',pad=(513,0))],
        [sg.Text(pad=(231,0)),sg.Radio('Fácil', "nivel"),sg.Radio('Medio', "nivel", default=True),sg.Radio('Difícil', "nivel")],
        [sg.Text()], # Genera espacio. En este caso queda mejor generar el espacio de esta forma que con el segundo valor de pad en el elemento de arriba o abajo
        [sg.Text('Configurar el puntaje de cada ficha',pad=(468,0))],                         # Por defecto cada letra tiene el valor establecido por valores_letras en m_fichas
        [sg.Text(letra) for letra in abecedario_con_espacio],[sg.Slider(range=(1,20), orientation='v', size=(5,15), default_value=valores_letras[letra]) for letra in abecedario_sin_espacio],
        [sg.Text()], # Genera espacio. En este caso queda mejor generar el espacio de esta forma que con el segundo valor de pad en el elemento de arriba o abajo
        [sg.Text('Configurar la cantidad total de fichas por letra',pad=(440,0))],
        [sg.Text(letra) for letra in abecedario_con_espacio],[crear_slider(letra) for letra in abecedario_sin_espacio], # Por defecto cada letra tiene la cantidad que está en creando_letras en ScrabbleAR
        [sg.Text(pad=(231,0)),sg.Button('Atrás',size=(8, 2),pad=(20,15)),sg.Button('Aceptar',size=(8, 2))]]
    window = sg.Window('Menú de configuración',layout)
    event, values = window.read()
    window.close()
    if event == "Aceptar":
        return crear_diccionario_con_configuracion(values,abecedario_sin_espacio)

def crear_slider(letra):
    
    """Dependiendo del valor de letra devuelve un slider con el valor por defecto correspondiente"""
    
    if letra in ["A","E"]:
        return sg.Slider(range=(1,20), orientation='v', size=(5,15), default_value=11)
    elif letra in ["B","M"]:
        return sg.Slider(range=(1,20), orientation='v', size=(5,15), default_value=3)
    elif letra in ["C","D","L","R","T"]:
        return sg.Slider(range=(1,20), orientation='v', size=(5,15), default_value=4)
    elif letra in ["F","G","H","J","K","Ñ","P","Q","V","W","Y"]:
        return sg.Slider(range=(1,20), orientation='v', size=(5,15), default_value=2)
    elif letra in ["I","U"]:
        return sg.Slider(range=(1,20), orientation='v', size=(5,15), default_value=6)
    elif letra in ["N"]:
        return sg.Slider(range=(1,20), orientation='v', size=(5,15), default_value=5)
    elif letra in ["O"]:
        return sg.Slider(range=(1,20), orientation='v', size=(5,15), default_value=8)
    elif letra in ["S"]:
        return sg.Slider(range=(1,20), orientation='v', size=(5,15), default_value=7)
    else:
        return sg.Slider(range=(1,20), orientation='v', size=(5,15), default_value=1)
        
def crear_diccionario_con_configuracion(values,abecedario_sin_espacio):
    
    """Devuelve un diccionario con el tiempo, el nivel, el puntaje y la cantidad de fichas elegidas"""
    
    retornar = {}
    retornar["tiempo"] = int(values[0])
    for i in range(1,4):
        if values[i] == True:
            if i == 1:
                retornar["nivel"] = "facil"
            elif i == 2:
                retornar["nivel"] = "medio"
            else:
                retornar["nivel"] = "dificil"
    puntajes_fichas = {}
    for i in range(4,31):
        puntajes_fichas[abecedario_sin_espacio[i-4]] = int(values[i])
    retornar["puntaje fichas"] = puntajes_fichas
    cantidad_fichas = {}
    for i in range(31,58):
        cantidad_fichas[abecedario_sin_espacio[i-31]] = int(values[i])
    retornar["cantidad fichas"] = cantidad_fichas
    return retornar
