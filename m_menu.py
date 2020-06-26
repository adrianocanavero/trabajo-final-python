import PySimpleGUI as sg

def menu():

    """Genera la ventana del menu principal"""

    hay_partida_guardada = True
    
    try:
        archivo_save = open('savewindow.pickle', 'rb')
        archivo_save.close()
        archivo_save = open('datos_usuario.pickle', 'rb')
        archivo_save.close()
    except EOFError: ## si no hay save, no tendria porque haber problema
        hay_partida_guardada = False
    except FileNotFoundError:
        hay_partida_guardada = False
            
    if hay_partida_guardada:
        layout = [[sg.Button('Nueva partida',size =(10,5)), sg.Button('Cargar partida',size =(10,5)), sg.Button('Configurar',size =(10,5)), sg.Button('Top ten\npuntajes',size =(10,5)),sg.Button('Salir',size =(10,5))]]
    else:
        layout = [[sg.Button('Nueva partida',size =(10,5)), sg.Button('Configurar',size =(10,5)), sg.Button('Top ten\npuntajes',size =(10,5)),sg.Button('Salir',size =(10,5))]]
    window = sg.Window('Menú principal',layout)
    event, values = window.read()
    window.close()
    return event

def top_puntajes():

    """Genera la ventana para el top de puntajes"""

    try:
        archivo_topten = open('top_ten.txt', 'r')
        lista_topten = []
        for linea in archivo_topten:
            lista_topten.append(linea.strip('\n'))
    except EOFError: 
        lista_topten = []
    except FileNotFoundError:
        lista_topten = []
    
    top_layout = [[sg.Text('Top 10 Scrabble AR', justification='center', font = 'Any 14')],
                    [sg.Listbox(lista_topten, font = 'Any 12', size = (20,20))],
                    [sg.Button('Salir')]]
    top_window = sg.Window('Top 10',top_layout)

    while True:
        e,v = top_window.read()
        if e in (None,'Salir'):
            break
    top_window.close()