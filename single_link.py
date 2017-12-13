import sys
import numpy as np
import scipy.sparse as ss
from collections import deque

def main():
    particoes, identificador = le_arquivo(sys.argv[1])
    kMin = int(sys.argv[2])
    kMax = int(sys.argv[3])

    tam_matriz = qtd_particoes(sys.argv[1])
    iteracoes = tam_matriz - kMax
    matriz = cria_matriz_inicial(particoes, tam_matriz)

    print("-----------MATRIZ INICIAL---------\n{}\n".format(matriz))
    for i in range(0, 5):
        print("\nITERAÇÃO {}".format(i))
        minimo, x, y = acha_minimo(matriz, tam_matriz)
        # descarta o primeiro mínimo
        matriz[x][y] = 0
        matriz = merge(x, y, matriz, tam_matriz)
        # exclui primeira coluna
        matriz = np.delete(matriz, 0, 1)
        tam_matriz -= 1
        print("A menor distância é entre os clusters {} e {}, com mínimo igual a {}".format(identificador[x], identificador[y], minimo))
        if(x > y):
            # adiciona x ao cluster de y
            identificador[y] = str(identificador[y]) + ", " + str(identificador[x])
            del identificador[x]
            print(identificador)
        else:
            # adiciona y ao cluster de x
            identificador[x] = str(identificador[x]) + ", " + str(identificador[y])
            del identificador[y]
            print(identificador)
        print(matriz)

def le_arquivo(dataset):
    nlinhas = qtd_particoes(dataset)
    particoes = np.zeros((nlinhas, 2))
    identificador = []

    try:
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
    except EnvironmentError as erro:
        print("Verifique se os parâmetros do seu arquivo estão separados por tabs.")
        print(erro)
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
    minimo  : int
        primeira distância mínima
    """
    matriz = np.zeros((tam_matriz, tam_matriz))
    for linha in range(0, tam_matriz):
        for coluna in range(linha+1, tam_matriz):
            matriz[linha][coluna] = dist(particoes[linha][0], particoes[coluna][0], particoes[linha][1], particoes[coluna][1])
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
    pos_x = 0
    pos_y = 1
    minimo = matriz[0][0]
    for i in range(0, tam_matriz):
        if(matriz[0][i] != 0):
            minimo = matriz[0][i]

    for linha in range(0, tam_matriz):
        # dá pra manter esse for pq agora a matriz continua triangular
        for coluna in range(linha+1, tam_matriz):
        #for coluna in range(0, tam_matriz):
            if(matriz[linha, coluna] < minimo and matriz[linha, coluna]> 0):
                minimo = matriz[linha][coluna]
                pos_x = linha
                pos_y = coluna
    return minimo, pos_x, pos_y;

def merge(cA, cB, matriz, tam_matriz):
    """
    Faz o merge entre os clusters de menor distância euclidiana
    """

    for i in range(0, tam_matriz):
        #print("cA: {}".format(matriz[cA][i]))
        #print("cB: {}".format(matriz[cB][i]))
        # checar coluna
        if(matriz[cA][i] > 0 and matriz[cB][i] > 0 and matriz[cA][i] <= matriz[cB][i]):
            matriz[cB][i] = 0
        elif(matriz[cA][i] > matriz[cB][i] and matriz[cB][i] > 0):
            matriz[cA][i] = matriz[cB][i]
            matriz[cB][i] = 0
        else:
            pass
    matriz = np.delete(matriz, cB, axis=0)
    return matriz

if __name__ == '__main__':
    main()
