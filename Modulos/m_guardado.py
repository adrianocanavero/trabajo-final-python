import pickle
import Modulos.m_tablero as m_tablero
import Modulos.m_maquina as m_maquina
from Modulos.m_carpeta import crear_carpeta

def guardar(save,lugares_usados_total,lugares_usados_temp,window,pos_atril_usadas,nivel,bolsa_letras,letras_ingresadas,palabra,
    backup_text,horizontal,vertical,puntos_jugador,puntos_maquina,Letras,tiempo_actual,TIEMPO,valores_de_letras,veces_cambiadas,cambios_maquina,cant_letras):
    
    """Guarda la información de la partida si el jugador elige Posponer. En save se encuentra la informacion del tablero,
        mientras que en datos_usuario estan los datos indispensables que necesita el juego para realizar sus funciones"""

    for i in range (cant_letras):
        save[i] = window[i].GetText()
    save['timer'] = tiempo_actual
    crear_carpeta() # Si la carpeta "Archivos locales" no existe la crea, sino no hace nada
    archivo_save = open('Archivos locales/savewindow.pickle', 'wb')
    pickle.dump(save,archivo_save)
    archivo_save.close()
    archivo_save = open('Archivos locales/datos_usuario.pickle', 'wb')
    datos_usuario ={'lug_tot': lugares_usados_total,
                    'lug_temp':lugares_usados_temp,
                    'pos_at': pos_atril_usadas,
                    'let_ing': letras_ingresadas,
                    'pal': palabra,
                    'back_txt': backup_text,
                    'hor': horizontal,
                    'ver': vertical,
                    'letras': Letras, 
                    'pj': puntos_jugador,
                    'pm': puntos_maquina,
                    'pos_jug': m_tablero.posicion_jugador,
                    'pos_maq': m_tablero.posicion_maquina,
                    'atril_maq': m_maquina.letras_de_maquina,
                    'nivel': nivel,
                    'timer_total': TIEMPO,
                    'valores_letras': valores_de_letras,
                    'cantidad_letras': bolsa_letras,
                    'cambios': veces_cambiadas,
                    'cambios_mq':cambios_maquina
                    }
    pickle.dump(datos_usuario,archivo_save)
    archivo_save.close()

def inicializar_variables(save_window,datos_usuario):

    """Inicializa variables del juego con los datos del guardado"""

    save = save_window # si hay save se pone en save lo que hay en verificar_guardado.
    lugares_usados_temp = datos_usuario['lug_temp']
    lugares_usados_total = datos_usuario['lug_tot']
    vertical = datos_usuario['ver']
    horizontal = datos_usuario['hor']
    letras_ingresadas = datos_usuario['let_ing']
    backup_text = datos_usuario['back_txt']
    palabra = datos_usuario['pal']
    pos_atril_usadas = datos_usuario['pos_at'] 
    Letras = datos_usuario['letras']
    puntos_jugador = datos_usuario['pj']
    puntos_maquina = datos_usuario['pm']
    m_tablero.posicion_maquina = datos_usuario['pos_maq']
    m_tablero.posicion_jugador = datos_usuario['pos_jug']
    m_maquina.letras_de_maquina = datos_usuario['atril_maq']
    turno_jugador = True # si se carga la partida siempre es el turno del jugador.
    tiempo_actual = save['timer']
    tiempo = datos_usuario['timer_total']
    valores_de_letras = datos_usuario['valores_letras']
    veces_cambiadas = datos_usuario['cambios']
    cambios_maquina = datos_usuario['cambios_mq']
    return save,lugares_usados_temp,lugares_usados_total,vertical,horizontal,letras_ingresadas, \
        backup_text,palabra,pos_atril_usadas,Letras,puntos_jugador,puntos_maquina,turno_jugador, \
        tiempo_actual,tiempo,valores_de_letras,veces_cambiadas,cambios_maquina

def abrir_guardado():

    """Abre el archivo de guardado y carga los datos en variables"""

    crear_carpeta() # Si la carpeta "Archivos locales" no existe la crea, sino no hace nada
    archivo_save = open('Archivos locales/savewindow.pickle', 'rb')
    save_window = pickle.load(archivo_save) # aca se guarda para actualizar el tablero
    archivo_save.close()
    archivo_save = open('Archivos locales/datos_usuario.pickle', 'rb')
    datos_usuario = pickle.load(archivo_save) # aca se guarda los datos del usuario
    archivo_save.close()
    nivel = datos_usuario['nivel']
    bolsa_letras = datos_usuario["cantidad_letras"]
    return save_window,datos_usuario,nivel,bolsa_letras
