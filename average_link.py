import sys
import numpy as np

def main():
	np.set_printoptions(threshold='nan')

	particoes, identificador = le_arquivo(sys.argv[1])
	#print particoes
	kMin = int(sys.argv[2])
	kMax = int(sys.argv[3])

	tam_matriz = qtd_particoes(sys.argv[1]) 
	matriz = cria_matriz_inicial(particoes, tam_matriz)
	print(matriz)
	
	clu = 0
	clusters = np.zeros(tam_matriz, 2)
	media(matriz, tam_matriz, particoes, identificador, clusters, clu)
	

def le_arquivo(dataset):
	nlinhas = qtd_particoes(dataset)
	particoes = np.zeros((nlinhas, 2))
	identificador = []

	with open(dataset) as f:
		next(f)
		i = 0
		for linha in f:
			parametros = linha.replace('\n', '').split('\t')
			identificador.append(parametros[0])
			if(i == nlinhas - 1):
				break
			particoes[i,0] = float(parametros[1])
			particoes[i,1] = float(parametros[2])
			i += 1
	f.close()
	return particoes, identificador

def qtd_particoes(dataset):
	with open(dataset) as f:
		for i, l in enumerate(f):
			pass
	return i

def cria_matriz_inicial(particoes, tam_matriz):
	matriz = np.zeros((tam_matriz, tam_matriz))
	for linha in range(0, tam_matriz):
		for coluna in range(0, tam_matriz):
			if(linha == coluna):
				matriz[linha][coluna] = 0
			elif(linha > coluna):
				matriz[linha][coluna] = matriz[coluna][linha]
			else:
				matriz[linha][coluna] = dist(particoes[linha][0], particoes[coluna][0], particoes[linha][1], particoes[coluna][1])
			
	return matriz

def dist(x0, x1, y0, y1):
	""" Calcula a distancia euclidiana entre os pontos """
	return np.sqrt((x1 - x0)**2 + (y1 - y0)**2)


def acha_minimo(matriz, tam_matriz):
	""" Acha o minimo da matriz desconsiderando diagonais """
	minimo = matriz[0, 1]
	pos_x = 0
	pos_y = 1
	for linha in range(0, tam_matriz):
		for coluna in range(linha+1, tam_matriz):
			if(matriz[linha, coluna] < minimo):
				minimo = matriz[linha, coluna]
				pos_x = linha
				pos_y = coluna
	return minimo, pos_x, pos_y;
	
def media(matriz, tam_matriz, particoes, identificador, clusters, clu):

	minimo, posx, posy = acha_minimo(matriz, tam_matriz)
	merge(posx, posy, matriz, particoes, clusters, clu)
	
	

def merge(posx, posy, matriz, particoes, clusters, clu):
	
	if(clusters[posx] == 0 and clusters[posy] == 0):
		clu = clu + 1
		clusters[posx, 0] = clu
		clusters[posx, 1] = 2
		clusters[posy, 0] = clu
		clusters[posy, 1] = 2
		
		recalcula_media(posx, posy, particoes, matriz, clusters, clu)
		
	elif(clusters[posx] != 0 and clusters[posy] == 0):
		a = 0
		

	return "nada acontece feijoada"
	
def recalcula_media(posx, posy, particoes, matriz, clusters, clu)
	#d(a,bc) = (d(a,b)X|b| + d(a,c)X|c|) / |b|+|c|

	matriz[posx][posy] = 0
	matriz[posy][posx] = 0

	for linha in (0, tam_matriz):
		dist = 0
		for i in clusters[posx][1]
			distancia = distancia + dist(particoes[posx][0], particoes[linha][0], particoes[posx][1], particoes[linha][1])
			
		
		matriz[linha][posx] = 
			
			





if __name__ == '__main__':
    main()
