import numpy as np
import scipy as sp

def le_arquivo(dataset):
    nlinhas = qtd_particoes(dataset) - 1
    particoes = np.zeros(nlinhas, 3)

    with open(dataset) as f:
        next(f)
        for linha in f:
            parametros = linha.split("\t")
            particoes[linha-1,0:2] = parametros



def qtd_particoes(dataset):
    with open(dataset) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
