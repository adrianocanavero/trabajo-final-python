from pattern.es import tag
import sys
import PySimpleGUI as sg
import pickle

try:
	archivo_palabras = open('Pickles/lista_palabras_arg.pickle', 'rb')
	lista_palabras = pickle.load(archivo_palabras)
	archivo_palabras.close()
	archivo_verbos = open('Pickles/lista_verbos_sin_acento.pickle', 'rb')
	lista_verbos = pickle.load(archivo_verbos)
	archivo_verbos.close()
except FileNotFoundError: #Manejo de excepcion por si falta un modulo del juego.
    layoutERROR = [[sg.Text('Faltan archivos de palabras. Descárguese ScrabbleAR nuevamente',font= 'Any 10', justification='center')],
                    [sg.Button('Salir', button_color=('white', '#52313a'))]]
    window = sg.Window('Error', layoutERROR)
    while True:
        e,v = window.read()
        if e in('Salir', None):
            break
    window.close()
    sys.exit()
	


def clasificar(palabra,nivel):

	"""Usando pattern retorna si la palabra es sustantivo o es adjetivo"""
    
	if nivel == 'facil':
		t = tag(palabra, tokenize=True, encoding='utf-8')
		# print('tag: ',t[0][1]) # ver VB JJ o NN
		if 'NN' in t[0][1]: # tag devuelve una lista con una tupla ('palabra', 'tipo') asi que entre a la pos 0 de la lista y directamente al tipo que esta en la pos 1 de la tupla.
			#print('Es sustantivo')
			return True
		elif 'JJ' in t[0][1]:
			#print('Es adjetivo')
			return True
		elif 'VB' in t[0][1]:
			#print('Es verbo')
			return True
		else:
			#print('no es verbo ni adjetivo ni sustantivo')
			return False
	else: # si es medio o dificil, valida solo adjetivos o verbos.
		t = tag(palabra, tokenize=True, encoding='utf-8')
		#print('tag: ',t[0][1]) # ver VB JJ o NN
		if 'JJ' in t[0][1]:
			#print('Es adjetivo')
			return True
		elif 'VB' in t[0][1]:
			#print('Es verbo')
			return True
		else:
			#print('no es verbo ni adjetivo')
			return False

def buscar_palabra(palabra,nivel):

	"""Busca la palabra primero en la lista de verbos en pattern. Si la encuentra ahi,
		devuelve directamente True. Si no, busca en la lista de palabras armada y
		manda a la funcion clasificar"""
	
	#print('Buscar ' + palabra + ' verbos')
	if not palabra.lower() in lista_verbos:	
		#print('busco en es_AR')
		if not palabra.lower() in lista_palabras:
			#print('no se encontro en es_AR')
			return False
		else:
			#print('la encontre en es_AR')
			return clasificar(palabra,nivel)
	else:
		#print('la encontro en verbos')
		return True
