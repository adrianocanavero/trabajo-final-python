import pygame,time

from pygame import mixer

mixer.init(48000, -16, 2, 1024)

def s_perdedor():

    """Ejecuta sonido perder.wav"""

    try:
        wavperder = mixer.Sound('Sonidos/perder.wav')
        wavperder.play()
    except:
        pass

def s_ganador():

    """Ejecuta sonido ganar.wav"""

    try:
        wavganar = mixer.Sound('Sonidos/ganar.wav')
        wavganar.play()    
    except:
        pass
    else:
        return wavganar

def s_menu():

    """Ejecuta sonido menu.wav"""

    try:
        wavmenu = mixer.Sound('Sonidos/menu.wav')
        wavmenu.play()        
    except:
        pass
    else:
        return wavmenu  

def s_valida():

    """Ejecuta sonido valida.wav"""

    try:
        wavvalida = mixer.Sound('Sonidos/valida.wav')
        wavvalida.play()  
    except:
        pass

def s_invalida():

    """Ejecuta sonido invalida.wav"""

    try:
        wavinvalida = mixer.Sound('Sonidos/invalida.wav')
        wavinvalida.play()  
    except:
        pass

def s_boton():

    """Ejecuta sonido boton.wav"""
    
    try:
        wavboton = mixer.Sound('Sonidos/boton.wav')
        wavboton.play()  
    except:
        pass
