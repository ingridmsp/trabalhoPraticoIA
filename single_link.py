import numpy as np
import scipy as sp

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

    return particoes, identificador

def qtd_particoes(dataset):
    with open(dataset) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

