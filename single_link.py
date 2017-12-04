import sys
import numpy as np
import scipy as sp

def main():
    particoes, identificador = le_arquivo(sys.argv[1])
    kMin = int(sys.argv[2])
    kMax = int(sys.argv[3])

    tam_matriz = qtd_particoes(sys.argv[1])
    cria_matriz_inicial(particoes, tam_matriz)

def le_arquivo(dataset):
    nlinhas = qtd_particoes(dataset) - 1
    particoes = np.zeros((nlinhas, 2))
    identificador = []

    with open(dataset) as f:
        next(f)
        i = 0
        for linha in f:
            parametros = linha.replace('\n', '').split('\t')
            #print("Parâmetros: {}".format(parametros))
            identificador.append(parametros[0])
            particoes[i,0] = float(parametros[1])
            particoes[i,1] = float(parametros[2])
            if(i == nlinhas - 1):
                break
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
    for linha in range(0, tam_matriz-1):
        matriz[linha][linha] = 0

        for coluna in range(0, tam_matriz-1):
            if(coluna >= linha and linha > 0):
                matriz[linha][coluna] = dist(particoes[linha-1][0], particoes[linha][0], particoes[linha-1][1], particoes[linha][1])
    return matriz

# conferir o RuntimeWarning
def dist(x0, x1, y0, y1):
    print(np.sqrt((x1 - x0) + (y1 - y0)))
    return np.sqrt((x1 - x0) + (y1 - y0))



if __name__ == '__main__':
    main()
