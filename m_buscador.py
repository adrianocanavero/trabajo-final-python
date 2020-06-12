from pattern.es import tag

import pickle

archivo_palabras = open('lista_palabras_arg.pickle', 'rb')
lista_palabras = pickle.load(archivo_palabras)
archivo_palabras.close()
archivo_verbos = open('lista_verbos_sin_acento.pickle', 'rb')
lista_verbos = pickle.load(archivo_verbos)
archivo_verbos.close()


def clasificar(palabra):
	t = tag(palabra, tokenize=True, encoding='utf-8')
	print('tag: ',t[0][1]) # ver VB JJ o NN
	if 'NN' in t[0][1]: # tag devuelve una lista con una tupla ('palabra', 'tipo') asi que entre a la pos 0 de la lista y directamente al tipo que esta en la pos 1 de la tupla.
		print('Es sustantivo')
		return True
	elif 'JJ' in t[0][1]:
		print('Es adjetivo')
		return True
	elif 'VB' in t[0][1]:
		print('Es verbo')
		return True
	else:
		print('no es verbo ni adjetivo ni sustantivo')
		return False

def buscar_palabra(palabra):
	
	print('Buscar ' + palabra + ' verbos')
	if not palabra.lower() in lista_verbos:	
		print('busco en es_AR')
		if not palabra.lower() in lista_palabras:
			print('no se encontro en es_AR')
			return False
		else:
			print('la encontre en es_AR')
			return clasificar(palabra)
	else:
		print('la encontro en verbos')
		return True
