import sys
import numpy as np
from datetime import datetime

def main():
    startTime = datetime.now()
    particoes, identificador = le_arquivo(sys.argv[1])
    kMin = int(sys.argv[2])
    kMax = int(sys.argv[3])

    tam_matriz = qtd_particoes(sys.argv[1])
    iteracoes = tam_matriz - kMin
    matriz = cria_matriz_inicial(particoes, tam_matriz)

    for i in range(0, iteracoes):
        minimo, x, y = acha_minimo(matriz, tam_matriz)
        matriz = merge(x, y, matriz, tam_matriz)
        matriz = np.delete(matriz, y, 1)
        tam_matriz -= 1
        if(x > y):
            # adiciona x ao cluster de y
            identificador[y] = str(identificador[y]) + "," + str(identificador[x])
            del identificador[x]
        else:
            # adiciona y ao cluster de x
            identificador[x] = str(identificador[x]) + "," + str(identificador[y])
            del identificador[y]
        print(matriz)

        if(tam_matriz <= kMax):
            escreve_arquivo(identificador, tam_matriz)
    print("Tempo de execução: {}".format(datetime.now()-startTime))

def le_arquivo(dataset):
    nlinhas = qtd_particoes(dataset)
    particoes = np.zeros((nlinhas, 2))
    identificador = []

    with open(dataset, 'r') as f:
        next(f)
        i = 0
        for linha in f:
            parametros = linha.replace('\n', '').split('\t')
            identificador.append(parametros[0])
            if(i == nlinhas - 1):
                break
            try:
                particoes[i,0] = float(parametros[1])
                particoes[i,1] = float(parametros[2])
                i += 1
            except Exception as erro:
                print("Erro de índice. Verifique se os parâmetros do seu arquivo estão separados por tabs.")
                break
    f.close()
    return particoes, identificador

def qtd_particoes(dataset):
    with open(dataset) as f:
        for i, l in enumerate(f):
            pass
    return i

def cria_matriz_inicial(particoes, tam_matriz):
    """
    Cria a matriz triangular superior de distâncias entre todos os pontos da entrada.
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
    e valores zerados
    """
    minimo = np.amin(matriz[np.nonzero(matriz > 0)])

    idx_pos = np.argwhere(matriz == minimo)
    pos_x = idx_pos[0][0]
    pos_y = idx_pos[0][1]

    return minimo, pos_x, pos_y;

def merge(cA, cB, matriz, tam_matriz):
    """
    Faz o merge entre os clusters de menor distância euclidiana
    """

    for i in range(0, tam_matriz):
        # as duas linhas tiverem valores válidos
        if(matriz[cA][i] > 0 and matriz[cB][i] > 0):
            if(matriz[cA][i] <= matriz[cB][i]):
                matriz[cB][i] = 0
            elif(matriz[cA][i] > matriz[cB][i]):
                matriz[cA][i] = matriz[cB][i]
                matriz[cB][i] = 0
            else:
                pass
        # segundo cluster tem posição de valor 0
        elif(matriz[cB][i] == 0):
            if(matriz[cA][i] <= matriz[i][cB]):
                matriz[cB][i] = 0
            elif(matriz[cA][i] > matriz[i][cB]):
                matriz[cA][i] = matriz[i][cB]
                matriz[i][cB] = 0
            else:
                pass
    matriz = np.delete(matriz, cB, axis=0)
    return matriz

def escreve_arquivo(identificador, tam_matriz):
    """
    Escreve nos arquivos de saída de acordo com formato especificado:
        cluster_label\tcluster_id
    """
    nome_arquivo = sys.argv[1].replace('.txt', '') + '_' + str(tam_matriz) + '.txt'
    with open(nome_arquivo, 'w') as f:
        # escreve escreve escreve
        for idx in range(0, tam_matriz):
            clusters = identificador[idx].split(',')
            for label in clusters:
                linha = label + '\t' + str(idx) + '\n'
                f.write(linha)
    f.close()
    return nome_arquivo

if __name__ == '__main__':
    main()
