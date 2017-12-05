import sys
import numpy as np
import scipy.sparse as ss

def main():
    particoes, identificador = le_arquivo(sys.argv[1])
    kMin = int(sys.argv[2])
    kMax = int(sys.argv[3])

    tam_matriz = qtd_particoes(sys.argv[1])
    matriz = cria_matriz_inicial(particoes, tam_matriz)
    #print(matriz)
    minimo, teste_x, teste_y = acha_minimo(matriz, tam_matriz)
    print("A menor distância é entre os clusters {} e {}".format(identificador[teste_x], identificador[teste_y]))
    print("teste linha matriz pro cluster {}: {}".format( identificador[teste_x], matriz[teste_x][:]))
    print("teste linha matriz pro cluster {}: {}".format( identificador[teste_y], matriz[teste_y][:]))


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
    Retorna uma matriz esparsa pra tentar melhorar um pouquinho esse lixo que é a complexidade desse algoritmo.
    Parâmetros
    ----------
    particoes   :   array
        array com as posições x e y de cada elemento
    tam_matriz  :   int
        inteiro com a quantidade de particoes
    Retorno
    -------
    matriz_esparsa  :   lil_matrix
        matriz esparsa com todas as distâncias calculadas
    minimo  : int
        primeira distância mínima
    """
    matriz = np.zeros((tam_matriz, tam_matriz))
    for linha in range(0, tam_matriz):
        for coluna in range(linha+1, tam_matriz):
            matriz[linha][coluna] = dist(particoes[linha][0], particoes[coluna][0], particoes[linha][1], particoes[coluna][1])
   # matriz_esparsa = ss.lil_matrix(matriz)
   # return matriz_esparsa
    return matriz

def dist(x0, x1, y0, y1):
    """
    Calcula a distância euclidiana entre os pontos
    """
    return np.sqrt((x1 - x0)**2 + (y1 - y0)**2)


def acha_minimo(matriz, tam_matriz):
    """
    Acha o mínimo da matriz desconsiderando diagonais
    """
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

def merge(cA, cB, matriz):
    """
    Faz o merge entre os clusters de menor distância euclidiana
    """

    #comparar matriz[cA][:] c/ matriz[cB][:] e manter quem for menor

    return "nada acontece feijoada"

if __name__ == '__main__':
    main()
