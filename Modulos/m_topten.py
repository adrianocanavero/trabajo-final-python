import PySimpleGUI as sg
import pickle
from collections import OrderedDict

def top_puntajes():

    """Genera la ventana para el top de puntajes"""

    try:
        archivo_topten = open('Archivos locales/top_ten.pickle', 'rb')
        lista_topten = []
        dic_top = pickle.load(archivo_topten)
        top_ordenado = OrderedDict(sorted(dic_top.items(), key=lambda x: x[1],reverse =True))
        for tupla in top_ordenado.items():
            lista_topten.append(str(tupla[0]) + ':' + str(tupla[1]))
    except FileNotFoundError: # Se comprueba si hay un top ten guardado
        lista_topten = []
    
    top_layout = [[sg.Text('Top 10 ScrabbleAR', justification='center', font = 'Any 14')],
        [sg.Listbox(lista_topten, font = 'Any 12', size = (20,20))],
        [sg.Button('Salir', button_color=('white', '#52313a'))]]
    top_window = sg.Window('Top 10',top_layout)

    while True:
        e,v = top_window.read()
        if e in (None,'Salir'):
            break
    top_window.close()
