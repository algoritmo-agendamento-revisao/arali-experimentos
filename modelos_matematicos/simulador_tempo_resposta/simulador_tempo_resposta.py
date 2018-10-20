import numpy as np

def distribuicao_normal(media, desvio_padrao):
    # retorna um array, assim é necessário acessar sua posição única
    return np.random.normal(media, desvio_padrao, 1)[0] * 1000