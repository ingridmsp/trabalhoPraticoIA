import sys
import numpy as np
import scipy.sparse as ss

def main():
    particoes, identificador = le_arquivo(sys.argv[1])
    kMin = int(sys.argv[2])
    kMax = int(sys.argv[3])

    tam_matriz = qtd_particoes(sys.argv[1])
    matriz = cria_matriz_inicial(particoes, tam_matriz)
    dists = cria_vetor_dists(particoes, tam_matriz)
    print(dists)
    #print(matriz)

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
    """
    Cria a matriz triangular de distâncias entre todos os pontos da entrada.
    """
    matriz = np.zeros((tam_matriz, tam_matriz))
    for linha in range(0, tam_matriz):
        matriz[linha][linha] = 0

        for coluna in range(0, tam_matriz):
            if(coluna > linha):
                matriz[linha][coluna] = dist(particoes[linha][0], particoes[coluna][0], particoes[linha][1], particoes[coluna][1])

    matriz_esparsa = ss.lil_matrix(matriz)
    return matriz_esparsa

# conferir o RuntimeWarning
def dist(x0, x1, y0, y1):
    return np.sqrt((x1 - x0)**2 + (y1 - y0)**2)


def cria_vetor_dists(particoes, tam_matriz):
    """
    Cria vetor ordenado de distâncias.
    """
    #tam_vet = (tam_matriz**2/2)-tam_matriz

    dists = []
    for linha in range(0, tam_matriz):
        for coluna in range(0, tam_matriz):
            if(coluna > linha):
                dists.append(dist(particoes[linha][0], particoes[coluna][0], particoes[linha][1], particoes[coluna][1]))
    npdists = np.asarray(dists)

    # falta ordernar o vetor e ordenar os identificadores ao mesmo tempo de uma maneira minimamente decente

    return npdists

def sorting(vet_dist, identificadores):
    return "essa função vai ser burra"


if __name__ == '__main__':
    main()
