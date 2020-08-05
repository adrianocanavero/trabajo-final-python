import os
import platform
def crear_carpeta():
    
    """Si no existe la carpeta "Archivos locales" la crea, sino no hace nada.
        En este carpeta se guardan los archivos necesarios para cargar una
        partida y el top ten"""
    
    try:
        if platform.system() == 'Linux':
            os.mkdir(os.getcwd() + "/Archivos locales")
        else:
            os.mkdir(os.getcwd()+"\Archivos locales")
    except OSError:
        pass
