import PySimpleGUI as sg

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
