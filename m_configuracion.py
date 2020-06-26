import PySimpleGUI as sg

def configurar():
    
    """Genera la ventana del menu de configuración"""
    
    layout = [[sg.Button('Configurar el tiempo',size =(10,5)), sg.Button('Configurar el nivel',size =(10,5)), sg.Button('Configurar el\npuntaje de\ncada ficha',size =(10,5)),
    sg.Button('Configurar la cantidad de fichas por\nletra',size =(10,5))]]
    window = sg.Window('Menú de configuración',layout)
    event, values = window.read()
    window.close()
