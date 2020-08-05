import simpleaudio as sa

def s_perdedor():
    
    """Ejecuta sonido perder.wav"""
    
    try:
        perder_obj = sa.WaveObject.from_wave_file('Sonidos/perder.wav')
        perder_play = perder_obj.play()
    except:
        pass

def s_ganador():
    
    """Ejecuta sonido ganar.wav"""
    
    try:
        ganar_obj = sa.WaveObject.from_wave_file('Sonidos/ganar.wav')
        ganar_play = ganar_obj.play()      
    except:
        pass
    else:
        return ganar_play
        
def s_menu():
    
    """Ejecuta sonido menu.wav"""
    
    try:
        menu_obj = sa.WaveObject.from_wave_file('Sonidos/menu.wav')
        menu_play = menu_obj.play()      
    except:
        pass
    else:
        return menu_play

def s_valida():
    
    """Ejecuta sonido valida.wav"""
    
    try:
        valida_obj = sa.WaveObject.from_wave_file('Sonidos/valida.wav')
        valida_play = valida_obj.play() 
    except:
        pass

def s_invalida():
    
    """Ejecuta sonido invalida.wav"""
    
    try:
        invalida_obj = sa.WaveObject.from_wave_file('Sonidos/invalida.wav')
        invalida_play = invalida_obj.play() 
    except:
        pass

def s_boton():
    
    """Ejecuta sonido boton.wav"""
    
    try:
        boton_obj = sa.WaveObject.from_wave_file('Sonidos/boton.wav')
        boton_play = boton_obj.play() 
    except:
        pass
