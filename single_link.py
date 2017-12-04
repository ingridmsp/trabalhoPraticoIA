import sys
import numpy as np
import scipy as sp

def main():
    particoes, identificador = le_arquivo(sys.argv[1])
    # colocar validações?????
    kMin = int(sys.argv[2])
    kMax = int(sys.argv[3])

    tam_matriz = qtd_particoes(dataset)
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
            identificador.append(parametros[0])
            particoes[i,0] = float(parametros[1])
            particoes[i,1] = float(parametros[2])
            i += 1
    dataset.close()
    return particoes, identificador

def qtd_particoes(dataset):
    with open(dataset) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def cria_matriz_inicial(particoes, tam_matriz):
    matriz = np.zeros(tam_matriz, tam_matriz)
    for linha in range(0, tam_matriz):
        # diagonal
        matriz[i][i] = 0
        # tem alguma coisa errada aqui
        for coluna in range(0, tam_matriz):
            if(coluna >= linha):
                matriz[i][j] = dist(particoes[0], particoes[1])




if __name__ == '__main__':
    main()
