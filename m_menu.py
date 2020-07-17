import PySimpleGUI as sg

def menu():

    """Genera la ventana del menu principal"""

    hay_partida_guardada = True
    
    try:
        archivo_save = open('savewindow.pickle', 'rb')
        archivo_save.close()
        archivo_save = open('datos_usuario.pickle', 'rb')
        archivo_save.close()
    except FileNotFoundError: # Se comprueba si hay una partida guardada
        hay_partida_guardada = False
            
    # Solo si hay una partida guardada se muestra la opción "Cargar partida"
    if hay_partida_guardada:
        layout = [[sg.Button('Nueva partida',size =(10,5)), sg.Button('Cargar partida',size =(10,5)), sg.Button('Configurar',size =(10,5)),
            sg.Button('Top ten\npuntajes',size =(10,5)),sg.Button('Salir',size =(10,5))]]
    else:
        layout = [[sg.Button('Nueva partida',size =(10,5)), sg.Button('Configurar',size =(10,5)), sg.Button('Top ten\npuntajes',size =(10,5)),sg.Button('Salir',size =(10,5))]]
    window = sg.Window('Menú principal',layout)
    event, values = window.read()
    window.close()
    return event
