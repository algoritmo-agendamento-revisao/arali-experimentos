from collections import defaultdict


class UtilitarioTeste:

    __episodio_recompensa_media__ = defaultdict(list)

    def salvar_recompensa_media(self, episodio: int, recompensa: float):
        self.__episodio_recompensa_media__[episodio] = recompensa

    def obter_recompensa_media_repeticao(self, episodio:int):
        return self.__episodio_recompensa_media__[episodio]

    def obter_recompensa_media(self):
        recompensa_acumulada = 0
        qtd_episodio = len(self.__episodio_recompensa_media__)
        for episodio in self.__episodio_recompensa_media__.keys():
            recompensa_acumulada += self.__episodio_recompensa_media__[episodio]
        return recompensa_acumulada/qtd_episodio

    def limpar_lista(self):
        self.__episodio_recompensa_media__.clear()
