import simpleaudio as sa

def s_perdedor():
    try:
        perder_obj = sa.WaveObject.from_wave_file('Sonidos/perder.wav')
        perder_play = perder_obj.play()
    except:
        pass

def s_ganador():
    try:
        ganar_obj = sa.WaveObject.from_wave_file('Sonidos/ganar.wav')
        ganar_play = ganar_obj.play()      
    except:
        pass
    else:
        return ganar_play
def s_menu():
    try:
        menu_obj = sa.WaveObject.from_wave_file('Sonidos/menu.wav')
        menu_play = menu_obj.play()      
    except:
        pass
    else:
        return menu_play


def s_valida():
    try:
        valida_obj = sa.WaveObject.from_wave_file('Sonidos/valida.wav')
        valida_play = valida_obj.play() 
    except:
        pass

def s_invalida():
    try:
        invalida_obj = sa.WaveObject.from_wave_file('Sonidos/invalida.wav')
        invalida_play = invalida_obj.play() 
    except:
        pass

def s_boton():
    try:
        boton_obj = sa.WaveObject.from_wave_file('Sonidos/boton.wav')
        boton_play = boton_obj.play() 
    except:
        pass